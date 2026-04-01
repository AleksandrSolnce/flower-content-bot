import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CARD_NUMBER = os.getenv('CARD_NUMBER')
CARD_HOLDER = os.getenv('CARD_HOLDER')

PRODUCTS = {
    "flowers": {"name": "50 постов для цветочного магазина", "price": 590, "file": "files/flowers.pdf"},
    "weekend": {"name": "5 постов для выходных", "price": 100, "file": "files/weekend.pdf"}
}