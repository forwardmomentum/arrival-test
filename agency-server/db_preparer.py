# -*-  coding: utf-8 -*-


# metadata = sa.MetaData()
#
# tbl = sa.Table('drivers', metadata,
#                sa.Column('driver_id', sa.Integer, primary_key=True),
#                sa.Column('val', sa.String(255)))
#
#
async def prepare_db(conn, drivers_count):
    await conn.execute('DROP TABLE IF EXISTS messages')
    await conn.execute('DROP TABLE IF EXISTS users')
    await conn.execute('''CREATE TABLE users (
     id serial PRIMARY KEY,
     "name" varchar(50),
     email varchar(30),
     birthdate date,
     phone varchar(15),
     working_day_start time,
     working_day_finish time,
     first_rest_start time,
     first_rest_stop time,
     launch_rest_start time,
     launch_rest_stop time,
     second_rest_start time,
     second_rest_stop time,
     third_rest_start time,
     third_rest_stop time
    );''')
    await conn.execute('''CREATE TABLE messages (
     message_id uuid PRIMARY KEY,
     body text,
     type varchar(12),
     sended_at timestamp,
     from_id int4,
     to_id int4
    );''')
    await conn.execute('''ALTER TABLE messages ADD CONSTRAINT messages_users_fk_to FOREIGN KEY (to_id) REFERENCES users(id);
                        ALTER TABLE messages ADD CONSTRAINT messages_users_fk_from FOREIGN KEY (from_id) REFERENCES users(id);''')
    await conn.execute('''CREATE INDEX messages_from_id_idx ON messages (from_id,to_id);''')


    # async with engine.acquire() as conn:
    #     await conn.execute(tbl.insert().values(val='abc'))
    #
    #     async for row in conn.execute(tbl.select()):
    #         print(row.id, row.val)
