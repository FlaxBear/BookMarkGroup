import hashlib, binascii
from module import baseDB
import numberingModel

class AdminUserModel(baseDB.BaseDB):
	def __init__(self):
		super().__init__()
		self.table_info = {
			"table": "adomin_user",
			"param": {
				"user_id": {"primary_key":"YES", "insert": "YES", "update": "YES"},
				"user_name": {"primary_key":"NO", "insert": "YES", "update": "YES"},
				"user_mail_address": {"primary_key":"NO", "insert": "YES", "update": "YES"},
				"user_password":  {"primary_key":"NO", "insert": "YES", "update": "YES"},
				"create_time": { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"update_time": { "primary_key":"NO", "insert": "YES", "update": "YES"},
			}
		}

	def selectUser(self, form):
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertUser(self, form):
		numbering_class = numberingModel.NumberingModel()

		insert_value = self.createRequestSqlValue(form, self.table_info, "insert")

		insert_value["user_id"], message = numbering_class.getNextValue("user_id")
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()
		insert_value["user_password"] = self.safty_password(insert_value["user_id"], insert_value["user_password"])

		insert_sql = self.createInsertSql(self.table_info)
		
		self.startConnect()
		message = self.insertExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["user_id"]

	def updateUser(self, form):
		update_value = self.createRequestSqlValue(form, self.table_info, "update")
		update_value["update_time"] = self.create_time()

		self.startConnect()
		select_data, message = self.selectUser(form)

		if update_value["user_password"] == select_data[0][3]:
			update_sql = self.createUpdateSql(self.table_info, False)
			update_value.pop("user_password")
		else:
			update_sql = self.createUpdateSql(self.table_info, True)
			update_value["user_password"] = self.safty_password(update_value["user_id"], update_value["user_password"])
			
		message = self.updateExecute(update_sql, update_value)
		self.finishConnect()

		return message
	
	def delateUser(self, form):
		delate_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		delate_sql = self.createDelateSql(self.table_info)

		self.startConnect()
		message = self.delateExecute(delate_sql, delate_value)
		self.finishConnect()

		return message

	def getList(self):
		select_sql = """
					 SELECT user_id, user_name, user_mail_address, user_password
					 , create_time, update_time
					 FROM adomin_user
					"""
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	def getLoginData(self, user_mail_address):
		select_sql = "SELECT user_id, user_mail_address, user_password FROM " + self.table_info["table"] + " WHERE user_mail_address"
		sql_value = {
			"user_mail_address": user_mail_address
		}

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, sql_value)
		self.finishConnect()

		return select_data, message

	def createUpdateSql(self, table_info, password_state):
		sql_where = ""
		sql_value = ""

		for key in table_info["param"]:
			if(table_info["param"][key]["primary_key"] == "YES"):
				sql_where += key + "=%(" + key + ")s"
			else:
				if(table_info["param"][key]["update"] == "YES"):
					if(key == "user_password"):
						if password_state == True:
							sql_value += key + "=%(" + key + ")s,"
					else:
						sql_value += key + "=%(" + key + ")s,"

		sql_value = sql_value[:-1]

		sql = "UPDATE " + table_info["table"] + " SET " + sql_value + " WHERE " + sql_where
		return sql

	def safty_password(self, id, password):
		hash = hashlib.sha256()
		hash.update(str(id).encode("UTF-8") + password.encode("UTF-8"))
		return hash.hexdigest()