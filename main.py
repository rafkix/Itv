import asyncio
from data import config
from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.start import router
from database.users_data import Base, engine


# Bot va dispatcher sozlamalari
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


# Bazani va jadvalni yaratish
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Asosiy bot ishga tushiruvchi funksiya
async def main():
    # await init_db()  # Bazani yaratish
    dp.include_router(router) 
    await bot.send_message(chat_id=config.ADMINS[0], text='bot ishga tushdi')
    await dp.start_polling(bot, session=AsyncSession()) # Botni ishga tushirish

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print('run')
    except KeyboardInterrupt:
        print('stoped')
