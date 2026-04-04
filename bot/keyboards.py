"""
Inline keyboard builders for E18 Meter Reader Bot.

Constructs role-aware menus and input interfaces using InlineKeyboardMarkup.
"""

from typing import Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot import texts


def build_main_menu_for_role(role: Optional[str]) -> InlineKeyboardMarkup:
    """
    Build main menu keyboard for a given role.

    Args:
        role: One of None, 'tenant', 'grayhound', 'administrator'

    Returns:
        InlineKeyboardMarkup with role-appropriate buttons
    """
    buttons = []

    if role is None:
        # New user menu
        buttons = [
            [
                InlineKeyboardButton(
                    texts.BUTTON_REQUEST_SUBMEETING, callback_data="request_submeeting"
                )
            ],
            [InlineKeyboardButton(texts.BUTTON_ABOUT, callback_data="about")],
        ]
    elif role == "tenant":
        # Tenant menu
        buttons = [
            [
                InlineKeyboardButton(
                    texts.BUTTON_SUBMIT_READING, callback_data="submit_reading"
                )
            ],
            [
                InlineKeyboardButton(
                    texts.BUTTON_VIEW_READINGS, callback_data="view_readings"
                )
            ],
            [
                InlineKeyboardButton(
                    texts.BUTTON_REQUEST_SUBMEETING, callback_data="request_submeeting"
                )
            ],
            [InlineKeyboardButton(texts.BUTTON_ABOUT, callback_data="about")],
        ]
    elif role == "grayhound":
        # Grayhound menu
        buttons = [
            [
                InlineKeyboardButton(
                    texts.BUTTON_SUBMIT_READING, callback_data="submit_reading"
                )
            ],
            [InlineKeyboardButton(texts.BUTTON_EXPORT_CSV, callback_data="export_csv")],
            [
                InlineKeyboardButton(
                    texts.BUTTON_VIEW_READINGS, callback_data="view_readings"
                )
            ],
            [
                InlineKeyboardButton(
                    texts.BUTTON_REQUEST_SUBMEETING, callback_data="request_submeeting"
                )
            ],
            [InlineKeyboardButton(texts.BUTTON_ABOUT, callback_data="about")],
        ]
    elif role == "administrator":
        # Administrator menu (full access)
        buttons = [
            [
                InlineKeyboardButton(
                    texts.BUTTON_SUBMIT_READING, callback_data="submit_reading"
                )
            ],
            [InlineKeyboardButton(texts.BUTTON_EXPORT_CSV, callback_data="export_csv")],
            [
                InlineKeyboardButton(
                    texts.BUTTON_VIEW_READINGS, callback_data="view_readings"
                )
            ],
            [
                InlineKeyboardButton(
                    texts.BUTTON_REQUESTS, callback_data="view_requests"
                )
            ],
            [
                InlineKeyboardButton(
                    texts.BUTTON_ASSIGN_ROLES, callback_data="assign_roles"
                )
            ],
            [
                InlineKeyboardButton(
                    texts.BUTTON_MANAGE_USERS, callback_data="manage_users"
                )
            ],
            [
                InlineKeyboardButton(
                    texts.BUTTON_MANAGE_APARTMENTS, callback_data="manage_apartments"
                )
            ],
            [InlineKeyboardButton(texts.BUTTON_ABOUT, callback_data="about")],
        ]

    return InlineKeyboardMarkup(buttons)


def build_numeric_keypad() -> InlineKeyboardMarkup:
    """
    Build numeric input keypad for meter readings.

    Layout:
        1 2 3
        4 5 6
        7 8 9
        0 Clear
        Submit Cancel

    Returns:
        InlineKeyboardMarkup with numeric buttons
    """
    buttons = [
        [
            InlineKeyboardButton(texts.BUTTON_1, callback_data="input_1"),
            InlineKeyboardButton(texts.BUTTON_2, callback_data="input_2"),
            InlineKeyboardButton(texts.BUTTON_3, callback_data="input_3"),
        ],
        [
            InlineKeyboardButton(texts.BUTTON_4, callback_data="input_4"),
            InlineKeyboardButton(texts.BUTTON_5, callback_data="input_5"),
            InlineKeyboardButton(texts.BUTTON_6, callback_data="input_6"),
        ],
        [
            InlineKeyboardButton(texts.BUTTON_7, callback_data="input_7"),
            InlineKeyboardButton(texts.BUTTON_8, callback_data="input_8"),
            InlineKeyboardButton(texts.BUTTON_9, callback_data="input_9"),
        ],
        [
            InlineKeyboardButton(texts.BUTTON_0, callback_data="input_0"),
            InlineKeyboardButton(texts.BUTTON_CLEAR, callback_data="input_clear"),
        ],
        [
            InlineKeyboardButton(texts.BUTTON_SUBMIT, callback_data="reading_submit"),
            InlineKeyboardButton(texts.BUTTON_CANCEL, callback_data="reading_cancel"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def build_confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Build yes/no confirmation keyboard.

    Returns:
        InlineKeyboardMarkup with Confirm/Deny buttons
    """
    buttons = [
        [
            InlineKeyboardButton(texts.BUTTON_CONFIRM, callback_data="confirm_yes"),
            InlineKeyboardButton(texts.BUTTON_DENY, callback_data="confirm_no"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def build_back_button() -> InlineKeyboardMarkup:
    """
    Build single back button.

    Returns:
        InlineKeyboardMarkup with Back button
    """
    buttons = [
        [InlineKeyboardButton(texts.BUTTON_BACK, callback_data="menu_back")],
    ]
    return InlineKeyboardMarkup(buttons)


def build_apartment_selector(apartments: list) -> InlineKeyboardMarkup:
    """
    Build apartment selection keyboard.

    Args:
        apartments: List of apartment objects (with 'id' and 'number' attributes)

    Returns:
        InlineKeyboardMarkup with apartment buttons + Back
    """
    buttons = []
    for apt in apartments:
        buttons.append(
            [
                InlineKeyboardButton(
                    f"Apt. {apt.number}", callback_data=f"select_apartment_{apt.id}"
                )
            ]
        )
    buttons.append([InlineKeyboardButton(texts.BUTTON_BACK, callback_data="menu_back")])
    return InlineKeyboardMarkup(buttons)
