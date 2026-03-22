import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# создаём клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    prompt = f"""
Ты мой личный ассистент.

Проанализируй сообщение и ответь:
1. Насколько оно важно (1–10)
2. Кратко суть
3. Предложи ответ от моего имени (вежливо, уверенно, без лишнего)

Сообщение:
{user_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content

    await update.message.reply_text(reply)


# запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Бот запущен 🚀")
    app.run_polling()
