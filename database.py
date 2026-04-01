import aiosqlite

DB_NAME = 'shop.db'

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_name TEXT,
                file_path TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def create_order(user_id, product_name, file_path):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            'INSERT INTO orders (user_id, product_name, file_path) VALUES (?, ?, ?)',
            (user_id, product_name, file_path)
        )
        await db.commit()
        return cursor.lastrowid

async def get_order(order_id):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        return await cursor.fetchone()

async def confirm_order(order_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE orders SET status = ? WHERE id = ?', ('paid', order_id))
        await db.commit()

async def get_pending_orders():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT * FROM orders WHERE status = ?', ('pending',))
        return await cursor.fetchall()