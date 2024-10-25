import aiosqlite
import asyncio
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, func, select
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLAlchemy uchun asosiy baza sinfi
Base = declarative_base()

# Users jadvali modeli
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, unique=True)
    full_name = Column(String, nullable=False)
    lang = Column(String, default="uz")
    user_time = Column(DateTime, default=datetime.utcnow)
    is_blocked = Column(Integer, default=0)  # 0 - faol, 1 - bloklangan

# SQLite ulanishi va sessiyalarni sozlash
DATABASE_URL = "sqlite+aiosqlite:///./users.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Baza va jadval yaratish
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Foydalanuvchini qo'shish
async def add_user(user_id, full_name, lang="uz"):
    async with async_session() as session:
        async with session.begin():
            new_user = User(user_id=user_id, full_name=full_name, lang=lang)
            session.add(new_user)
        await session.commit()

# Foydalanuvchi tilini yangilash
async def update_lang(user_id, new_lang):
    async with async_session() as session:
        async with session.begin():
            stmt = select(User).where(User.user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.lang = new_lang
                await session.commit()

# Foydalanuvchini tanlash
async def select_user(user_id):
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

# Har bir til bo'yicha foydalanuvchilar soni
async def count_lang(lang):
    async with async_session() as session:
        stmt = select(func.count(User.user_id)).where(User.lang == lang)
        result = await session.execute(stmt)
        return result.scalar()

# Foydalanuvchilar soni
async def count_user():
    async with async_session() as session:
        stmt = select(func.count(User.user_id))
        result = await session.execute(stmt)
        return result.scalar()

# Foydalanuvchini bloklash
async def block_user(user_id):
    async with async_session() as session:
        async with session.begin():
            stmt = select(User).where(User.user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.is_blocked = 1
                await session.commit()

# # Asosiy funksiyani chaqirish
# async def main():
#     await init_db()  # Bazani va jadvalni yaratish
#     await add_user(1, "John Doe", "en")  # Foydalanuvchini qo'shish
#     user = await select_user(1)
#     print(user.full_name, user.lang, user.user_time)  # Foydalanuvchini chiqarish
#     await update_lang(1, "uz")  # Foydalanuvchi tilini yangilash
#     lang_count = await count_lang("uz")  # Til bo'yicha foydalanuvchi soni
#     print("Uzbek tilidagi foydalanuvchilar soni:", lang_count)
#     user_count = await count_user()  # Jami foydalanuvchilar soni
#     print("Jami foydalanuvchilar soni:", user_count)
#     await block_user(1)  # Foydalanuvchini bloklash

# # Asinxron funksiyani ishga tushirish
# asyncio.run(main())
