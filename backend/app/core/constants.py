from enum import Enum


class UserRole(str, Enum):
    """User roles in the system"""
    ADMIN = "admin"
    TEAM_OWNER = "team_owner"
    PLAYER = "player"
    MODERATOR = "moderator"


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    PENDING_VERIFICATION = "pending_verification"


class AuctionStatus(str, Enum):
    """Auction status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    LIVE = "live"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class BidStatus(str, Enum):
    """Bid status"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class TransactionType(str, Enum):
    """Wallet transaction type"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    AUCTION_BID = "auction_bid"
    AUCTION_WIN = "auction_win"
    REFUND = "refund"


class TransactionStatus(str, Enum):
    """Transaction status"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaymentGateway(str, Enum):
    """Payment gateway providers"""
    RAZORPAY = "razorpay"
    STRIPE = "stripe"
    CASHFREE = "cashfree"


class NotificationType(str, Enum):
    """Notification types"""
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    IN_APP = "in_app"


class NotificationEvent(str, Enum):
    """Notification events"""
    AUCTION_STARTED = "auction_started"
    AUCTION_CLOSED = "auction_closed"
    BID_PLACED = "bid_placed"
    BID_OUTBID = "bid_outbid"
    AUCTION_WON = "auction_won"
    AUCTION_LOST = "auction_lost"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    ACCOUNT_VERIFIED = "account_verified"
    PASSWORD_CHANGED = "password_changed"


# Default values
DEFAULT_PAGINATION_LIMIT = 20
MAX_PAGINATION_LIMIT = 100
DEFAULT_PAGINATION_OFFSET = 0

# Bid constraints
MIN_BID_INCREMENT_PERCENTAGE = 5  # 5% minimum increment
AUTO_EXTENSION_THRESHOLD_SECONDS = 60  # Auto-extend if bid within 1 minute of end
AUTO_EXTENSION_DURATION_SECONDS = 120  # Extend auction by 2 minutes

# Wallet constraints
MIN_WITHDRAWAL_AMOUNT = 100  # Minimum withdrawal amount
MAX_WITHDRAWAL_AMOUNT = 1000000  # Maximum withdrawal amount
