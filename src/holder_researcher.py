from src.solscan import Solscan


class HolderResearcher:
    def __init__(self):
        self.solscan = Solscan()

    def get_holders(self, token_address: str, chain: str) -> int:
        if chain == "solana":
            return self.solscan.get_token_metadata(token_address).holder
        else:
            return 0
