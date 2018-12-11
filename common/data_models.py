import datetime
import random
import uuid
import dateutil.parser


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

names = ['Andrew', 'Bob', 'John', 'Vitaly', 'Alex', 'Lina', 'Olga',
         'Doug', 'Julia', 'Matt', 'Jessica', 'Nick', 'Dave', 'Martin',
         'Abbi', 'Eva', 'Lori', 'Rita', 'Rosa', 'Ivy', 'Clare', 'Maria',
         'Jenni', 'Margo', 'Anna']

surnames = ['Monk', 'Davis', 'Evans', 'Ellington']

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