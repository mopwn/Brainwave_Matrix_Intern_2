import sqlite3
import re
from enum import Enum

class StrengthLevel(Enum):
    WEAK = "Weak"
    MODERATE = "Moderate"
    STRONG = "Strong"
def password_strength(password):
    # Initialize score
    score = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase the length to at least 8 characters.")

    # Character diversity checks
    if re.search(r'[a-z]', password): score += 1
    else: feedback.append("Add lowercase letters.")
    if re.search(r'[A-Z]', password): score += 1
    else: feedback.append("Add uppercase letters.")
    if re.search(r'\d', password): score += 1
    else: feedback.append("Add numbers.")
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1
    else: feedback.append("Add special characters.")

    # Dictionary and common pattern checks
    def is_common_password(password):
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()

        # Query the database
        cursor.execute('SELECT 1 FROM common_passwords WHERE password = ? LIMIT 1;', (password.lower(),))
        result = cursor.fetchone()

        conn.close()
        return result is not None
    if is_common_password(password):
        feedback.append("This is a common password. Please choose a stronger one.")
    else:
        score += 1
    if len(set(password)) < len(password)/2:
        feedback.append("Avoid repeated characters")
    else:
        score += 1
    def has_sequence(password, min_length=3):
        sequences = [
            "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "0123456789", "!@#$%^&*()",
            "qwertyuiopasdfghjklzxcvbnm"
    ]
        for seq in sequences:
            for i in range(len(seq) - min_length + 1):
                if seq[i:i + min_length] in password or seq[i:i + min_length][::-1] in password:
                    return True
        return False

    if has_sequence(password, min_length=3):  # Detect sequences of length 3 or more
        feedback.append( "Avoid sequences like '123' or 'abc'.")
    else:
        score += 1
    # Strength feedback
    strength = (StrengthLevel.STRONG if score >= 6 else
                StrengthLevel.MODERATE if score >= 4 else
                StrengthLevel.WEAK)
    return strength.value, feedback

# Example usage
password = input("Enter a password: ")
strength, suggestions = password_strength(password)
print(f"Password Strength: {strength}")
if suggestions:
    print("Suggestions:")
    for suggestion in suggestions:
        print(f" - {suggestion}")
