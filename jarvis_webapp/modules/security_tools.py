"""
JARVIS Security Tools — password generation, hash, encode/decode
"""
import random
import string
import hashlib
import base64
import re


class SecurityTools:

    def generate_password(self, length: int = 16, strong: bool = True) -> str:
        """Generate a secure random password"""
        if length < 6:
            length = 6
        if length > 64:
            length = 64

        if strong:
            chars = (string.ascii_uppercase + string.ascii_lowercase +
                     string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?")
        else:
            chars = string.ascii_letters + string.digits

        # Ensure at least one of each required type
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
        ]
        if strong:
            password.append(random.choice("!@#$%^&*()_+-="))

        password += [random.choice(chars) for _ in range(length - len(password))]
        random.shuffle(password)
        pwd = "".join(password)

        strength = self._assess_strength(pwd)
        return (f"Generated password, sir:\n\n"
                f"🔐 Password: {pwd}\n"
                f"📏 Length: {length} characters\n"
                f"💪 Strength: {strength}\n\n"
                f"Please store this securely and do not share it.")

    def _assess_strength(self, pwd: str) -> str:
        score = 0
        if len(pwd) >= 12: score += 1
        if len(pwd) >= 16: score += 1
        if re.search(r'[A-Z]', pwd): score += 1
        if re.search(r'[a-z]', pwd): score += 1
        if re.search(r'\d', pwd): score += 1
        if re.search(r'[^A-Za-z0-9]', pwd): score += 1
        if score >= 6: return "Very Strong 🟢"
        if score >= 4: return "Strong 🟡"
        if score >= 2: return "Moderate 🟠"
        return "Weak 🔴"

    def hash_text(self, text: str, algorithm: str = "sha256") -> str:
        """Hash a string"""
        algos = {"md5": hashlib.md5, "sha1": hashlib.sha1,
                 "sha256": hashlib.sha256, "sha512": hashlib.sha512}
        fn = algos.get(algorithm.lower(), hashlib.sha256)
        result = fn(text.encode()).hexdigest()
        return (f"Hash result, sir:\n\n"
                f"📝 Input: {text}\n"
                f"🔑 Algorithm: {algorithm.upper()}\n"
                f"#️⃣ Hash: {result}")

    def encode_base64(self, text: str) -> str:
        encoded = base64.b64encode(text.encode()).decode()
        return f"Base64 encoded, sir:\n\n📝 Input: {text}\n🔐 Encoded: {encoded}"

    def decode_base64(self, text: str) -> str:
        try:
            decoded = base64.b64decode(text.encode()).decode()
            return f"Base64 decoded, sir:\n\n🔐 Input: {text}\n📝 Decoded: {decoded}"
        except Exception:
            return "That doesn't appear to be valid Base64, sir."

    def check_password_strength(self, password: str) -> str:
        strength = self._assess_strength(password)
        issues = []
        if len(password) < 8: issues.append("Too short (< 8 chars)")
        if not re.search(r'[A-Z]', password): issues.append("No uppercase letters")
        if not re.search(r'[a-z]', password): issues.append("No lowercase letters")
        if not re.search(r'\d', password): issues.append("No numbers")
        if not re.search(r'[^A-Za-z0-9]', password): issues.append("No special characters")

        result = f"Password Strength: {strength}\n"
        if issues:
            result += "⚠ Suggestions:\n" + "\n".join(f"  • {i}" for i in issues)
        else:
            result += "✅ This password meets all security criteria, sir."
        return result


security_tools = SecurityTools()
