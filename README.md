# Token Research Toolkit
You can find our latest analysis reports on [Twitter](https://x.com/berkshire_ai)

# Goal
* Create a tool to analyze crypto projects and provide insights on their potential for success.

## Data Sources
- [Dexscreener](https://dexscreener.com/)
- [CoinGecko](https://www.coingecko.com/)
- [Solscan](https://solscan.io/)

## Token Metrics
We will use the following metrics to analyze the token:
- [Token Metrics](./token_metrics.md)

## Dev
```
# Build the containers
docker compose build

# Start and access the dev container
docker compose run --rm dev

# Or access an already running container
docker compose exec dev bash
```