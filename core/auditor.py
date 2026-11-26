
import json
import hashlib
import secrets
import hmac
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

ACCOUNTS_FILE = DATA_DIR / "accounts.json"
WORDLIST_FILE = DATA_DIR / "wordlist.txt"

ALGORITHM = "PBKDF2-HMAC-SHA256"
ITERATIONS = 100_000
SALT_LENGTH = 16


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    ).hex()


def create_demo_accounts():
    """Create synthetic accounts for authorized lab testing."""

    demo_users = [
        ("test_weak", "123456"),
        ("test_strong", "YemenCyber!2026#Secure")
    ]

    accounts = []

    for username, password in demo_users:
        salt = secrets.token_bytes(SALT_LENGTH)

        accounts.append({
            "username": username,
            "algorithm": ALGORITHM,
            "iterations": ITERATIONS,
            "salt": salt.hex(),
            "hash": hash_password(password, salt)
        })

    ACCOUNTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with ACCOUNTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)

    print("Synthetic test accounts created successfully.")


class SystemAccountAuditor:

    def __init__(self):
        self.wordlist = self.load_wordlist()

    def load_wordlist(self):

        if not WORDLIST_FILE.exists():
            raise FileNotFoundError("Wordlist not found.")

        passwords = set()

        with WORDLIST_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                password = line.rstrip("\r\n")

                if password:
                    passwords.add(password)

        return passwords

    def validate_account(self, account):

        if not isinstance(account, dict):
            raise ValueError("Invalid account record.")

        required_fields = (
            "username",
            "algorithm",
            "iterations",
            "salt",
            "hash"
        )

        if not all(field in account for field in required_fields):
            raise ValueError("Account record is missing required fields.")

        if not isinstance(account["username"], str):
            raise ValueError("Invalid username.")

        if account["algorithm"] != ALGORITHM:
            raise ValueError("Unsupported password-hashing algorithm.")

        iterations = account["iterations"]

        if (
            isinstance(iterations, bool)
            or not isinstance(iterations, int)
            or not 1 <= iterations <= 10_000_000
        ):
            raise ValueError("Invalid PBKDF2 iteration count.")

        try:
            salt = bytes.fromhex(account["salt"])
            stored_hash = bytes.fromhex(account["hash"])
        except (TypeError, ValueError):
            raise ValueError("Invalid salt or hash encoding.")

        if len(salt) != SALT_LENGTH:
            raise ValueError("Invalid salt length.")

        if len(stored_hash) != 32:
            raise ValueError("Invalid SHA-256 hash length.")

        return salt, stored_hash, iterations

    def audit_accounts(self):

        if not ACCOUNTS_FILE.exists():
            create_demo_accounts()

        with ACCOUNTS_FILE.open("r", encoding="utf-8") as file:
            accounts = json.load(file)

        if not isinstance(accounts, list):
            raise ValueError("Invalid accounts file format.")

        findings = []

        for account in accounts:

            salt, stored_hash, iterations = (
                self.validate_account(account)
            )

            compromised = False

            for candidate in self.wordlist:

                candidate_hash = hashlib.pbkdf2_hmac(
                    "sha256",
                    candidate.encode("utf-8"),
                    salt,
                    iterations
                )

                if hmac.compare_digest(candidate_hash, stored_hash):
                    compromised = True
                    break

            findings.append({
                "username": account["username"],
                "algorithm": account["algorithm"],
                "status": (
                    "WEAK PASSWORD DETECTED"
                    if compromised
                    else "NO WORDLIST MATCH"
                )
            })

        return findings

    def generate_report(self, findings):

        REPORT_DIR.mkdir(parents=True, exist_ok=True)

        report_path = REPORT_DIR / "audit_report.json"

        with report_path.open("w", encoding="utf-8") as file:
            json.dump(
                findings,
                file,
                indent=4,
                ensure_ascii=False
            )

        return report_path


if __name__ == "__main__":

    auditor = SystemAccountAuditor()

    print("\n=== SYSTEM ACCOUNT AUDITOR ===\n")

    try:
        findings = auditor.audit_accounts()

        for item in findings:
            print("--------------------------------")
            print("Username:", item["username"])
            print("Algorithm:", item["algorithm"])
            print("Status:", item["status"])

        report = auditor.generate_report(findings)

        print("\nAudit completed.")
        print("Report saved to:", report)

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("\nAudit error:", error)
