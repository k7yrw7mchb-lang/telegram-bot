import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# OpenAI клиент
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты личный ассистент. Отвечай кратко и по делу."},
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.choices[0].message.content

    await update.message.reply_text(answer)


def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Бот запущен 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
