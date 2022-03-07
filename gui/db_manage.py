import sqlite3


class DataBaseWR:
	# write and red with db
	def __init__(self):
		self.name_table = "CashBase"
		self.column_table = "Date TEXT, Time TEXT, Remark TEXT, Cash_In NUMERIC, Cash_Out NUMERIC, Balance INTEGER"
		self.connect()
		self.create_table()

	def connect(self):
		self.conn = sqlite3.connect('db.db')
		self.cursor = self.conn.cursor()
	
	def create_table(self):
		try:
			self.cursor.execute(f"CREATE TABLE {self.name_table} ({self.column_table})")
		except sqlite3.OperationalError:
			pass
	
	def write_in_db(self, list_data):
		self.cursor.execute(f"INSERT INTO {self.name_table} VALUES {list_data}")
		self.conn.commit()
	
	def read_db(self):
		rows = self.cursor.execute(f"SELECT {self.column_table} FROM {self.name_table}").fetchall()
		return rows
	
	def close(self):
		self.cursor.close()
		self.conn.close()