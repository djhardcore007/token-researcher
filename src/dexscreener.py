import logging
import click
import pandas as pd
from datetime import datetime
import os
import requests

class DexScreener:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest"

    def get_token_info(self, token_address):
        endpoint = f"{self.base_url}/dex/tokens/{token_address}"
        response = requests.get(endpoint)

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}")

        return response.json()

    def get_timeframe_metrics(self, txn_data, volume_data, timeframe):
        return {
            # Transaction counts
            f'buys_{timeframe}': txn_data.get('buys', 0),
            f'sells_{timeframe}': txn_data.get('sells', 0),
            f'total_txns_{timeframe}': (txn_data.get('buys', 0) + txn_data.get('sells', 0)),

            # Volume data
            f'volume_{timeframe}': volume_data,
        }

    def process_token_data(self, token_data):
        pairs = token_data.get('pairs', [])
        if not pairs:
            return None

        # Get the most liquid pair
        main_pair = max(pairs, key=lambda x: float(x.get('liquidity', {}).get('usd', 0)))

        # Get price metrics
        price_metrics = main_pair.get('priceChange', {})

        # Get transaction and volume metrics for different timeframes
        txn_5m = main_pair.get('txns', {}).get('m5', {})
        txn_1h = main_pair.get('txns', {}).get('h1', {})
        txn_6h = main_pair.get('txns', {}).get('h6', {})
        txn_24h = main_pair.get('txns', {}).get('h24', {})

        volume_5m = main_pair.get('volume', {}).get('m5', 0)
        volume_1h = main_pair.get('volume', {}).get('h1', 0)
        volume_6h = main_pair.get('volume', {}).get('h6', 0)
        volume_24h = main_pair.get('volume', {}).get('h24', 0)

        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'token_name': main_pair.get('baseToken', {}).get('name'),
            'token_symbol': main_pair.get('baseToken', {}).get('symbol'),
            'price_usd': main_pair.get('priceUsd'),
            'price_native': main_pair.get('priceNative'),

            # Price changes
            'price_change_5m': price_metrics.get('m5'),
            'price_change_1h': price_metrics.get('h1'),
            'price_change_6h': price_metrics.get('h6'),
            'price_change_24h': price_metrics.get('h24'),

            # Market metrics
            'liquidity_usd': main_pair.get('liquidity', {}).get('usd'),
            'fdv': main_pair.get('fdv'),
            'market_cap': main_pair.get('marketCap'),

            # Chain info
            'chain': main_pair.get('chainId'),
            'dex_id': main_pair.get('dexId'),
            'pair_address': main_pair.get('pairAddress'),
        }

        # Add metrics for each timeframe
        data.update(self.get_timeframe_metrics(txn_5m, volume_5m, '5m'))
        data.update(self.get_timeframe_metrics(txn_1h, volume_1h, '1h'))
        data.update(self.get_timeframe_metrics(txn_6h, volume_6h, '6h'))
        data.update(self.get_timeframe_metrics(txn_24h, volume_24h, '24h'))

        return data

def setup_logger(log_level=logging.INFO):
    """Configure logging settings."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def get_token_addresses(tokens: str = None, file: str = None, logger=None) -> set:
    """Get token addresses from command line args or file."""
    token_addresses = set()

    if tokens:
        token_addresses.update([addr.strip() for addr in tokens.split(',') if addr.strip()])

    if file:
        try:
            with open(file, 'r') as f:
                token_addresses.update([line.strip() for line in f if line.strip()])
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")

    return token_addresses

def research_tokens(addresses: set, logger=None) -> list:
    """Research token information for given addresses."""
    researcher = DexScreener()
    results = []

    total = len(addresses)
    for i, addr in enumerate(addresses, 1):
        try:
            logger.info(f"Processing token {i}/{total}: {addr}")
            token_data = researcher.get_token_info(addr)
            processed_data = researcher.process_token_data(token_data)
            if processed_data:
                results.append(processed_data)
        except Exception as e:
            logger.error(f"Error processing token {addr}: {str(e)}")

    return results

def save_results(results: list, output_dir: str, logger=None):
    """Save research results to CSV."""
    if not results:
        logger.warning("No results to save.")
        return

    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(results)
    output_file = os.path.join(output_dir, f"dexscreener_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    df.to_csv(output_file, index=False)
    logger.info(f"Results saved to {output_file}")

@click.command()
@click.option('--tokens', '-t', help='Comma-separated list of token addresses')
@click.option('--file', '-f', type=click.Path(exists=True), help='Text file containing token addresses (one per line)')
@click.option('--output', '-o', type=click.Path(), default='output', help='Output directory path (default: ./output)')
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(tokens, file, output, debug):
    """Research token information from DexScreener."""
    # Setup logger
    logger = setup_logger(logging.DEBUG if debug else logging.INFO)
    logger.debug("Starting token research")

    # Get token addresses
    addresses = get_token_addresses(tokens, file, logger)
    if not addresses:
        logger.error("No token addresses provided. Use --tokens or --file to specify addresses.")
        return

    logger.info(f"Found {len(addresses)} token addresses to process")

    # Research tokens
    results = research_tokens(addresses, logger)
    logger.info(f"Successfully processed {len(results)} tokens")

    # Save results
    save_results(results, output, logger)
    logger.debug("Token research completed")

if __name__ == '__main__':
    main()