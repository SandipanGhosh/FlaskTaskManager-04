# project/db_create.py

from views import db
from models import Task
from datetime import date

# create db and table
db.create_all()

# insert data
#db.session.add(Task("Finish this tutorial", date(2018, 1, 26), 10, 1))
#db.session.add(Task("Finish this course", date(2018, 1, 31), 10, 1))

# commit changes
db.session.commit()