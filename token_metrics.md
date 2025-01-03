# Crypto Analysis Metrics & Formulas

## Volume & Price Metrics
* **Continuous Price Increase (CPI)**
  * `CPI = ∏(Pᵢ/Pᵢ₋₁) where i = current day`
  * Measures consecutive daily price increases

* **Turnover Rate (TR)**
  * `TR = (24h Trading Volume / Circulating Supply) × 100%`
  * Indicates trading activity relative to available supply

* **Net Flow Ratio (NFR)**
  * `NFR = (Inflow - Outflow) / (Inflow + Outflow)`
  * Range: [-1, 1], positive indicates net buying pressure

## On-Chain Metrics
* **Daily Active Addresses (DAA)**
  * `DAA = Count(Unique Addresses with Transactions)₂₄ₕ`

* **Liquidity Depth (LD)**
  * `LD = (Liquidity Pool Value / Market Cap) × 100%`
  * Alpha Signal if `LD > 10%`

* **Market Depth Ratio (MDR)**
  * `MDR = ∑(Orders within ±2% of current price) / Market Cap`

## Wallet Concentration
* **Gini Coefficient (GC)**
  * `GC = (∑(i=1 to n) ∑(j=1 to n) |xᵢ - xⱼ|) / (2n²μ)`
  * Where x = wallet holdings, n = total wallets, μ = mean holdings

* **Top Holder Concentration (THC)**
  * `THC₁₀ = (∑Top 10 Wallet Holdings / Total Supply) × 100%`
  * `THC₂₀ = (∑Top 20 Wallet Holdings / Total Supply) × 100%`

## Social Metrics
* **Social Dominance (SD)**
  * `SD = (Project Mentions / Total Crypto Mentions) × 100%`

* **Engagement Rate (ER)**
  * `ER = ((Likes + Comments + Retweets) / Impressions) × 100%`

* **Sentiment Score (SS)**
  * `SS = (Positive Mentions - Negative Mentions) / Total Mentions`
  * Range: [-1, 1]

## Financial Metrics
* **On-Chain P/E Ratio**
  * `P/E = Market Cap / (Annual Protocol Revenue)`

* **Revenue Growth Rate (RGR)**
  * `RGR = ((Current Revenue - Previous Revenue) / Previous Revenue) × 100%`

* **Protocol Revenue per Token (PRT)**
  * `PRT = Annual Protocol Revenue / Circulating Supply`

## KOL Analysis
* **KOL Holding Impact (KHI)**
  * `KHI = (∑KOL Holdings / Total Supply) × 100%`

* **KOL Movement Impact (KMI)**
  * `KMI = (KOL Net Flow / 24h Volume) × 100%`

* **KOL Concentration Index (KCI)**
  * `KCI = (Largest KOL Holding / ∑All KOL Holdings) × 100%`

## Notes
* All metrics should be monitored across multiple timeframes (24h, 7d, 30d)
* Thresholds and signals should be calibrated based on market conditions
* Consider correlations between metrics for stronger signals
* Historical volatility should be factored into threshold settings