import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from settings import *
from details.handlers import start, text, button, document



app = Application.builder().token(BOT_TOKEN).build()



app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.PDF | filters.Document.DOCX | filters.Document.DOC, document))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))

if __name__ == "__main__":
    print("Pooling ishlayapti...")
    app.run_polling(
    allowed_updates=[Update.MESSAGE, Update.CALLBACK_QUERY],
    drop_pending_updates=True,
    )