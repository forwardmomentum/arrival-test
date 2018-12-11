# -*-  coding: utf-8 -*-
import datetime
import random
import uuid
import dateutil.parser

import sqlalchemy as sa
from aiopg.sa import create_engine
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


async def get_engine():
    return await create_engine(user='postgres',
                               database='agency',
                               host='127.0.0.1',
                               password='postgres')


Base = declarative_base()

names = ['Andrew', 'Bob', 'John', 'Vitaly', 'Alex', 'Lina', 'Olga',
         'Doug', 'Julia', 'Matt', 'Jessica', 'Nick', 'Dave', 'Martin',
         'Abbi', 'Eva', 'Lori', 'Rita', 'Rosa', 'Ivy', 'Clare', 'Maria',
         'Jenni', 'Margo', 'Anna']
surnames = ['Monk', 'Davis', 'Evans', 'Ellington']


def get_time_with_delta(time, delta):
    return (datetime.datetime.combine(datetime.date(1, 1, 1), time) + delta).time()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.date, datetime.time)):
        return obj.isoformat()
    if isinstance(obj, (UserModel, MessageModel)):
        return obj.to_dict()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError("Type %s not serializable" % type(obj))


class MessageModel:
    def __init__(self, body, from_id, to_id, message_id=None, received=False, sended_at=None):
        if not message_id:
            self.message_id = uuid.uuid4()
        else:
            self.message_id = message_id
        if not sended_at:
            sended_at = datetime.datetime.now()
        self.to_id = to_id
        self.from_id = from_id
        self.sended_at = sended_at
        self.received = received
        self.body = body

    @staticmethod
    def generate_random(from_id, to_id):
        return MessageModel(
            to_id=to_id, from_id=from_id, sended_at=datetime.datetime.now(), received=False,
            body="rndrnd{}".format(random.randint(1, 100))
        )

    @staticmethod
    def build_from_dict(message_dict):
        return MessageModel(message_id=message_dict["message_id"], body=message_dict["body"],
                            sended_at=dateutil.parser.parse(message_dict["sended_at"]),
                            from_id=message_dict["from_id"], to_id=message_dict["to_id"])

    def to_dict(self):
        result = {
            "body": self.body,
            "received": self.received,
            "sended_at": self.sended_at,
            "from_id": self.from_id,
            "to_id": self.to_id
        }
        if self.message_id:
            result["message_id"] = self.message_id
        return result


class UserModel:

    def __init__(self, name, email=None, birthdate=None, phone=None, working_day_start=None, working_day_finish=None,
                 first_rest_start=None,
                 first_rest_stop=None, launch_rest_start=None, launch_rest_stop=None, second_rest_start=None,
                 second_rest_stop=None,
                 third_rest_start=None, third_rest_stop=None, id=None):
        self.phone = phone
        self.working_day_start = working_day_start
        self.working_day_finish = working_day_finish
        self.first_rest_start = first_rest_start
        self.first_rest_stop = first_rest_stop
        self.second_rest_stop = second_rest_stop
        self.second_rest_start = second_rest_start
        self.launch_rest_stop = launch_rest_stop
        self.launch_rest_start = launch_rest_start
        self.third_rest_start = third_rest_start
        self.third_rest_stop = third_rest_stop
        self.id = id
        self.name = name
        self.email = email
        self.birthdate = birthdate

    @staticmethod
    def generate_random(num):
        random_delta = datetime.timedelta(minutes=random.randint(1, 168) * 5)  # to cover all *:*5 time points
        return UserModel(
            name="{} {}".format(names[num % len(names)], surnames[num % len(surnames)]),
            email="{}{}@gmail.com".format(names[num % len(names)], num),
            birthdate=datetime.date(1990, 3, (25 % num + 1)),
            phone="+79229223344",
            working_day_start=get_time_with_delta(datetime.time(0, 0), random_delta),
            working_day_finish=get_time_with_delta(datetime.time(10, 0), random_delta),
            first_rest_start=get_time_with_delta(datetime.time(2, 0), random_delta),
            first_rest_stop=get_time_with_delta(datetime.time(2, 20), random_delta),
            launch_rest_start=get_time_with_delta(datetime.time(4, 0), random_delta),
            launch_rest_stop=get_time_with_delta(datetime.time(5, 0), random_delta),
            second_rest_start=get_time_with_delta(datetime.time(7, 0), random_delta),
            second_rest_stop=get_time_with_delta(datetime.time(7, 20), random_delta),
            third_rest_start=get_time_with_delta(datetime.time(8, 0), random_delta),
            third_rest_stop=get_time_with_delta(datetime.time(8, 20), random_delta)
        )

    def to_dict(self):
        result = {
            "name": self.name,
            "email": self.email,
            "birthdate": self.birthdate,
            "phone": self.phone,
            "working_day_start": self.working_day_start,
            "working_day_finish": self.working_day_finish,
            "first_rest_start": self.first_rest_start,
            "first_rest_stop": self.first_rest_stop,
            "launch_rest_start": self.launch_rest_start,
            "launch_rest_stop": self.launch_rest_stop,
            "second_rest_start": self.second_rest_start,
            "second_rest_stop": self.second_rest_stop,
            "third_rest_start": self.third_rest_start,
            "third_rest_stop": self.third_rest_stop
        }
        if self.id:
            result["id"] = self.id
        return result

    @staticmethod
    def build_from_dict(user_dict):
        return UserModel(name=user_dict["name"], id=user_dict["id"],
                         birthdate=dateutil.parser.parse(user_dict["birthdate"]),
                         phone=user_dict["phone"],
                         working_day_start=dateutil.parser.parse(user_dict["working_day_start"]).time(),
                         working_day_finish=dateutil.parser.parse(user_dict["working_day_finish"]).time(),
                         first_rest_start=dateutil.parser.parse(user_dict["first_rest_start"]).time(),
                         first_rest_stop=dateutil.parser.parse(user_dict["first_rest_stop"]).time(),
                         launch_rest_start=dateutil.parser.parse(user_dict["launch_rest_start"]).time(),
                         launch_rest_stop=dateutil.parser.parse(user_dict["launch_rest_stop"]).time(),
                         second_rest_start=dateutil.parser.parse(user_dict["second_rest_start"]).time(),
                         second_rest_stop=dateutil.parser.parse(user_dict["second_rest_stop"]).time(),
                         third_rest_start=dateutil.parser.parse(user_dict["third_rest_start"]).time(),
                         third_rest_stop=dateutil.parser.parse(user_dict["third_rest_stop"]).time())


metadata_users = sa.MetaData()
users_tbl = sa.Table('users', metadata_users,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('name', sa.String(50)),
                     sa.Column('email', sa.String(30)),
                     sa.Column('birthdate', sa.Date),
                     sa.Column('phone', sa.String(15)),
                     sa.Column('working_day_start', sa.Time),
                     sa.Column('working_day_finish', sa.Time),
                     sa.Column('first_rest_start', sa.Time),
                     sa.Column('first_rest_stop', sa.Time),
                     sa.Column('launch_rest_start', sa.Time),
                     sa.Column('launch_rest_stop', sa.Time),
                     sa.Column('second_rest_start', sa.Time),
                     sa.Column('second_rest_stop', sa.Time),
                     sa.Column('third_rest_start', sa.Time),
                     sa.Column('third_rest_stop', sa.Time)
                     )

metadata_messages = sa.MetaData()
messages_tbl = sa.Table('messages', metadata_messages,
                        sa.Column('message_id', UUID(as_uuid=True), primary_key=True),
                        sa.Column('body', sa.Text),
                        sa.Column('received', sa.Boolean),
                        sa.Column('sended_at', sa.TIMESTAMP),
                        sa.Column("from_id", sa.Integer),
                        sa.Column("to_id", sa.Integer)
                        )


async def read_all_drivers(conn):
    query = sa.select([users_tbl])
    result = []
    async for row in conn.execute(query):
        if row[0] != 1:  # fixme: dirty check
            result.append(UserModel(id=row[0], name=row[1], email=row[2], birthdate=row[3],
                                    phone=row[4], working_day_start=row[5], working_day_finish=row[6],
                                    first_rest_start=row[7], first_rest_stop=row[8], launch_rest_start=row[9],
                                    launch_rest_stop=row[10], second_rest_start=row[11], second_rest_stop=row[12],
                                    third_rest_start=row[13], third_rest_stop=row[14]))
    # print(json.dumps(result, default=json_serial))
    return result


async def read_driver_with_short_history(conn, driver_id):
    # todo make with join to make 1 query instead of 2?
    query = sa.select([users_tbl]).where(users_tbl.c.id == driver_id)
    result = {}
    async for row in conn.execute(query):
        result["driver"] = UserModel(id=row[0], name=row[1], email=row[2], birthdate=row[3],
                                     phone=row[4], working_day_start=row[5], working_day_finish=row[6],
                                     first_rest_start=row[7], first_rest_stop=row[8], launch_rest_start=row[9],
                                     launch_rest_stop=row[10], second_rest_start=row[11], second_rest_stop=row[12],
                                     third_rest_start=row[13], third_rest_stop=row[14])
    result["short_history"] = await read_messages_history(conn, driver_id, short=True)
    # print(json.dumps(result, default=json_serial))
    return result


async def read_messages_history(conn, driver_id, short=False):
    query = sa.select([messages_tbl]).where(
        or_(messages_tbl.c.from_id == driver_id, messages_tbl.c.to_id == driver_id)).order_by(
        messages_tbl.c.sended_at.desc())
    if short:
        query = query.limit(10)
    result = {'driver_id': driver_id, 'history': []}
    async for row in conn.execute(query):
        result["history"].append(MessageModel(message_id=row[0], body=row[1], received=row[2], sended_at=row[3],
                                              from_id=row[4], to_id=row[5]))
    # print(len(result))
    # print(json.dumps(result, default=json_serial))
    return result


async def read_last_messages(conn):
    query = sa.select([messages_tbl]).limit(100).order_by(messages_tbl.c.sended_at)
    result = []
    async for row in conn.execute(query):
        result.append(MessageModel(message_id=row[0], body=row[1], received=row[2], sended_at=row[3],
                                   from_id=row[4], to_id=row[5]))
    # print(len(result))
    # print(json.dumps(result, default=json_serial))
    return result


async def add_message(conn, message_model):
    await conn.execute(messages_tbl.insert().values(message_model.to_dict()))


async def message_received(conn, message_id):
    query = messages_tbl.update().where(messages_tbl.c.message_id == message_id).values(received=True)
    await conn.execute(query)


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
     received bool,
     sended_at timestamp,
     from_id int4,
     to_id int4
    );''')
    await conn.execute('''ALTER TABLE messages ADD CONSTRAINT messages_users_fk_to FOREIGN KEY (to_id) REFERENCES users(id);
                        ALTER TABLE messages ADD CONSTRAINT messages_users_fk_from FOREIGN KEY (from_id) REFERENCES users(id);''')
    await conn.execute('''CREATE INDEX messages_from_id_idx ON messages (from_id,to_id);''')

    await conn.execute(users_tbl.insert().values(name="chief"))

    for i in range(1, drivers_count + 1):
        generated_user = UserModel.generate_random(i)
        await conn.execute(users_tbl.insert().values(generated_user.to_dict()))

    # to generate test messages
    # for x in range(1, 10):
    #     for i in range(1, drivers_count + 1):
    #         generated_message = MessageModel.generate_random(1, i)
    #         await conn.execute(messages_tbl.insert().values(generated_message.to_dict()))
    #         generated_message = MessageModel.generate_random(i, 1)
    #         await conn.execute(messages_tbl.insert().values(generated_message.to_dict()))

    print("Initial data uploaded!")

    # await read_all_drivers(conn)
    # await read_driver_with_short_history(conn, 2)
    # await read_messages_history(conn, 2)
