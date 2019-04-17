from module import baseDB

class AuthorityModel(baseDB.BaseDB):
	def __init__(self):
		super().__init__()
		self.table_info = {
			"table": "authority",
			"param": {
				"user_id": { "primary_key":"YES", "insert": "YES", "update": "YES"},
				"group_folder_id": { "primary_key":"YES", "insert": "YES", "update": "YES"},
				"authority_state" : { "primary_key":"NO", "insert": "YES", "update": "YES"},
				"create_time": { "primary_key":"NO" , "insert": "YES", "update": "NO"},
				"update_time": { "primary_key":"NO" , "insert": "YES", "update": "YES"},
			}
		}

	def selectAuthority(self, form):
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertAuthority(self, form):
		insert_value = self.createRequestSqlValue(form, self.table_info, "insert")
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		insert_sql = self.createInsertSql(self.table_info)

		self.startConnect()
		message = self.insertExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["user_id"], insert_value["group_folder_id"]

	def upadteAuthority(self, form):
		update_value = self.createRequestSqlValue(form, self.table_info, "update")
		update_value["update_time"] = self.create_time()

		update_sql = self.createUpdateSql(self.table_info)

		self.startConnect()
		message = self.updateExecute(update_sql, update_value)
		self.finishConnect()

		return message

	def delateAuthority(self, form):
		delate_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		delate_sql = self.createDelateSql(self.table_info)

		self.startConnect()
		message = self.delateExecute(delate_sql, delate_value)
		self.finishConnect()

		return message

	def getList(self):
		select_sql = """
					 SELECT t1.user_id, t1.group_folder_id
					 , t2.user_name, t3.group_folder_name, t1.authority_state
					 , t1.create_time, t1.update_time
					 FROM authority t1
					 INNER JOIN user t2 ON t1.user_id = t2.user_id
					 INNER JOIN group_folder t3 ON t1.group_folder_id = t3.group_folder_id
					"""

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	def getFolderAuthority(self, group_folder_id):
		delate_value = {
			"group_folder_id": group_folder_id
		}
		#select_sql = """SELECT * FROM authority WHERE group_folder_id=%(group_folder_id)s"""
		select_sql = """
					 SELECT t1.user_id, t2.user_name, t1.authority_state
					 , t1.create_time, t1.update_time
					 , t3.group_folder_name
					 FROM authority t1
					 INNER JOIN user t2 ON t1.user_id = t2.user_id
					 INNER JOIN group_folder t3 ON t1.group_folder_id = t3.group_folder_id
					 WHERE t1.group_folder_id=%(group_folder_id)s
					"""

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, delate_value)
		self.finishConnect()

		return select_data, message