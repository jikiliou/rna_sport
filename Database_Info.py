import sqlite3

foot_db = "Football.db"

con = sqlite3.connect(foot_db, timeout=1)
con.row_factory = sqlite3.Row
cursor = con.cursor()

def aff(table) :
	cursor.execute("SELECT * FROM " + table)
	rows = cursor.fetchall()
	for row in rows :
		for key in row.keys() :
			print(row[key], end=", ")
		print("")


	
	