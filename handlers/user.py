from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from config import PRODUCTS, CARD_NUMBER, CARD_HOLDER, ADMIN_ID
from database import create_order
from keyboards import get_payment_keyboard, get_main_menu

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "🌸 Добро пожаловать в **Цветочный Контент**!\n\n"
        "Выберите товар:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: CallbackQuery):
    product_key = callback.data.split("_")[1]
    product = PRODUCTS.get(product_key)
    if not product:
        return

    order_id = await create_order(callback.from_user.id, product['name'], product['file'])

    payment_text = (
        f"💳 <b>Оплата заказа #{order_id}</b>\n\n"
        f"Товар: {product['name']}\n"
        f"Сумма: <b>{product['price']} ₽</b>\n\n"
        f"Переведите сумму на карту:\n"
        f"🏦 <code>{CARD_NUMBER}</code>\n"
        f"👤 {CARD_HOLDER}\n\n"
        f"После перевода нажмите кнопку ниже."
    )

    await callback.message.edit_text(payment_text, reply_markup=get_payment_keyboard(order_id), parse_mode="HTML")

@router.callback_query(F.data.startswith("paid_"))
async def process_paid_notify(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])
    admin_text = (
        f"🔔 <b>Новая оплата!</b>\n"
        f"Заказ #{order_id}\n"
        f"Пользователь: {callback.from_user.username} ({callback.from_user.id})\n"
        f"Нажмите /confirm {order_id} для выдачи товара."
    )
    try:
        await callback.bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
        await callback.answer("Заявка отправлена администратору! Ожидайте подтверждения.")
    except Exception:
        await callback.answer("Ошибка отправки админу. Напишите в поддержку.")
