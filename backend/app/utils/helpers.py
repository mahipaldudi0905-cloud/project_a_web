import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional


def generate_random_string(length: int = 10) -> str:
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_otp(length: int = 6) -> str:
    """Generate OTP"""
    return ''.join(random.choices(string.digits, k=length))


def get_date_after_days(days: int) -> datetime:
    """Get date after specified days"""
    return datetime.now(timezone.utc) + timedelta(days=days)


def is_date_expired(date: datetime) -> bool:
    """Check if date has expired"""
    return datetime.now(timezone.utc) > date


def format_currency(amount: float, currency: str = "INR") -> str:
    """Format amount as currency"""
    currencies = {
        "INR": "₹",
        "USD": "$",
        "EUR": "€"
    }
    
    symbol = currencies.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def calculate_bid_increment(base_amount: float, percentage: float = 5) -> float:
    """Calculate bid increment"""
    return base_amount + (base_amount * percentage / 100)


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone format"""
    import re
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None


def truncate_string(text: str, length: int = 50) -> str:
    """Truncate string to specified length"""
    if len(text) > length:
        return text[:length-3] + "..."
    return text


def paginate_query(items: list, offset: int = 0, limit: int = 20) -> tuple:
    """Paginate a list of items"""
    total = len(items)
    start = offset
    end = offset + limit
    
    return items[start:end], total
