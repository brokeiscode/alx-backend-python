import asyncio
import aiosqlite

db_name = 'users.db'


async def async_fetch_users():
    async with aiosqlite.connect(db_name) as db:
        result = await db.execute_fetchall("SELECT * FROM users")
        return result


async def async_fetch_older_users():
    async with aiosqlite.connect(db_name) as db:
        result = await db.execute_fetchall("SELECT * FROM users WHERE age > 40")
        return result


async def fetch_concurrently():
    result = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print(result)


asyncio.run(fetch_concurrently())
