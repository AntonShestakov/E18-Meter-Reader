#!/usr/bin/env python3
"""
E18 Meter Reader Telegram Bot
Main entry point for the bot application.
Menu structure per design.md § Menu Structure.
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError
from bot import texts
from bot.keyboards import build_main_menu_for_role

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to notify the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(texts.UNEXPECTED_ERROR)
        except TelegramError as e:
            logger.error(f"Failed to send error message: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.

    TODO: Integrate with DB to:
    1. Check if user exists
    2. Get user's active roles
    3. Select highest-privilege menu

    For now, shows new user menu as placeholder.
    """
    # TODO: Replace with actual DB user/role lookup
    user_role = None  # Placeholder: will be replaced with DB query

    menu = build_main_menu_for_role(role=user_role)

    await update.message.reply_text(texts.START_MESSAGE, reply_markup=menu)


async def post_init(application: Application) -> None:
    """Run on application startup."""
    logger.info("Bot has started and is listening for commands")


def main() -> None:
    """Start the bot."""
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    # Create application
    application = Application.builder().token(token).build()

    # Set startup handler
    application.post_init = post_init

    # Add handlers
    application.add_handler(CommandHandler("start", start))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start polling
    logger.info("Starting bot with polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
