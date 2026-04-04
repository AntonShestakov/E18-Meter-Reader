"""
Handlers package — Telegram update handlers.

Handlers process incoming Telegram updates and orchestrate services/repositories.
Each handler module corresponds to a user role or feature area.
"""

from bot.handlers import common, admin, tenant, grayhound

__all__ = ["common", "admin", "tenant", "grayhound"]