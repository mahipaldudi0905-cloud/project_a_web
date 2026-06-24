from typing import List
from app.core.constants import UserRole


# Define role-based permissions
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        "create_auction",
        "edit_auction",
        "delete_auction",
        "close_auction",
        "view_all_users",
        "manage_users",
        "manage_roles",
        "view_reports",
        "manage_payments",
        "manage_notifications",
    ],
    UserRole.MODERATOR: [
        "view_all_users",
        "manage_auctions",
        "manage_bids",
        "view_reports",
    ],
    UserRole.TEAM_OWNER: [
        "create_team",
        "edit_team",
        "place_bid",
        "view_auction",
        "withdraw_funds",
        "deposit_funds",
    ],
    UserRole.PLAYER: [
        "create_profile",
        "edit_profile",
        "view_auction",
        "view_wallet",
    ],
}


def has_permission(role: UserRole, permission: str) -> bool:
    """Check if role has specific permission"""
    return permission in ROLE_PERMISSIONS.get(role, [])


def get_role_permissions(role: UserRole) -> List[str]:
    """Get all permissions for a role"""
    return ROLE_PERMISSIONS.get(role, [])
