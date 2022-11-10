import re
from colorama import Fore, Style

class Printer:
    def __init__(self, color, verbose):
        self.color = color
        self.verbose = verbose

    def content(self, text: str) -> None:
        text = re.sub("^", " | ", text)
        text = text.replace("\n", "\n | ")
        print(text)


    def positive(self, text: str):
        if self.color:
            print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {text}")
        else:
            print(f"[+] {text}")


    def negative(self, text: str):
        if self.color:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} {text}")
        else:
            print(f"[-] {text}")


    def good(self, text: str):
        if self.color:
            print(f"{Fore.GREEN}[✔]{Style.RESET_ALL} {text}")
        else:
            print(f"[✔] {text}")


    def bad(self, text: str):
        if self.color:
            print(f"{Fore.RED}[✘]{Style.RESET_ALL} {text}")
        else:
            print(f"[✘] {text}")


    def warning(self, text: str):
        if self.color:
            print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {text}")
        else:
            print(f"[+] {text}")


    def info(self, text: str):
        if self.color:
            print(f"{Fore.BLUE}[i]{Style.RESET_ALL} {text}", end="\n" if self.verbose else "\r")
        else:
            print(f"[i] {text}", end="\n" if self.verbose else "\r")
