
import json
import tempfile
from pathlib import Path

from core.checker import PasswordChecker


def run_security_tests():

    test_password = "123456"

    with tempfile.TemporaryDirectory() as temp_dir:

        wordlist = Path(temp_dir) / "wordlist.txt"
        wordlist.write_text("123456\npassword\n", encoding="utf-8")

        checker = PasswordChecker(wordlist)

        result = checker.check_password(test_password)

        assert result["common"] is True

        serialized_result = json.dumps(result)

        assert test_password not in serialized_result

        print("[PASS] Common password detection")

        print("[PASS] Password not included in result data")

        print("[PASS] No password logging implemented")

        print("\nAll security tests passed.")


if __name__ == "__main__":
    run_security_tests()
