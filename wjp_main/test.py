#coding=utf8

import time

from config import DBSession
from database.status import Status

session2 = DBSession()
today_date = time.strftime("%Y-%m-%d")
statuss = Status(today = today_date, new_data = 1, duplicate_data = 2)
session2.add(statuss)
session2.commit()
session2.close()