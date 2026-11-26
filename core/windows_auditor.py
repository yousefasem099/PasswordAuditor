
import os
import subprocess
import json


class WindowsAccountAuditor:

    @staticmethod
    def get_local_accounts():

        if os.name != "nt":
            raise OSError("This module requires Windows.")

        command = (
            "Get-LocalUser | "
            "Select-Object Name, Enabled, "
            "PasswordRequired, PasswordLastSet | "
            "ConvertTo-Json -Depth 2"
        )

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        output = result.stdout.strip()

        if not output:
            return []

        accounts = json.loads(output)

        if isinstance(accounts, dict):
            accounts = [accounts]

        return [
            {
                "username": account.get("Name"),
                "enabled": account.get("Enabled"),
                "password_required": account.get("PasswordRequired"),
                "password_last_set": account.get("PasswordLastSet")
            }
            for account in accounts
        ]

    @staticmethod
    def get_password_policy():

        if os.name != "nt":
            raise OSError("This module requires Windows.")

        result = subprocess.run(
            ["net", "accounts"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        policy = {}

        for line in result.stdout.splitlines():

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            policy[key.strip()] = value.strip()

        return policy


if __name__ == "__main__":

    print("\n=== WINDOWS LOCAL ACCOUNT AUDITOR ===\n")

    try:

        accounts = WindowsAccountAuditor.get_local_accounts()

        print("LOCAL ACCOUNTS")

        for account in accounts:
            print("-" * 40)

            for key, value in account.items():
                print(f"{key}: {value}")

        print("\nPASSWORD POLICY")
        print("=" * 40)

        policy = WindowsAccountAuditor.get_password_policy()

        for key, value in policy.items():
            print(f"{key}: {value}")

        print("\nWindows audit completed successfully.")

    except (
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        json.JSONDecodeError
    ) as error:

        print("Audit error:", error)
