"""
Decorators for Telegram bot handlers with comprehensive logging.

Provides:
- Handler execution logging (start, end, duration)
- User/update data extraction and logging
- Context information (optional)
- Error handling with detailed traceback
"""

import logging
import time
from functools import wraps
from typing import Optional, Any, Callable
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def _extract_user_info(update: Optional[Any]) -> dict:
    """Extract relevant user information from Update object."""
    info = {}
    if not update:
        return info

    # Extract from effective_user
    if hasattr(update, "effective_user") and update.effective_user:
        user = update.effective_user
        info["user_id"] = user.id
        info["username"] = user.username
        info["first_name"] = user.first_name
        info["last_name"] = user.last_name

    # Extract from effective_chat
    if hasattr(update, "effective_chat") and update.effective_chat:
        chat = update.effective_chat
        info["chat_id"] = chat.id
        info["chat_type"] = chat.type

    # Extract from message
    if hasattr(update, "message") and update.message:
        msg = update.message
        info["message_text"] = msg.text[:50] if msg.text else None  # First 50 chars
        info["message_id"] = msg.message_id

    # Extract from callback_query
    if hasattr(update, "callback_query") and update.callback_query:
        cbq = update.callback_query
        info["callback_data"] = cbq.data
        info["callback_id"] = cbq.id

    return info


def log_handler(include_context: bool = False, include_update: bool = True) -> Callable:
    """
    Decorator for Telegram bot handlers with comprehensive logging.

    Logs:
    - Handler function name
    - Start event with timestamp
    - User/chat information from Update
    - Execution duration
    - End event with result or error
    - Optional: Full Context details

    Args:
        include_context: If True, log Context object details (careful with secrets)
        include_update: If True, log extracted Update data (default True)

    Example:
        @log_handler()
        async def my_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text("Hello!")

        @log_handler(include_context=True)
        async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            pass
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            update: Optional[Update],
            context: Optional[ContextTypes.DEFAULT_TYPE] = None,
        ) -> Any:
            handler_name = func.__name__
            start_time = time.time()

            # Extract user/chat info
            user_info = _extract_user_info(update) if include_update else {}

            # Log start
            logger.info(
                f"[{handler_name}] START",
                extra={"user_data": user_info} if user_info else {},
            )
            if user_info:
                logger.debug(f"[{handler_name}] User info: {user_info}")

            # Log context info if requested
            if include_context and context:
                context_info = {
                    "user_data": dict(context.user_data) if context.user_data else {},
                    "chat_data": dict(context.chat_data) if context.chat_data else {},
                    "args": context.args,
                }
                logger.debug(f"[{handler_name}] Context: {context_info}")

            try:
                # Execute handler
                result = await func(update, context)

                # Log end
                duration = time.time() - start_time
                logger.info(
                    f"[{handler_name}] END (duration: {duration:.3f}s, result: {result})"
                )

                return result

            except Exception as e:
                # Log error
                duration = time.time() - start_time
                logger.error(
                    f"[{handler_name}] ERROR after {duration:.3f}s: {type(e).__name__}: {str(e)}",
                    exc_info=True,
                )
                raise

        return wrapper

    return decorator
