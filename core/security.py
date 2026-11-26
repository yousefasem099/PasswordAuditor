
import re


class PasswordSecurity:

    @staticmethod
    def evaluate(password):

        if not isinstance(password, str) or not password:
            return {
                "score": 0,
                "level": "EMPTY",
                "recommendation": "Enter a password."
            }

        score = 0
        lower_password = password.lower()

        # 1. Password length
        if len(password) >= 8:
            score += 1

        if len(password) >= 12:
            score += 1

        if len(password) >= 16:
            score += 1

        # 2. Character diversity
        if re.search(r"[a-z]", password):
            score += 1

        if re.search(r"[A-Z]", password):
            score += 1

        if re.search(r"[0-9]", password):
            score += 1

        if re.search(r"[^a-zA-Z0-9]", password):
            score += 1

        # 3. Repeated character detection
        repeated = bool(
            re.search(r"(.)\1{3,}", password)
        )

        # 4. Sequential pattern detection
        sequential_patterns = (
            "12345",
            "23456",
            "34567",
            "45678",
            "56789",
            "qwerty",
            "asdfgh",
            "zxcvbn",
            "abcdef"
        )

        sequential = any(
            pattern in lower_password
            for pattern in sequential_patterns
        )

        # 5. Common password pattern detection
        common_patterns = (
            "password",
            "admin",
            "welcome",
            "letmein",
            "iloveyou",
            "monkey",
            "dragon"
        )

        common_word = any(
            pattern in lower_password
            for pattern in common_patterns
        )

        # 6. Apply penalties
        if repeated or sequential or common_word:
            score = min(score, 2)

        # 7. Determine password strength
        if score <= 2:
            level = "WEAK"
            recommendation = (
                "Use a longer and less predictable password."
            )

        elif score <= 4:
            level = "MODERATE"
            recommendation = (
                "Increase password length and character diversity."
            )

        elif score <= 6:
            level = "STRONG"
            recommendation = (
                "Good password characteristics."
            )

        else:
            level = "VERY STRONG"
            recommendation = (
                "Good length and character diversity."
            )

        return {
            "score": score,
            "level": level,
            "recommendation": recommendation
        }
