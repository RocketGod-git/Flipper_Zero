class Color:
    @classmethod
    def green(self, s: str) -> str:
        return f"\033[32m{s}\x1b[0m"
