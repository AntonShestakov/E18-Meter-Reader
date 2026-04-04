"""
Tenant role handlers for E18 Meter Reader Bot.
"""

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.decorators import log_handler


@log_handler()
async def tenant_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display tenant menu."""
    # TODO: Implement tenant menu with buttons for:
    # - Submit meter reading
    # - View own readings
    pass
