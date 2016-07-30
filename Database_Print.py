from Database_Info import *

def print_table(con, str) :
	cursor = con.execute(str)
	for row in cursor :
		print(row)
	
def print_match(con) :
	str = "SELECT * FROM match"
	print_table(con, str)
	
con = sqlite3.connect(foot_db)
print_match(con)