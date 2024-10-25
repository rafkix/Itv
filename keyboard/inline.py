from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

async def create_web_app_keyboard(lang_code):
    keyboard_builder = InlineKeyboardBuilder()

    # Define the web app URLs for each language
    web_app_urls = {
        'uz': 'https://itv.uz/uz',  # Uzbek
        'ru': 'https://itv.uz/ru',  # Russian
        'en': 'https://itv.uz/en'   # English
    }

    # Create button only for the specified language
    if lang_code in web_app_urls:
        url = web_app_urls[lang_code]
        button = InlineKeyboardButton(
            text=f"ITv - Web App ({lang_code})",
            web_app={'url': url}  # Specify the URL for the web app
        )
        keyboard_builder.add(button)

    return keyboard_builder.as_markup()

async def select_lang(lang_code):
    """
    Create a keyboard for selecting languages, with a checkmark for the current language.
    """
    # Define the language buttons
    button_texts = {
        'uz': '🇺🇿 O\'zbekcha',
        'ru': '🇷🇺 Русский',
        'en': '🇬🇧 English'
    }

    # Use InlineKeyboardBuilder to build the keyboard
    keyboard_builder = InlineKeyboardBuilder()

    # Create buttons with checkmark for selected language
    for code, text in button_texts.items():
        display_text = f"{text} {'✅' if code == lang_code else ''}"
        keyboard_builder.add(InlineKeyboardButton(text=display_text, callback_data=f"lang:{code}"))

    # Adjust the keyboard to display two buttons per row
    keyboard_builder.adjust(2)
    
    return keyboard_builder.as_markup()