# Understand the methods, preserve the evidence

Public investigations describe a recurring set of stages. These stages are analytical categories: an individual incident may skip, repeat or reorder them. Evidence that assets reached a service is different from evidence that they were sold for cash.

## 1. Theft and initial transfers

Investigators first establish the incident, transaction history and attribution. Attribution may come from a government statement, an exchange, a research firm or an independent investigator. Those are different kinds of evidence and should remain attributed to their source.

For defenders: record transaction hashes, chain, token, amount, timestamps and original incident notices. Keep an access date and distinguish a source's allegation from a conclusion you independently reproduced.

## 2. Conversion and cross-chain swaps

Tokens may be sold or exchanged for assets on other chains. A swap service can process a large amount while retaining little customer money afterward. A wallet interface may route a trade through a separate liquidity protocol; both can receive different fees.

For defenders: identify the interface, underlying protocol and destination asset separately. Preserve evidence of each observed hop and mark the point where an inference replaces direct observation. Do not infer exchange custody from use of that exchange's Web3 brand.

Example: the [March 4, 2025 Bybit update](https://x.com/benbybit/status/1896798476945744010) distinguishes THORChain processing and OKX Web3 proxy activity. Those figures are historical flows, not current holdings.

## 3. Privacy and mixing

Public reports describe both custodial mixers and protocols where users retain control through cryptographic mechanisms. CoinJoin wallets, independent coordinators, market participants and application developers have distinct roles. A known incoming amount does not automatically reveal a current attributable balance or every recipient of fees.

For defenders: preserve the distinction between an observed deposit, an attributed withdrawal and an inference. Report attribution uncertainty rather than assigning unrelated users' funds to a suspected actor.

Example: the [FBI's Harmony statement](https://www.fbi.gov/news/press-releases/fbi-confirms-lazarus-group-cyber-actors-responsible-for-harmonys-horizon-bridge-currency-theft) reports over $60m processed through RAILGUN in January 2023. That does not establish how much remains there today or how current controls operate.

## 4. Brokers, exchanges and cash conversion

A transfer to a broker or exchange is a potential intervention point, not proof of a completed fiat payout. Investigators often have less public visibility once funds enter custodial accounts or off-chain arrangements.

For defenders: share a concise evidence bundle through the relevant exchange's official incident channel and the appropriate authorities. Include the chain, hashes, dates, source links and an explanation of why you associate the funds with the incident. Distinguish frozen assets, returned assets and unresolved exposure.

The [Multilateral Sanctions Monitoring Team report](https://www.mofa.go.jp/mofaj/files/100922718.pdf) provides background on reported DPRK laundering and cash-conversion networks. The [FinCEN Huione finding](https://www.fincen.gov/news/news-releases/fincen-finds-cambodia-based-huione-group-be-primary-money-laundering-concern) illustrates group-wide exposure without a fee or business-level breakdown.

## 5. Fees and incentives

Ask four separate questions:

1. How much passed through the service, and over which period?
2. What rate applied to those particular transactions?
3. Who received the payment: operator, liquidity provider, relayer, miner, governance treasury or token mechanism?
4. Was any amount later refunded or recovered?

An illustrative fee scenario uses `reported flow x assumed rate`. It becomes observed revenue only after actual receipts are reconciled. Processing costs, price impact, gross fees and net profit are different measures.

The [Bybit ParaSwap proposal](https://gov.velora.xyz/t/pip-59-proposal-for-returning-40-203-weth-to-bybit-after-10-bounty-deduction/2065) identifies a specific fee amount and requests its return. It is stronger evidence of attributed fees than applying a generic rate to a large flow, while still requiring follow-up before claiming a final retained amount.
