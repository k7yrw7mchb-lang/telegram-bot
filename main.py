import os
from openai import OpenAI
from telegram.ext import Updater, MessageHandler, Filters

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_message(update, context):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.choices[0].message.content

    update.message.reply_text(answer)


def main():
    updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)

    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    print("Бот запущен 🚀")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
