# token-researcher
research a token given token addr.

## Usage

`python -m src.main -t 0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82 --chain=bsc`

`python -m src.main -t 0x4f7d2D728ce137dd01ec63EF7B225805C7b54575 --chain=ethereum`

`python -m src.main -t 0x20d704099B62aDa091028bcFc44445041eD16f09 --chain=base`

`python -m src.main -t 8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump --chain=solana`

## Development
```bash
docker-compose up
docker-compose run test
docker-compose run test pytest
docker-compose run dexscreener /bin/bash
```