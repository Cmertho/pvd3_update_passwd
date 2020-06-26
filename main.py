import sys
import logging
# pip install passgen
import passgen
# pip install bcrypt
import bcrypt
# pip install pymongo
import pymongo
from urllib.parse import quote_plus


def log_uncaught_exceptions(ex_cls="", ex="", tb=""):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    with open("error.txt", "a+", encoding="utf-8") as file:
        file.write(text)
    logging.error(text)


# отлавливание ошибок
sys.excepthook = log_uncaught_exceptions


def generate():
    """
    Генерация рандомных паролей
    :return: сгенерированный пароль при помощи bCrypt  с salt
    """
    # генерация 10 символьного пароля
    random_string = "".join(passgen.passgen(10))
    return bcrypt.hashpw(random_string.encode("utf-8"), bcrypt.gensalt(10, prefix=b"2a")).decode("utf-8"), random_string


def update_passwd(login):
    # включаем логирование
    logger = logging.getLogger("update_passwd_pvd3")
    # Тип логирования
    logger.setLevel(logging.INFO)
    logger.info(f"Генерация пароля для {login}")
    # Генерация пароля для ПВД 3
    passwd = generate()
    logging.info("Пароль сгенерирован")
    # Заполнения учетных данных для базы данных
    conn = pymongo.MongoClient('mongodb://%s:%s@%s/pvdrs' % (quote_plus("user db mongo"), quote_plus("passwd db mongo"),
                                                             "ip db mongo"), port=27017)

    # выбираем базу данных
    db = conn.pvdrs

    # выбираем коллекцию документов
    coll = db.mia_user
    logger.info("Чтение базы")
    # Проверка на существование пользователя
    if coll.find_one({"login": login}):
        logger.info("Обновление пароля в базе")
        # Обновление пароля пользователя
        coll.update_one({"login": login}, {"$set": {"password": passwd[0]}})
        logger.info("Пароль в базе обновлен")
        logger.info("Обновление пароля успешно завершено")
    else:
        logger.error("Учетная запись не существует или не верно записана")


if __name__ == "__main__":
    # отправка в функцию данных из параметра -login и консоли
    if "-login=" in sys.argv[1]:
        update_passwd(sys.argv[1].replace("-login=", ""))
    # update_passwd(login='')
