from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.users_data import add_user, select_user, update_lang, count_user
from keyboard.inline import select_lang, create_web_app_keyboard
from lang import LANGUAGE_MESSAGES

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    user_info = message.from_user
    users = await select_user(user_id=user_info.id)
    
    if not users:
        add = await add_user(
            user_id=user_info.id,
            full_name=user_info.full_name,
            lang='uz'
        )
        
    user = await select_user(user_id=user_info.id)
    
    welcome_text = LANGUAGE_MESSAGES.get(user.lang, LANGUAGE_MESSAGES['uz'])['start']
    
    web_app = await create_web_app_keyboard(user.lang)
    
    await message.answer(
            text=welcome_text,
            reply_markup=web_app,
            parse_mode="Markdown"
        )
    
@router.message(Command("set_lang"))
async def set_language_command(message: Message):
    user_info = message.from_user
    user = await select_user(user_id=user_info.id)
    keyboard = await select_lang(user.lang)
    await message.answer(
        text=LANGUAGE_MESSAGES.get(user.lang, LANGUAGE_MESSAGES['uz'])['lang_prompt'],
        reply_markup=keyboard
    )

# Inline tugma bosilganida tilni yangilash
@router.callback_query(lambda call: call.data.startswith("lang:"))
async def update_lang_callback(call: CallbackQuery):
    # Tanlangan tilni ajratib olish
    new_lang = call.data.split(":")[1]
    user_info = call.from_user
    user = await select_user(user_id=user_info.id)

    # Foydalanuvchi tilini yangilash
    await update_lang(user_id=user_info.id, new_lang=new_lang)

    # Yangi xabar matnini tayyorlash
    chosen_message = LANGUAGE_MESSAGES.get(new_lang, LANGUAGE_MESSAGES['uz'])['chosen']
    lang_prompt_message = LANGUAGE_MESSAGES.get(new_lang, LANGUAGE_MESSAGES['uz'])['lang_prompt']

    # Xabarni yangilashdan oldin eski matn bilan taqqoslash
    if call.message.text != lang_prompt_message:
        await call.message.edit_text(
            text=lang_prompt_message,
            reply_markup=await select_lang(new_lang)  # Tanlangan til uchun klaviatura
        )
    
    # Foydalanuvchiga xabarni tasdiqlash
    await call.answer(text=chosen_message)

        
        
@router.message(Command('stat'))
async def stat(message: Message):
    user_count = await count_user()
    await message.answer(text = f"Jami foydalanuvchilar soni: {user_count}")
    
