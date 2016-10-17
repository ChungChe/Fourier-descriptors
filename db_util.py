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
def delete_unreasonable_data(dbName):
    try:
        con = db.connect(dbName)
        cur = con.cursor()
        cur.execute("delete from a_curve where value > 200")
        con.commit()
    except db.Error, e:
        if con:
            con.rollback()
        print("Error %s:" % e.args[0])
        sys.exit(1)
    finally:
        if con:
            con.close()
    
def insert(cur, m_id, value, second_diff = 0):
	data = [m_id, value]
	cur.execute("insert into a_curve values (?,?,datetime('now', 'localtime', '+{} seconds'))".format(second_diff), data)

def insert_data(con, cur, m_id, value):
    insert(cur, m_id, value)
    con.commit()
if __name__ == "__main__":
    #create_db(dbName)
    delete_unreasonable_data(dbName)
