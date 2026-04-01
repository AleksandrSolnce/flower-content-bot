from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from config import ADMIN_ID
from database import get_order, confirm_order, get_pending_orders
from keyboards import get_confirm_keyboard, get_admin_orders_keyboard
import os

router = Router()

@router.message(F.text == "/orders")
async def cmd_orders(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    orders = await get_pending_orders()
    if not orders:
        await message.answer("Нет активных заказов.")
        return
    await message.answer("📋 Активные заказы:", reply_markup=get_admin_orders_keyboard(orders))

@router.message(F.text.startswith("/confirm"))
async def cmd_confirm(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split()
        order_id = int(parts[1])
    except (IndexError, ValueError):
        await message.answer("Используйте: /confirm <ID заказа>")
        return

    order = await get_order(order_id)
    if not order:
        await message.answer("Заказ не найден.")
        return

    await confirm_order(order_id)
    file_path = order['file_path']
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            await message.bot.send_document(
                chat_id=order['user_id'],
                document=file,
                caption=f"✅ Оплата подтверждена!\nВаш товар: {order['product_name']}"
            )
        await message.answer(f"✅ Заказ #{order_id} выполнен. Файл отправлен.")
    else:
        await message.answer(f"❌ Ошибка: Файл {file_path} не найден на сервере.")

@router.callback_query(F.data.startswith("admin_view_"))
async def admin_view_order(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
    order_id = int(callback.data.split("_")[2])
    order = await get_order(order_id)
    if order:
        text = (
            f"📦 <b>Заказ #{order['id']}</b>\n"
            f"Пользователь: {order['user_id']}\n"
            f"Товар: {order['product_name']}\n"
            f"Статус: {order['status']}"
        )
        await callback.message.answer(text, reply_markup=get_confirm_keyboard(order_id), parse_mode="HTML")