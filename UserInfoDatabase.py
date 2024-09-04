import datetime

import aiosqlite


class UsersDataBase:
    def __init__(self):
        self.botDatabase = "database/fileDB/BotDDatabase.db"

    async def create_table_warns(self):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS warns (
                                        userID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        userName TEXT NULL,
                                        countWarns INTEGER DEFAULT 0,
                                        countRemark INTEGER DEFAULT 0,
                                        warns_time TIMESTAMP
                                    )''')
                await db.commit()

    async def insert_warns(self, interaction, member_id, member_name, warn: int, remark: int, warns_time: datetime.datetime):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = '''INSERT INTO warns VALUES (?, ?, ?, ?, ?)'''
                await cursor.execute(query, (member_id, member_name, warn, remark, warns_time))
                await db.commit()

    async def get_warns_older_than(self, seconds: int):
        async with aiosqlite.connect(self.botDatabase) as db:
            warnstime_time = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
            async with db.execute(
                """
                SELECT * FROM warn WHERE warns_time  < ? OR userID = ?
                """,
                (warnstime_time,),
            ) as cursor:
                return await cursor.fetchall()

    async def update_warns(self, interaction, member_id, warn: int):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = '''UPDATE warns SET countWarns = countWarns + ? WHERE userID = ?'''
                await cursor.execute(query, (warn, member_id))
                await db.commit()

    async def update_remark(self, interaction, member_id, remark: int):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query = '''UPDATE warns SET countRemark = countRemark + ? WHERE userID = ?'''
                await cursor.execute(query, (remark, member_id))
                await db.commit()

    async def check_user_warndb(self, member_id):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query_check = '''SELECT * FROM warns WHERE userID = ?'''
                await cursor.execute(query_check, (member_id,))
                row = await cursor.fetchone()
                if row:
                    return row

    async def get_user_warn_count(self, member_id):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query_check = '''SELECT countWarns FROM warns WHERE userID = ?'''
                await cursor.execute(query_check, (member_id,))
                row = await cursor.fetchone()

                if row and row[0] is not None:
                    return row[0]
                else:
                    return 0

    async def get_user_remark_count(self, member_id):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query_check = '''SELECT countRemark FROM warns WHERE userID = ?'''
                await cursor.execute(query_check, (member_id,))
                row = await cursor.fetchone()

                if row and row[0] is not None:
                    return row[0]
                else:
                    return 0

    async def delete_warn_user(self, member_id, countWarn):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query_update = '''UPDATE warns SET countWarns = countWarns - ? WHERE userID = ?'''
                await cursor.execute(query_update, (countWarn, member_id))
                await db.commit()

    async def delete_remark_user(self, member_id, countRemark):
        async with aiosqlite.connect(self.botDatabase) as db:
            async with db.cursor() as cursor:
                query_update = '''UPDATE warns SET countRemark = countRemark - ? WHERE userID = ?'''
                await cursor.execute(query_update, (countRemark, member_id))
                await db.commit()

    async def delete_user_from_all_databases(self, user_id):
        databases = self.botDatabase

        for database in databases:
            async with aiosqlite.connect(database) as db:
                async with db.cursor() as cursor:
                    if 'users' in database:
                        await cursor.execute('DELETE FROM users WHERE userID = ?', (user_id,))
                    elif 'warns' in database:
                        await cursor.execute('DELETE FROM warns WHERE userID = ?', (user_id,))
                    await db.commit()