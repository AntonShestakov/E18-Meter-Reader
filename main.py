#!/usr/bin/env python3
"""
E18 Meter Reader Telegram Bot
Main entry point for the bot application.
Menu structure per design.md § Menu Structure.
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

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
            await update.effective_message.reply_text(
                "An error occurred while processing your request. Please try again."
            )
        except TelegramError as e:
            logger.error(f"Failed to send error message: {e}")


def create_menu_for_role(role: str = None) -> InlineKeyboardMarkup:
    """
    Create role-based menu per design.md § Menu Structure.

    Args:
        role: User role ('tenant', 'grayhound', 'administrator', or None for new user)

    Returns:
        InlineKeyboardMarkup with role-appropriate buttons

    Notes:
        - New user (role=None): Request for Meter Submeeting, About Bot
        - Tenant: Submit Reading, View Own Readings/Chart, Request for Meter Submeeting, About Bot
        - Grayhound: Submit Reading, Export Readings (CSV), View Readings/Chart, Request for Meter Submeeting, About Bot
        - Administrator: Submit Reading, Export Readings (CSV), View Own Readings/Chart, Requests,
                         Assign/Revoke Roles, Add/Deactivate Users, Manage Apartment List, About Bot
    """

    keyboard = []

    if role is None:
        # New user menu (no roles assigned)
        keyboard = [
            [
                InlineKeyboardButton(
                    "📋 Request for Meter Submeeting",
                    callback_data="request_submeeting",
                )
            ],
            [InlineKeyboardButton("ℹ️ About Bot", callback_data="about_bot")],
        ]

    elif role == "tenant":
        # Tenant menu
        keyboard = [
            [InlineKeyboardButton("📊 Submit Reading", callback_data="submit_reading")],
            [
                InlineKeyboardButton(
                    "📈 View Own Readings / Chart", callback_data="view_own_readings"
                )
            ],
            [
                InlineKeyboardButton(
                    "📋 Request for Meter Submeeting",
                    callback_data="request_submeeting",
                )
            ],
            [InlineKeyboardButton("ℹ️ About Bot", callback_data="about_bot")],
        ]

    elif role == "grayhound":
        # Grayhound menu
        keyboard = [
            [InlineKeyboardButton("📊 Submit Reading", callback_data="submit_reading")],
            [
                InlineKeyboardButton(
                    "📥 Export Readings (CSV)", callback_data="export_readings"
                )
            ],
            [
                InlineKeyboardButton(
                    "📈 View Readings / Chart", callback_data="view_readings"
                )
            ],
            [
                InlineKeyboardButton(
                    "📋 Request for Meter Submeeting",
                    callback_data="request_submeeting",
                )
            ],
            [InlineKeyboardButton("ℹ️ About Bot", callback_data="about_bot")],
        ]

    elif role == "administrator":
        # Administrator menu (highest privilege)
        keyboard = [
            [InlineKeyboardButton("📊 Submit Reading", callback_data="submit_reading")],
            [
                InlineKeyboardButton(
                    "📥 Export Readings (CSV)", callback_data="export_readings"
                )
            ],
            [
                InlineKeyboardButton(
                    "📈 View Own Readings / Chart", callback_data="view_own_readings"
                )
            ],
            [InlineKeyboardButton("📬 Requests", callback_data="view_requests")],
            [
                InlineKeyboardButton(
                    "👥 Assign / Revoke Roles", callback_data="manage_roles"
                )
            ],
            [
                InlineKeyboardButton(
                    "➕ Add / Deactivate Users", callback_data="manage_users"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Manage Apartment List", callback_data="manage_apartments"
                )
            ],
            [InlineKeyboardButton("ℹ️ About Bot", callback_data="about_bot")],
        ]

    return InlineKeyboardMarkup(keyboard)


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

    menu = create_menu_for_role(role=user_role)

    await update.message.reply_text(
        "Welcome to E18 Meter Reader Bot!\n\n" "Please select an option below.",
        reply_markup=menu,
    )


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
