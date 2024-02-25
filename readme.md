flask run

db:
flask db init
flask db migrate
flask db upgrade
flask db downgrade

tests:
cd tests -> python -m unittest user.py

coverage run -m unittest user.py
coverage report -m
python user.py #HTMLTestRunner