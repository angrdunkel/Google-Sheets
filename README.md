# Google-Sheets

Действия для разворачивания проектов


Создание и работа с виртуальной средой.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Зайти в папку проекта еклипса и выполнить::

   virtualenv .venv  # для python2
   virtualenv -p python3 .venv3 # для python3

потом::

   . .venv/bin/activate  # для python2
   . .venv3/bin/activate # для python3

Установить сразу все нужные модули::
  .venv/bin/pip install -r requirements.txt  # для python2
  .venv3/bin/pip install -r requirements.txt # для python3

Создаём таблицу в postgres с параметрами::
num - int4
price - int4
d_time - date
rub - num
orders - int4

Запускаем скрипт::
python google_shet.py
