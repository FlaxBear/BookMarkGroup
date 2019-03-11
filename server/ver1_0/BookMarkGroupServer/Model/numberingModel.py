from module import baseDB

class NumberingModel(baseDB.BaseDB):
	def __init__(self):
		self.table_info = {
			"table": "numbering",
			"param": {
				"numbering_id": { "primary_key":"YES", "insert": "YES", "update": "NO"},
				"numbering_name": { "primary_key":"NO" , "insert": "YES", "update": "YES"},
				"next_value": { "primary_key":"NO", "insert": "YES", "update": "YES"},
				"create_time": { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"update_time": { "primary_key":"NO", "insert": "YES", "update": "YES"},
			}
		}

	def selectNumbering(self, request):
		# Create select_value from requested data
		select_value = self.createRequestSqlValue(request)

		# Create sql statement
		select_sql = self.createSelectSql(self.table_info)

		# Perform processing
		select_data, message = self.selectExecute(select_sql, select_value)
		return select_data, message

	def insertNumbering(self, request):
		# Create insert_value from requested data
		insert_value = self.createRequestSqlValue(request)
		# Acquire group_folder_id from numbering DB
		insert_value["group_folder_id"] = self.getNextValue("numbering_id")
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		# Create sql statement
		insert_sql = self.createInsertSql(self.table_info)

		# Perform processing
		message = self.insertExecute(insert_sql, insert_value)
		return message

	def updateNumbergin(self, request):
		# Create update_value from requested data
		update_value = self.createRequestSqlValue(request)
		update_value["update_time"] = self.create_time()

		# Create sql statement
		update_sql = self.createUpdateSql(self.table_info)

		# Perform processing
		message = self.updateExecute(update_sql, update_value)
		return message

	def delateNumbergin(self, request):
		# Create delate_value from requested data
		delate_value = self.createRequestSqlValue(request)

		# Create sql statement
		delate_sql = self.createDelateSql(self.table_info)

		# Perform processing
		message = self.delateExecute(delate_sql, delate_value)
		return message

	def getNextValue(self, numbering_name):
		select_value = {
			"numbering_name": numbering_name
		}
		select_sql = "SELECT numbering_id,next_value FROM " + self.table_info["table"] + " WHERE numbering_name=%(numbering_name)s"

		# Perform processing
		select_data, message = self.selectExecute(select_sql, select_value)

		if message == "Complate":
			next_value = select_data[1]
			update_value = {
				"table": self.table_info["table"],
				"numbering_id": select_data[0],
				"next_value": next_value + 1,
				"update_time": self.create_time()
			}
			update_sql = """
				UPDATE %(table)s SET
				next_value=%(next_value)s,
				update_time=%(update_time)s
				WHERE numbering_id=%(numbering_id)s
			"""
			message = self.updateExecute(update_sql, update_value)
			if message != "Complate":
				next_value = 0
		else :
			next_value = 0
		return next_value, message