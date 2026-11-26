
from pathlib import Path
from core.security import PasswordSecurity


class PasswordChecker:

    def __init__(self, wordlist_path=None):

        base_dir = Path(__file__).resolve().parent.parent

        self.wordlist_path = (
            Path(wordlist_path)
            if wordlist_path
            else base_dir / "data" / "wordlist.txt"
        )

        self.common_passwords = set()
        self.load_wordlist()

    def load_wordlist(self):

        if not self.wordlist_path.exists():
            raise FileNotFoundError("Wordlist file not found.")

        passwords = set()

        with self.wordlist_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                # Remove only the line ending, preserving password spaces and case.
                password = line.rstrip("\r\n")

                if password:
                    passwords.add(password)

        self.common_passwords = passwords

    def check_password(self, password):

        if not isinstance(password, str) or not password:
            return {
                "safe": False,
                "common": False,
                "message": "Please enter a password.",
                "strength": None
            }

        # Password comparison is case-sensitive.
        common = password in self.common_passwords

        strength = PasswordSecurity.evaluate(password)

        if common:

            message = "WARNING: Common password detected."
            safe = False

        elif strength["level"] in ("WEAK", "MODERATE"):

            message = "Password needs improvement."
            safe = False

        else:

            message = "No common-list match detected."
            safe = True

        return {
            "safe": safe,
            "common": common,
            "message": message,
            "strength": strength
        }
