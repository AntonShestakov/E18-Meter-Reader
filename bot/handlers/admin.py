"""
Administrator role handlers for E18 Meter Reader Bot.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display administrator menu."""
    # TODO: Implement admin menu with buttons for:
    # - Manage users
    # - Assign roles
    # - View readings
    # - Export CSV
    pass
