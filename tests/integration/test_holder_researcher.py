# import pytest
# import logging
# from src.holder_researcher import TokenHolderTracker

# @pytest.fixture(autouse=True)
# def setup_logging():
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(message)s'
#     )

# @pytest.fixture
# def tracker():
#     return TokenHolderTracker()

# TEST_TOKENS = [
#     ('WALLY', '0x4f7d2D728ce137dd01ec63EF7B225805C7b54575', 'eth'),
#     ('JAIL', '8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump', 'solana'),
#     ('CHAOS', '0x20d704099B62aDa091028bcFc44445041eD16f09', 'base')
# ]

# @pytest.mark.integration
# @pytest.mark.parametrize("name,address,chain", TEST_TOKENS)
# def test_get_holders(tracker, name, address, chain):
#     logging.info(f"\nTesting {name} on {chain}")
#     result = tracker.get_holders(address, chain)

#     assert isinstance(result, int), f"Result should be an integer for {name}"
#     assert result > 0, f"No holders found for {name}"


# @pytest.mark.integration
# def test_invalid_token(tracker):
#     result = tracker.get_holders(
#         "0x0000000000000000000000000000000000000000",
#         "eth"
#     )
#     assert result == 0

# @pytest.mark.integration
# def test_invalid_chain(tracker):
#     result = tracker.get_holders(TEST_TOKENS[0][1], "invalid_chain")
#     assert result == 0