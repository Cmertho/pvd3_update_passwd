import sys
import logging
import passgen
import bcrypt
import pymongo
import click
from urllib.parse import quote_plus


def log_uncaught_exceptions(ex_cls="", ex="", tb=""):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    with open("error.txt", "a+", encoding="utf-8") as file:
        file.write(text)
    logging.error(text)


sys.excepthook = log_uncaught_exceptions

#
login_db = ""
passwd_db = ""
ip_db = ""


def generate():
    """
    Генерация рандомных паролей
    :return: сгенерированный пароль при помощи bCrypt  с salt
    """
    random_string = "".join(passgen.passgen(10))
    return bcrypt.hashpw(random_string.encode("utf-8"), bcrypt.gensalt(10, prefix=b"2a")).decode("utf-8"), random_string


@click.command()
@click.option("-login", prompt="Старый логин прользователя", help="Логин прользователя")
@click.option("-login_new", prompt="Новый логин прользователя", help="Логин прользователя")
def update_passwd(login, login_new):
    logger = logging.getLogger("update_user_pvd3")
    logger.setLevel(logging.INFO)
    logger.info(f"Генерация пароля для {login}")

    passwd = generate()
    logging.info("Пароль сгенерирован")
    conn = pymongo.MongoClient('mongodb://%s:%s@%s/pvdrs' % (quote_plus(login_db), quote_plus(passwd_db),
                                                             ip_db), port=27017)

    # выбираем базу данных
    db = conn.pvdrs

    # выбираем коллекцию документов
    coll = db.mia_user
    logger.info("Чтение базы")
    if coll.find_one({"login": login}):
        logger.info("Обновление пароля в базе")
        coll.update_one({"login": login}, {"$set": {"password": passwd[0], "login": login_new}})
        logger.info("Пароль в базе обновлен")
        logger.info("Обновление пароля успешно завершено")
    else:
        logger.error("Учетная запись не существует или не верно записана")
    with open("log.txt", "a+", encoding="utf-8") as file:
        file.write(f"{login} - Изменен пароль\n")


if __name__ == "__main__":
    update_passwd()
