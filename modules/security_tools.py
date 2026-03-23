"""
Security Tools Module
Password generation, strength checking, hashing
"""

import random
import string
import hashlib

class SecurityTools:
    """Security utilities"""

    def generate_password(self, length: int = 16) -> str:
        """Generate a secure random password"""
        # Ensure at least one of each type
        lower = random.choice(string.ascii_lowercase)
        upper = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice('!@#$%^&*()_+-=[]{}|;:,.<>?')

        # Fill remaining
        remaining = length - 4
        all_chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
        rest = ''.join(random.choice(all_chars) for _ in range(remaining))

        # Combine and shuffle
        password = list(lower + upper + digit + special + rest)
        random.shuffle(password)
        pwd = ''.join(password)

        strength = self.check_strength(pwd)

        return (
            f"🔐 Generated Password:\n"
            f"  {pwd}\n\n"
            f"📊 Length: {length} characters\n"
            f"💪 Strength: {strength}\n"
            f"⚠️ Save this password in a safe place!"
        )

    def check_strength(self, password: str) -> str:
        """Check password strength"""
        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password): score += 1

        if score >= 6: return "🟢 Very Strong"
        if score >= 4: return "🟡 Strong"
        if score >= 3: return "🟠 Moderate"
        return "🔴 Weak"

    def hash_text(self, text: str) -> str:
        """Generate hashes"""
        md5 = hashlib.md5(text.encode()).hexdigest()
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        return (
            f"🔒 Hash Results for \"{text[:30]}{'...' if len(text) > 30 else ''}\":\n"
            f"  MD5:    {md5}\n"
            f"  SHA256: {sha256}"
        )

security_tools = SecurityTools()
