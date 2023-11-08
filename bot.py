#!/usr/bin/env python
# pylint: disable=unused-argument


import logging
import os

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from stock_quote import fetch_us_quote
from dalle import prompt, gen_mood_pic

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def try_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /try is issued."""

    quote = await fetch_us_quote()
    prompt_text = f'{prompt(quote.changesPercentage)}  embedding the text "{quote.changesPercentageStr}".'
    await update.message.reply_text(
        f"""
    NAME: {quote.name}  
    SYMBOL: {quote.symbol}  
    CHANGE: {quote.changesPercentageStr} 
    PROMPT: {prompt_text}
    """
    )

    imgs = await gen_mood_pic(prompt_text)
    for img in imgs:
        await update.message.reply_text(img)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    bot_token = os.getenv("TG_BOT_TOKEN")

    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("try", try_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
