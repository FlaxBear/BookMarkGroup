from module import baseDB
import numberingModel

class GroupFolderModel(baseDB.BaseDB):
	def __init__(self):
		super().__init__()
		self.table_info = {
			"table": "group_folder",
			"param": {
				"group_folder_id": { "primary_key":"YES", "insert": "YES", "update": "YES"},
				"group_folder_name": { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"group_folder_version": { "primary_key":"NO", "insert": "YES", "update": "YES"},
				"json_directory_path": { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"group_folder_memo": { "primary_key":"NO", "insert": "YES", "update": "YES" },
				"create_time": { "primary_key":"NO" , "insert": "YES", "update": "NO"},
				"update_time": { "primary_key":"NO" , "insert": "YES", "update": "YES"},
			}
		}

	def selectGroupFolder(self, form):
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertGroupFolder(self, form):		
		numbering_class = numberingModel.NumberingModel()

		insert_value = self.createRequestSqlValue(form, self.table_info, "insert")
		insert_value["group_folder_id"], message = numbering_class.getNextValue("group_folder_id")
		insert_value["group_folder_version"] = 1
		insert_value["json_directory_path"] = str(insert_value["group_folder_id"]) + "_" + insert_value["group_folder_name"]
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		insert_sql = self.createInsertSql(self.table_info)

		self.startConnect()
		message = self.insertExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["group_folder_id"]

	def updateGroupFolder(self, form):
		update_value = self.createRequestSqlValue(form, self.table_info, "update")
		update_value["update_time"] = self.create_time()

		update_sql = self.createUpdateSql(self.table_info)

		self.startConnect()
		message = self.updateExecute(update_sql, update_value)
		self.finishConnect()
		
		return message

	def delateGroupFolder(self, form):
		delate_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		delate_sql = self.createDelateSql(self.table_info)

		self.startConnect()
		message = self.delateExecute(delate_sql, delate_value)
		self.finishConnect()

		return message

	def getList(self):
		select_sql = """
					 SELECT group_folder_id, group_folder_name, group_folder_version, json_directory_path, group_folder_memo
					 , create_time, update_time
					 FROM group_folder
					"""
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	
	def getSelectList(self):
		select_sql = "SELECT group_folder_id, group_folder_name FROM group_folder"

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message