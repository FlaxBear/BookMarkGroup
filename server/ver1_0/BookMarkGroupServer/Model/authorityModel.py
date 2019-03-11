from module import baseDB

class AuthorityModel(baseDB.BaseDB):
	def __init__(self):
		self.table_info = {
			"table": "authority",
			"param": {
				"user_id": { "primary_key":"YES", "insert": "YES", "update": "NO"},
				"group_folder_id": { "primary_key":"YES", "insert": "YES", "update": "NO"},
				"authority_state" : { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"create_time": { "primary_key":"NO" , "insert": "YES", "update": "NO"},
				"update_time": { "primary_key":"NO" , "insert": "YES", "update": "YES"},
			}
		}

	def selectAuthority(self, request):
		# Create select_value from requested data
		select_value = self.createRequestSqlValue(request)

		# Create sql statement(This function is override)
		select_sql = self.createSelectSql(self.table_info)

		# Perform processing
		select_data, message = self.selectExecute(select_sql, select_value)
		return select_data, message

	def insertAuthority(self, request):
		# Create insert_value from requested data
		insert_value = self.createRequestSqlValue(request)
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		# Create sql statement
		insert_sql = self.createInsertSql(self.table_info)

		# Perform processing
		message = self.insertExecute(insert_sql, insert_value)
		return message

	def upadteAuthority(self, request):
		# Create update_value from requested data
		update_value = self.createRequestSqlValue(request)
		update_value["update_time"] = self.create_time()

		# Create sql statement
		update_sql = self.createUpdateSql(self.table_info)

		# Perform processing
		message = self.updateExecute(update_sql, update_value)
		return message

	def delateAuthority(self, request):
		# Create delate_value from requested data
		delate_value = self.createRequestSqlValue(request)

		# Create sql statement
		delate_sql = self.createDelateSql(self.table_info)

		# Perform processing
		message = self.delateExecute(delate_sql, delate_value)
		return message

	def createSelectSql(self, request):
		return ""