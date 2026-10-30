"""Offline evidence search and reproducible fee scenarios. Standard library only."""

import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from importlib.resources import files
import json
import sys
from urllib.parse import urlparse


METRICS = {"flow", "fee", "processing_cost", "context_revenue"}
EVIDENCE = {"reported", "calculated"}


def load_data():
    return json.loads(files("dprk_fightback").joinpath("data.json").read_text())


def number(value):
    if not isinstance(value, str):
        raise ValueError("numeric values must be decimal strings")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("invalid decimal value") from exc
    if not result.is_finite() or result < 0:
        raise ValueError("numeric values must be finite and non-negative")
    return result


def scenario_amounts(record, records):
    """Calculate once per independent scenario; never sum across claims."""
    calculation = record["calculation"]
    parent = records[calculation["flow_claim"]]
    return [number(parent["amount"]["value"]) * number(rate)
            for rate in calculation["rates"]]


def validate(data):
    errors = []
    services = {item["id"] for item in data["services"]}
    records = {item["id"]: item for item in data["claims"]}
    if len(services) != len(data["services"]):
        errors.append("duplicate service id")
    if len(records) != len(data["claims"]):
        errors.append("duplicate claim id")
    for record in data["claims"]:
        try:
            if record["service"] not in services:
                raise ValueError("unknown service")
            if record["metric"] not in METRICS or record["evidence"] not in EVIDENCE:
                raise ValueError("invalid metric or evidence type")
            date.fromisoformat(record["as_of"])
            if not record["scope"] or not record["limitations"]:
                raise ValueError("scope and limitations are required")
            if not record["sources"]:
                raise ValueError("at least one source is required")
            for source in record["sources"]:
                parsed = urlparse(source["url"])
                if parsed.scheme != "https" or not parsed.netloc or not source["title"]:
                    raise ValueError("sources need an HTTPS URL and title")
            amount = record["amount"]
            if not amount["currency"] or amount["qualifier"] not in {
                "approximate", "more_than", "at_least", "reported", "scenario"
            }:
                raise ValueError("invalid amount currency or qualifier")
            values = [number(value) for value in amount["values"]] if "values" in amount else [number(amount["value"])]
            if record["evidence"] == "calculated":
                calculation = record["calculation"]
                parent = records[calculation["flow_claim"]]
                if parent["metric"] != "flow" or parent["evidence"] != "reported":
                    raise ValueError("fee scenarios must reference a reported flow")
                if parent["service"] != record["service"]:
                    raise ValueError("scenario and flow must refer to the same service")
                if record["metric"] != "fee" or amount["currency"] != parent["amount"]["currency"]:
                    raise ValueError("scenario must be a fee in the flow currency")
                rates = calculation["rates"]
                if not rates or any(number(rate) > 1 for rate in rates):
                    raise ValueError("fee rates must be between zero and one")
                if amount["qualifier"] != "scenario" or values != scenario_amounts(record, records):
                    raise ValueError("scenario values do not match flow times rates")
                if not calculation["assumptions"]:
                    raise ValueError("scenario assumptions are required")
        except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
            errors.append(f"{record.get('id', '?')}: {exc}")
    return errors


def money(amount):
    values = amount.get("values", [amount.get("value")])
    return " / ".join(f"{number(value):,f} {amount['currency']}" for value in values)


def service_matches(service, query):
    return query.casefold() in " ".join(
        [service["id"], service["name"], *service.get("aliases", [])]
    ).casefold()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    services_parser = sub.add_parser("services", help="list service roles and evidence gaps")
    services_parser.add_argument("--json", action="store_true")
    for command in ("search", "show", "fees", "export"):
        item = sub.add_parser(command)
        if command == "search":
            item.add_argument("query")
        if command == "show":
            item.add_argument("service")
        if command in {"fees", "export"}:
            item.add_argument("--service", default="")
        if command != "export":
            item.add_argument("--json", action="store_true")
        if command in {"search", "show", "fees"}:
            item.add_argument("--evidence", choices=sorted(EVIDENCE))
        if command == "export":
            item.add_argument("--format", choices=["json", "csv"], default="json")
    sub.add_parser("validate", help="check sources, scope and calculation consistency")
    args = parser.parse_args(argv)
    data = load_data()
    errors = validate(data)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    if args.command == "validate":
        print(f"Valid: {len(data['services'])} services, {len(data['claims'])} claims. "
              "This checks data integrity, not source truth or current balances.")
        return 0
    if args.command == "services":
        if args.json:
            print(json.dumps(data["services"], indent=2))
        else:
            for service in data["services"]:
                count = sum(record["service"] == service["id"] for record in data["claims"])
                print(f"{service['name']} | {service['role']} | {count} numerical records")
        return 0
    selected_services = data["services"]
    query = getattr(args, "service", "")
    if query:
        selected_services = [service for service in selected_services if service_matches(service, query)]
        if not selected_services:
            parser.exit(1, f"No service matching {query!r}.\n")
    service_ids = {service["id"] for service in selected_services}
    records = [record for record in data["claims"] if record["service"] in service_ids]
    if args.command == "fees":
        records = [record for record in records if record["metric"] in {"fee", "processing_cost", "context_revenue"}]
    if getattr(args, "evidence", None):
        records = [record for record in records if record["evidence"] == args.evidence]
    if args.command == "search":
        term = args.query.casefold()
        records = [record for record in records if term in json.dumps(record, ensure_ascii=False).casefold()]
    if args.command == "export" and args.format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(["id", "service", "metric", "evidence", "as_of", "amount", "qualifier", "scope", "limitations", "sources", "calculation"])
        for record in records:
            writer.writerow([record["id"], record["service"], record["metric"], record["evidence"], record["as_of"], money(record["amount"]), record["amount"]["qualifier"], record["scope"], record["limitations"], json.dumps(record["sources"]), json.dumps(record.get("calculation"))])
    elif args.command == "export" or args.json:
        print(json.dumps({"dataset_as_of": data["as_of"], "services": selected_services, "claims": records}, indent=2))
    else:
        if not records:
            print("No matching numerical evidence in this dataset. Unknown does not mean zero.")
        names = {service["id"]: service["name"] for service in data["services"]}
        for record in records:
            print(f"\n{record['id']} | {names[record['service']]} | {record['evidence']} | {record['metric']}")
            print(f"  {money(record['amount'])} ({record['amount']['qualifier']}); as of {record['as_of']}")
            print(f"  Scope: {record['scope']}")
            print(f"  Limits: {record['limitations']}")
            if "calculation" in record:
                print(f"  Calculation: flow {record['calculation']['flow_claim']} x rates {', '.join(record['calculation']['rates'])}")
                print(f"  Assumptions: {record['calculation']['assumptions']}")
            for source in record["sources"]:
                print(f"  Source: {source['title']} - {source['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
