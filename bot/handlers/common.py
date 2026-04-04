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
from bot.handlers.decorators import log_handler

logger = logging.getLogger(__name__)


@log_handler()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start command — display welcome message and role-based menu.

    Flow:
    1. Check if user exists in database
    2. If new user: register user, display new user menu
    3. If existing: query active roles and show appropriate menu
    4. Highest privilege role menu wins if multiple roles
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started bot")

    try:
        # Get services from application context
        users_repo = context.bot_data.get("users_repo")
        role_service = context.bot_data.get("role_service")

        if not users_repo or not role_service:
            logger.error("Database services not initialized")
            await update.message.reply_text(texts.UNEXPECTED_ERROR)
            return

        # Check if user exists
        existing_user = await users_repo.get_by_telegram_id(user.id)
        if not existing_user:
            # Create new user
            await users_repo.create_user(
                user_id=user.id,
                username=user.username,
                full_name=user.first_name,
            )
            logger.info(f"New user registered: {user.id} ({user.username})")
            role = None  # New user has no role
        else:
            # Get highest privilege role for existing user
            role = await role_service.get_highest_privilege_role(user.id)
            logger.info(f"User {user.id} has role: {role}")

        # Build and display menu based on role
        menu_keyboard = keyboards.build_main_menu_for_role(role)

        await update.message.reply_text(
            texts.START_MESSAGE,
            reply_markup=menu_keyboard,
        )

    except Exception as e:
        logger.error(f"Error in start handler: {e}", exc_info=True)
        await update.message.reply_text(texts.UNEXPECTED_ERROR)


@log_handler()
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help command — display help message.
    """
    await update.message.reply_text(texts.HELP_MESSAGE)


@log_handler()
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /cancel command — cancel current operation and return to main menu.
    """
    user = update.effective_user
    role = None

    try:
        # Try to get user's actual role
        role_service = context.bot_data.get("role_service")
        if role_service:
            role = await role_service.get_highest_privilege_role(user.id)
    except Exception as e:
        logger.warning(f"Failed to get role for user {user.id}: {e}")

    menu_keyboard = keyboards.build_main_menu_for_role(role)
    await update.message.reply_text(
        "Cancelled. Back to main menu:",
        reply_markup=menu_keyboard,
    )


@log_handler(include_context=False)
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
