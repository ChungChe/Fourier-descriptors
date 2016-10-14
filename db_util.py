import sqlite3 as db
import sys
import time
import random

dbName = "curve.db"

def create_db(dbName):
	try:
		con = db.connect(dbName)
		cur = con.cursor()
		cur.execute("create table a_curve ( \
					machine_id INTEGER not null, \
					value REAL, \
					timestamp DATETIME default CURRENT_TIMESTAMP \
				)")
		con.commit()
	except db.Error, e:
		if con:
			con.rollback()
		print("Error %s:" % e.args[0])
		sys.exit(1)
	finally:
		if con:
			con.close()

def insert(cur, m_id, value):
	data = [m_id, value]
	cur.execute("insert into a_curve values (?,?,datetime('now'))", data)

def insert_data(con, cur, m_id, value):
    insert(cur, m_id, value)
    con.commit()
