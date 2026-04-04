"""
Common handlers for E18 Meter Reader Bot.

Shared handlers used across all roles:
- /start command
- /help command
- /cancel command
- Error handler
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot import texts, keyboards

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start command — display welcome message and role-based menu.

    Flow:
    1. Check if user exists in database
    2. If new user: display new user menu (request access)
    3. If existing: query active roles and show appropriate menu
    4. Highest privilege role menu wins if multiple roles
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started bot")

    # TODO: Query database for user roles
    # For now, use None (new user menu)
    role = None

    menu_keyboard = keyboards.build_main_menu_for_role(role)

    await update.message.reply_text(
        texts.START_MESSAGE,
        reply_markup=menu_keyboard,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help command — display help message.
    """
    await update.message.reply_text(texts.HELP_MESSAGE)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /cancel command — cancel current operation and return to main menu.
    """
    menu_keyboard = keyboards.build_main_menu_for_role(None)  # TODO: Get actual role
    await update.message.reply_text(
        "Cancelled. Back to main menu:",
        reply_markup=menu_keyboard,
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors during bot operation.

    Logs full traceback and sends user-friendly error message.
    """
    logger.error(
        f"Exception while handling an update: {context.error}", exc_info=context.error
    )

    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(texts.UNEXPECTED_ERROR)
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
