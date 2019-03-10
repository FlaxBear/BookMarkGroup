import db
import numberingModel

class GroupFolderModel(db.Base_db):
	def __init__(self):
		self.table_info = {
			"table": "group_folder",
			"param": {
				"group_folder_id": { "primary_key":"YES", "insert": "YES", "update": "NO"},
				"group_folder_name": { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"group_folder_version": { "primary_key":"NO", "insert": "YES", "update": "YES"},
				"json_directory_path": { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"group_folder_memo": { "primary_key":"NO", "insert": "YES", "update": "YES" },
				"create_time": { "primary_key":"NO" , "insert": "YES", "update": "NO"},
				"update_time": { "primary_key":"NO" , "insert": "YES", "update": "YES"},
			}
		}

	def selectGroupFolder(self, request):
		# Create select_value from requested data
		select_value = self.createRequestSqlValue(request)

		# Create sql statement
		select_sql = self.createSelectSql(self.table_info)

		# Perform processing
		select_data, message = self.selectExecute(select_sql, select_value)
		return select_data, message

	def insertGroupFolder(self, request):
		
		numbering_class = numberingModel.NumberingModel()

		# Create insert_value from requested data
		insert_value = self.createRequestSqlValue(request)
		# Acquire group_folder_id from numbering DB
		insert_value["group_folder_id"] = numbering_class.getNextValue("group_folder_id")
		insert_value["group_folder_version"] = 1
		insert_value["json_directory_path"] = insert_value["group_folder_id"] + "_" + insert_value["group_folder_name"]
		insert_value["group_folder_memo"] = ""
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		# Create sql statement
		insert_sql = self.createInsertSql(self.table_info)

		# Perform processing
		message = self.insertExecute(insert_sql, insert_value)
		return message

	def updateGroupFolder(self, request):

		# Create update_value from requested data
		update_value = self.createRequestSqlValue(request)
		update_value["update_time"] = self.create_time()

		# Create sql statement
		update_sql = self.createUpdateSql(self.table_info)

		# Perform processing
		message = self.updateExecute(update_sql, update_value)
		return message

	def delateGroupFolder(self, request):
		# Create delate_value from requested data
		delate_value = self.createRequestSqlValue(request)

		# Create sql statement
		delate_sql = self.createDelateSql(self.table_info)

		# Perform processing
		message = self.delateExecute(delate_sql, delate_value)
		return message