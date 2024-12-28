# token-researcher
research a token given token addr.

## Goal
Given a token address, find out all the information about the token.

## Features
- Token basic information (name, symbol, decimals)
- Price data from DexScreener API
- Trading volume and liquidity information
- Price charts and historical data
- Multiple chain support

## API Integration
This project utilizes the DexScreener API to fetch real-time token data:
- Price information
- Trading pairs
- Market statistics
- Liquidity pools


## Usage

```bash
docker-compose up
docker-compose run test
docker-compose run test pytest
docker-compose run dexscreener /bin/bash
```