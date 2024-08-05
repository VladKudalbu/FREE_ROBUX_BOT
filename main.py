from data import API_ID, API_HASH, BOT_TOKEN, start_message, bring_message
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from pyrogram import emoji
import asyncio

app = Client(name="FREE_ROBUX_BOT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

robuxes = {}

# buttons
btn_start = KeyboardButton("НАЧАТЬ😜")
btn_balance = KeyboardButton("БАЛАНС💰")
btn_bring_out = KeyboardButton("ВЫВЕСТИ РОБУКСЫ💸")
btn_support = KeyboardButton("ПОДДЕРЖКА🎧")
btn_click = KeyboardButton("КЛИК💎")
btn_back = KeyboardButton("Назад🔙")
btn_ready_bringout = KeyboardButton("ВЫВЕСТИ💸")

kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_start, btn_bring_out],
        [btn_support, btn_balance]
    ],
    resize_keyboard=True
)

kb_robuxes = ReplyKeyboardMarkup(
    keyboard=[
        [btn_click],
        [btn_balance, btn_support, btn_back]
    ],
    resize_keyboard=True
)

kb_balance = ReplyKeyboardMarkup(
    keyboard=[
        [btn_bring_out, btn_back],
        [btn_support]
    ],
    resize_keyboard=True
)

kb_bringout = ReplyKeyboardMarkup(
    keyboard=[
        [btn_ready_bringout]
    ],
    resize_keyboard=True
)

def button_filter(button):
    async def func(_, __, msg):
        return msg.text == button.text
    return filters.create(func, "ButtonFilter", button=button)

@app.on_message(filters.command('start'))
async def start_skam(client: Client, message: Message):
    await app.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJrK2avrNclRlx5V7yqcJnDLi4-7hG3AAI2IgAC8xwoSnNWDXYzRforNQQ')
    await message.reply_text(start_message, reply_markup=kb_main)

@app.on_message(filters.command("menu") | button_filter(btn_back))
async def menu(client: Client, message: Message):
    await message.reply_text("Успешно вернулись в меню✅", reply_markup=kb_main)

@app.on_message(filters.command('robux_start') | button_filter(btn_start))
async def robux_start(client: Client, message: Message):
    await app.send_sticker(message.chat.id, "CAACAgIAAxkBAAJrNWavtXBe4OkhZvsLU0pFwfhw_-sCAAKzTgAC0-i4S75V55QpBvw2NQQ")
    await message.reply_text("Чтобы начать зарабатывать робуксы нажимай кнопку 'КЛИК💎'", reply_markup=kb_robuxes)

@app.on_message(filters.command('balance') | button_filter(btn_balance))
async def balance(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in robuxes:
        robuxes[user_id] = 0
    await message.reply_text(f"Привет {message.from_user.first_name}👋 Расскажу тебе о счете твоих робуксов📊 Баланс Робуксов: {robuxes[user_id]}", reply_markup=kb_balance)

@app.on_message(filters.command('click') | button_filter(btn_click))
async def click(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in robuxes:
        robuxes[user_id] = 0
    robuxes[user_id] += 1
    await message.reply_text("+1 робукс к балансу✅", reply_markup=kb_robuxes)

@app.on_message(filters.command('bringout') | button_filter(btn_bring_out))
async def bringout(client: Client, message: Message):
    await message.reply_text(f"Приветсвую {message.from_user.first_name}👋 Хочешь вывести свои робуксы? Окей🤑/nНажми кнопку 'ВЫВЕСТИ💸' для подтверждения.", reply_markup=kb_bringout)

@app.on_message(filters.command('bringout_ready') | button_filter(btn_ready_bringout))
async def bringout_ready(client: Client, message: Message):
    await message.reply_text(bring_message, reply_markup=kb_main)

app.run()
