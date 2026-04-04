#!/usr/bin/env python3
"""
E18 Meter Reader Telegram Bot
Main entry point for the bot application.
Menu structure per design.md § Menu Structure.
"""

import logging
import os
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError
from bot import texts
from bot.handlers.common import start
from bot.database import DatabaseManager
from bot.repositories.users import UsersRepository
from bot.repositories.roles import UserRolesRepository
from bot.services.roles import RoleService

# Load environment variables from .env.local (local development)
load_dotenv(dotenv_path=".env.local")

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Suppress verbose httpx logging (HTTP client used by Telegram API)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to notify the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(texts.UNEXPECTED_ERROR)
        except TelegramError as e:
            logger.error(f"Failed to send error message: {e}")


async def post_init(application: Application) -> None:
    """Run on application startup — initialize database and services."""
    logger.info("Bot initializing...")

    try:
        # Initialize database
        db_manager = DatabaseManager()
        await db_manager.init()
        logger.info("Database initialized")

        # Initialize repositories
        users_repo = UsersRepository()
        roles_repo = UserRolesRepository()

        # Initialize services
        role_service = RoleService(roles_repo, users_repo)

        # Store in application bot_data for handler access
        application.bot_data["db_manager"] = db_manager
        application.bot_data["users_repo"] = users_repo
        application.bot_data["roles_repo"] = roles_repo
        application.bot_data["role_service"] = role_service

        logger.info("Bot has started and is listening for commands")
    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}")
        raise


def main() -> None:
    """Start the bot."""
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    # Create application
    application = Application.builder().token(token).build()

    # Initialize bot_data dictionary for storing shared resources
    application.bot_data = {}

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
