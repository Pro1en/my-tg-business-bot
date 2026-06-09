import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from groq import Groq

# --- НАЛАШТУВАННЯ (ВСТАВ СВОЇ ДАНІ СЮДИ) ---
TELEGRAM_TOKEN = "8852008619:AAE92aJk9rhCmLZPyAUDomcWEqo1qC65U0c"
GROQ_API_KEY = "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"

# Інструкція для ШІ (можеш змінити текст під свій бізнес)
SYSTEM_INSTRUCTION = (
    "Ти — крутий і привітний ШІ-менеджер для бізнесу. "
    "Відповідай коротко, чітко, з гумором та виключно українською мовою. "
    "Твоя ціль — допомогти клієнту та підтримати діалог."
)
# ------------------------------------------

# Ініціалізація ШІ Groq
ai_client = Groq(api_key=GROQ_API_KEY)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Обробник повідомлень для Telegram Business
@dp.business_message()
async def handle_business_message(message: types.Message):
    # Якщо повідомлення відправив ти сам — бот його ігнорує
    if message.from_user.id == bot.id:
        return

    text_from_client = message.text
    if not text_from_client:
        return

    try:
        # Запит до безкоштовної моделі Llama 3
        chat_completion = ai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": text_from_client}
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.7,
        )
        
        # Отримуємо відповідь від ШІ
        bot_response = chat_completion.choices[0].message.content
        
        # Відправляємо її клієнту в бізнес-чат
        await message.answer(bot_response)
        
    except Exception as e:
        print(f"Помилка ШІ: {e}")

async def main():
    print("🚀 Бот успішно запущений і готовий відповідати в Telegram Business 24/7!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())