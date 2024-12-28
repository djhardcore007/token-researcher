# from src.config import Config

# def main(tokens, file, output, debug):
#     """Research token information including price and social data."""
#     # Validate environment variables
#     try:
#         Config.validate()
#     except ValueError as e:
#         logger.error(f"Configuration error: {str(e)}")
#         return

#     logger = setup_logger(logging.DEBUG if debug else logging.INFO)
#     logger.debug("Starting token research")
#     # ... rest of the main function
