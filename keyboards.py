from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    kb = [
        [InlineKeyboardButton(text="🌸 50 постов (590₽)", callback_data="buy_flowers")],
        [InlineKeyboardButton(text="☕ 5 постов (100₽)", callback_data="buy_weekend")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def get_payment_keyboard(order_id):
    kb = [[InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"paid_{order_id}")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def get_admin_orders_keyboard(orders):
    kb = []
    for order in orders:
        kb.append([InlineKeyboardButton(
            text=f"Заказ #{order['id']} - {order['product_name']}", 
            callback_data=f"admin_view_{order['id']}"
        )])
    if not kb:
        kb.append([InlineKeyboardButton(text="Нет активных заказов", callback_data="none")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def get_confirm_keyboard(order_id):
    kb = [[InlineKeyboardButton(text="✅ Подтвердить и выдать", callback_data=f"confirm_{order_id}")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)