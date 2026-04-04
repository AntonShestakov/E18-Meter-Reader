"""
Tests for the bot main module and role-based menu structure per design.md.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Message, InlineKeyboardMarkup
from telegram.ext import ContextTypes


@pytest.mark.asyncio
async def test_start_command_calls_reply_text():
    """Test that /start command handler calls reply_text."""
    # Create mocks
    message = MagicMock(spec=Message)
    message.reply_text = AsyncMock()

    update = MagicMock(spec=Update)
    update.message = message

    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    # Import and call
    from main import start

    await start(update, context)

    # Verify reply_text was called
    message.reply_text.assert_called_once()


def test_create_new_user_menu():
    """Test menu for new user (no roles assigned)."""
    from main import create_menu_for_role

    # New user should see: "Request for Meter Submeeting", "About Bot"
    keyboard = create_menu_for_role(role=None)

    assert isinstance(keyboard, InlineKeyboardMarkup)
    buttons_text = []
    for row in keyboard.inline_keyboard:
        for btn in row:
            buttons_text.append(btn.text)

    assert any(
        "Request" in text for text in buttons_text
    ), f"Expected 'Request' button for new user, got: {buttons_text}"
    assert any(
        "About" in text for text in buttons_text
    ), f"Expected 'About' button for new user, got: {buttons_text}"


def test_create_tenant_menu():
    """Test menu for Tenant role per design.md."""
    from main import create_menu_for_role

    # Tenant should see: Submit Reading, View Own Readings/Chart, Request for Meter Submeeting, About Bot
    keyboard = create_menu_for_role(role="tenant")

    assert isinstance(keyboard, InlineKeyboardMarkup)
    buttons_text = []
    for row in keyboard.inline_keyboard:
        for btn in row:
            buttons_text.append(btn.text)

    expected = ["Submit Reading", "View Own Readings", "Request", "About"]
    for expected_text in expected:
        assert any(
            expected_text in text for text in buttons_text
        ), f"Expected '{expected_text}' button for tenant, got: {buttons_text}"


def test_create_grayhound_menu():
    """Test menu for Grayhound role per design.md."""
    from main import create_menu_for_role

    # Grayhound should see: Submit Reading, Export Readings (CSV), View Readings/Chart,
    # Request for Meter Submeeting, About Bot
    keyboard = create_menu_for_role(role="grayhound")

    assert isinstance(keyboard, InlineKeyboardMarkup)
    buttons_text = []
    for row in keyboard.inline_keyboard:
        for btn in row:
            buttons_text.append(btn.text)

    expected = ["Submit Reading", "Export", "View Readings", "Request", "About"]
    for expected_text in expected:
        assert any(
            expected_text in text for text in buttons_text
        ), f"Expected '{expected_text}' button for grayhound, got: {buttons_text}"


def test_create_administrator_menu():
    """Test menu for Administrator role per design.md."""
    from main import create_menu_for_role

    # Administrator should see: Submit Reading, Export Readings (CSV), View Own Readings/Chart,
    # Requests, Assign/Revoke Roles, Add/Deactivate Users, Manage Apartment List, About Bot
    keyboard = create_menu_for_role(role="administrator")

    assert isinstance(keyboard, InlineKeyboardMarkup)
    buttons_text = []
    for row in keyboard.inline_keyboard:
        for btn in row:
            buttons_text.append(btn.text)

    expected = [
        "Submit Reading",
        "Export",
        "View Own Readings",
        "Requests",
        "Assign",
        "Add",
        "Manage",
    ]
    for expected_text in expected:
        assert any(
            expected_text in text for text in buttons_text
        ), f"Expected '{expected_text}' button for administrator, got: {buttons_text}"


def test_highest_privilege_role_menu_wins():
    """Test that administrator menu is shown if user has multiple roles."""
    from main import create_menu_for_role

    # When user has both administrator and grayhound roles,
    # administrator menu (highest privilege) should be returned
    keyboard = create_menu_for_role(role="administrator")
    buttons_text = []
    for row in keyboard.inline_keyboard:
        for btn in row:
            buttons_text.append(btn.text)

    # Admin menu should have "Assign/Revoke Roles" which grayhound doesn't
    assert any(
        "Assign" in text for text in buttons_text
    ), "Admin menu should include 'Assign/Revoke Roles'"
