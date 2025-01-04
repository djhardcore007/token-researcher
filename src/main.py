import click
import logging
from pathlib import Path
from src.reporter import Reporter
from src.metrics import analyze_token
from src.utils import save_token_analysis


def setup_logger(debug: bool = False) -> logging.Logger:
    """Setup basic logger."""
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    return logging.getLogger('token_research')

@click.command()
@click.option('--token-address', '-t', required=True, help='Token contract address')
@click.option('--chain', '-c', default='ethereum', help='Chain name (default: ethereum)')
@click.option('--output-dir', '-o', default='output', help='Output directory', type=click.Path())
@click.option('--debug/--no-debug', default=False, help='Enable debug logging')
def main(token_address: str, chain: str, output_dir: str, debug: bool):
    """Research token and save report."""
    logger = setup_logger(debug)
    reporter = Reporter()

    # Generate report
    logger.info(f"Researching {token_address} on {chain}")
    report = reporter.generate_report(token_address, chain)

    if not report:
        logger.error("Could not generate report")
        return

    # Save report
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"report_{chain}_{report.dex.token_symbol}_{report.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    filepath = output_path / filename

    with open(filepath, 'w') as f:
        f.write(report.model_dump_json(indent=2))

    logger.info(f"Report saved: {filepath}")
    logger.info(f"Token: {report.dex.token_symbol} Price: ${report.dex.price_usd:.4f}")

    # Save analysis
    analysis = analyze_token(report)
    analysis_path = output_path / f"analysis_{chain}_{report.dex.token_symbol}_{report.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    save_token_analysis(analysis, analysis_path)

    logger.info(f"Analysis saved: {analysis_path}")

if __name__ == '__main__':
    main()
