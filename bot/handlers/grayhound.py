"""
Grayhound (building manager) role handlers for E18 Meter Reader Bot.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def grayhound_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display grayhound menu."""
    # TODO: Implement grayhound menu with buttons for:
    # - Submit reading for apartment
    # - View building readings
    # - Export CSV
    pass
