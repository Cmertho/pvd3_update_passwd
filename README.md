Скрипт для смены  пароля для ПК ПВД 3 update_passwd_pvd3.py

Актуально для версий с 3.8.0 по 3.8.4

 * Пример update_passwd_pvd3.py -login=twiss

Скрипт для смены логина для ПК ПВД3 update_login_pvd3.py

 * Пример update_login_pdv3.py -login=twiss -login_new=twiss_new

Требуемые библиотеки для python:

 * passgen - генерация пароля
  
 * bcrypt - конвертация в хэш функцию 
  
 * pymongo - для работы с бд mongodb
  
 * click - воспроиведение файла с параметрами 


pip install pymongo bcrypt passgen click
