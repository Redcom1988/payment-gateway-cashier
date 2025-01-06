import re
import random
import string

def valid_phone(phn):
    return bool(re.match(r"[789]\d{9}$", phn))

def random_id(prefix, length=7):
    digits = string.digits
    random_str = ''.join(random.choice(digits) for _ in range(length-len(prefix)))
    return f"{prefix}{random_str}"

def format_currency(amount):
    return f"₹{amount:.2f}"