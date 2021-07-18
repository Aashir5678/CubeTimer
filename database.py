import sqlite3
from CubeUtilities import Time, MultiPhaseTime

class Database:
	def __init__(self, table_name, db_dir):
		self.database_path = db_dir
		self.table_name = table_name
		self.closed = False

		try:
			self.conn = sqlite3.connect(self.database_path)

		except sqlite3.Error:
			raise Exception(f"'{self.database_path}' doesn't exist.")


		self.cursor = self.conn.cursor()
		self.create_table()


	def create_table(self):
		"""
		Attempts to create the table
		:returns: bool
		"""
		with self.conn:

			if self.table_name == "times":
				try:
					self.cursor.execute("""CREATE TABLE times ( time float, scramble text, date text, DNF integer, multiphase text )""")


				except sqlite3.OperationalError:
					return False

			elif self.table_name == "settings":
				try:
					self.cursor.execute("""CREATE TABLE settings ( inspection integer, display_time integer, scramble_len integer, multiphase integer, puzzle_type text )""")

				except sqlite3.OperationalError:
					return False



			else:
				raise ValueError(f"Invalid table name, couldn't create table with name '{self.table_name}'")

			return True

	def insert_record(self, record):
		"""
		Adds a new record to the database
		:param record: Time, MultiPhaseTime, dict
		:returns: bool
		"""
		if self.table_name == "settings":
			with self.conn:
				self.cursor.execute("INSERT INTO settings VALUES (:inspection, :display_time, :scramble_len, :multiphase, :puzzle_type)", record)


		elif self.table_name == "times" and isinstance(record, MultiPhaseTime):
			with self.conn:
				times = record.get_times()

				for index in range(len(times)):
					times[index] = str(times[index])

				times = ", ".join(times)
				
				with self.conn:
					self.cursor.execute("INSERT INTO times VALUES (?, ?, ?, ?, ?)", (record.time, record.scramble, record.date, int(record.DNF), times))

		elif self.table_name == "times" and isinstance(record, Time):
			print ("saving")
			with self.conn:
				self.cursor.execute("INSERT INTO times VALUES (?, ?, ?, ?, ?)",
							   (record.time, record.scramble, record.date, int(record.DNF), ""))


	def delete_record(self, oid=None):
		"""
		Deletes the record with the oid provided, if oid is None, and the table name is settings
		then all records in the database are deleted.
		:param oid: int, None
		:param bool
		"""
		if self.table_name == "settings":
			self.delete_all_records()

			return True

		elif self.table_name == "times" and oid is not None:
			with self.conn:
				self.cursor.execute("DELETE FROM times WHERE oid = :oid",
								   {"oid": oid})

				self.cursor.execute("VACUUM")

			return True

		return False

	def update_record(self, record_attr, new_value, identifier):
		"""
		Updates a record in the database with the attribute record_attr, to new_value.
		Identifier can be an oid, or a dictionary with a seperate record attribute along with it's known value
		:param record_attr: str
		:param new_value: str, int
		:param identifier: int, dict 
		:returns: bool
		"""
		if self.table_name == "times":
			with self.conn:
				try:
					self.cursor.execute(f"UPDATE times SET {record_attr}=:new_value WHERE oid=:oid", {"oid": identifier, "new_value": str(new_value)})

				except sqlite3.Error as e:
					return False

				return True

		elif self.table_name == "settings":
			with self.conn:
				try:
					known_attr, known_val = list(identifier.keys())[0], identifier.get(list(identifier.keys())[0])

					try:
						known_val = int(known_val)

					except ValueError:
						pass

					self.cursor.execute(f"UPDATE settings SET {record_attr}=:new_value WHERE {known_attr}=:known_val", 
						{"new_value": str(new_value), "known_val": known_val})

				except sqlite3.Error:
					return False

				except (AttributeError, TypeError):
					raise Exception("identifier argument must be a dictionary with a key of a seperate record attribute, and it's value is the record attributes known value. Ex: identifier={'puzzle_type': '3x3'}")

			return True

		return False



	def get_record(self, oid=None):
		"""
		Gets the record with the specified oid, if no oid is specified,
		then all records are returned
		:param oid: int, None
		:return: list[record_tuple]
		"""
		if self.table_name == "settings":
			return self.get_all_records()

		self.cursor.execute("SELECT * FROM times WHERE oid=:oid", {"oid": oid})

		return self.cursor.fetchall()



	def get_all_records(self):
		"""
		Gets every record in the database
		:returns: list[record_tuple]
		"""
		with self.conn:
			try:
				self.cursor.execute(f"SELECT * FROM {self.table_name}")

			except sqlite3.Error:
				return []

			return self.cursor.fetchall()


	def delete_all_records(self):
		"""
		Deletes every record in the database
		:returns: bool
		"""
		with self.conn:
			try:
				self.cursor.execute(f"DELETE FROM {self.table_name}")
				self.create_table()

			except sqlite3.Error:
				return False

			else:
				self.cursor.execute("VACUUM")

		return True


	def close_connection(self):
		"""
		Closes the conection to the database:
		:returns: None
		"""
		self.conn.close()
		self.closed = True

	

