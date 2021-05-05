from mongoengine.fields import StringField, IntField
from mongoengine import Document
from mongoengine import connect
import config
import modes

mongo_config = config.get('mongodb')
connect(mongo_config['name'], host=mongo_config['host'])


class User(Document):
    id = StringField(primary_key=True)
    color = StringField(default='white')
    lang = StringField(default='rus')
    size = IntField(default=2)
    mode = StringField(default=next(iter(modes.modes)))

def add_user(user_id):
    """
    Добавляет юзера в базу
    :param user_id:
    :return:
    """
    user = User(
        id=user_id,
        color="white",
        lang="rus",
        size=2,
        mode=next(iter(modes.modes))
    )
    user.save()


def get_user(user_id):
    """
    Получает юзера из базы
    :param user_id:
    :return:
    """
    return User.objects(id=str(user_id))[0]


def check_user(user_id):
    """
    Проверка есть ли юзер в базе
    :param user_id:
    :return:
    """
    if User.objects(id=str(user_id)).count() == 0:
        return False
    else:
        return True
