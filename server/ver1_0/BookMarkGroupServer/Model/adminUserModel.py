# -*- coding: utf-8 -*-
"""This module contains basic processing for AdminUser database."""
import hashlib, binascii
from module import baseDB
import numberingModel

class AdminUserModel(baseDB.BaseDB):
	"""
	Connect to the database and process AdminUser database

	Attributes
	----------
	table_info : dict
		Table name and param info

	"""
	def __init__(self):
		"""Set attributes."""
		super().__init__()
		self.table_info = {
			"table": "admin_user",
			"param": {
				"admin_user_id": {"primary_key":"YES", "insert": "YES", "update": "YES"},
				"admin_user_name": {"primary_key":"NO", "insert": "YES", "update": "YES"},
				"admin_user_login_id": {"primary_key":"NO", "insert": "YES", "update": "YES"},
				"admin_user_password":  {"primary_key":"NO", "insert": "YES", "update": "YES"},
				"create_time": { "primary_key":"NO", "insert": "YES", "update": "NO"},
				"update_time": { "primary_key":"NO", "insert": "YES", "update": "YES"},
			}
		}

	def selectAdminUser(self, form):
		"""
		Execute the SELECT statement.

		Parameters
		----------
		form : AdminUserEditUpdValidate
			form data

		Returns
		----------
		select_data : list
			All data in the AdminUser database
		message : str
			'Complate' message or Error message
		"""
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertAdminUser(self, form):
		"""
		Execute the INSERT statement.

		Parameters
		----------
		form : AdminUserEditUpdValidate
			form data

		Returns
		----------
		message : str
			'Complate' message or Error message
		insert_value["admin_user_id"] : num
			admin_user_id

		"""
		numbering_class = numberingModel.NumberingModel()

		insert_value = self.createRequestSqlValue(form, self.table_info, "insert")

		# Create data
		insert_value["admin_user_id"], message = numbering_class.getNextValue("admin_user_id")
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()
		insert_value["admin_user_password"] = self.safty_password(insert_value["admin_user_id"], insert_value["admin_user_password"])

		insert_sql = self.createInsertSql(self.table_info)

		self.startConnect()
		message = self.insertExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["admin_user_id"]

	def updateAdminUser(self, form):
		"""
		Execute the UPDATE statement.

		Parameters
		----------
		form : AdminUserEditUpdValidate
			form data

		Returns
		----------
		message : str
			'Complate' message or Error message

		"""
		update_value = self.createRequestSqlValue(form, self.table_info, "update")
		update_value["update_time"] = self.create_time()

		self.startConnect()
		select_data, message = self.selectAdminUser(form)

		if update_value["admin_user_password"] == select_data[0][3]:
			update_sql = self.createUpdateSql(self.table_info, False)
			update_value.pop("admin_user_password")
		else:
			update_sql = self.createUpdateSql(self.table_info, True)
			update_value["admin_user_password"] = self.safty_password(update_value["admin_user_id"], update_value["admin_user_password"])

		message = self.updateExecute(update_sql, update_value)
		self.finishConnect()

		return message

	def delateAdminUser(self, form):
		"""
		Execute the DELATE statement.

		Parameters
		----------
		form : AdminUserEditUpdValidate
			form data

		Returns
		----------
		message : str
			'Complate' message or Error message

		"""
		delate_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		delate_sql = self.createDelateSql(self.table_info)

		self.startConnect()
		message = self.delateExecute(delate_sql, delate_value)
		self.finishConnect()

		return message

	def getList(self):
		"""
		Get adminUser data list

		Returns
		----------
		select_data : list
			adminUser data list
		message : str
			'Complate' message or Error message

		"""
		select_sql = """
					 SELECT admin_user_id, admin_user_name, admin_user_login_id, admin_user_password
					 , create_time, update_time
					 FROM admin_user
					"""
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	def getData(self, admin_user_id):
		"""
		Get one data based on admin_user_id

		Parameters
		----------
		admin_user_id : int
			admin_user_id data

		Returns
		----------
		select_data : list
			One adminUser data
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT admin_user_id, admin_user_login_id, admin_user_password FROM " + self.table_info["table"] + " WHERE admin_user_id=%(admin_user_id)s"
		sql_value = {
			"admin_user_id": admin_user_id
		}

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, sql_value)
		self.finishConnect()

		return select_data, message

	def getLoginData(self, admin_user_login_id):
		"""
		Get one data based on admin_user_login_id

		Parameters
		----------
		admin_user_login_id : int
			admin_user_login_id data

		Returns
		----------
		select_data : list
			One adminUser data
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT admin_user_id, admin_user_login_id, admin_user_password FROM " + self.table_info["table"] + " WHERE admin_user_login_id=%(admin_user_login_id)s"
		sql_value = {
			"admin_user_login_id": admin_user_login_id
		}

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, sql_value)
		self.finishConnect()

		return select_data, message

	def createUpdateSql(self, table_info, password_state):
		"""
		Over write
		Create UPDATE statement.

		Parameters
		----------
		table_info : dict
			Table information

		password_state : bool
			Whether the password has been changed

		Returns
		----------
		sql : str
			UPDATE statement
		"""
		sql_where = ""
		sql_value = ""

		for key in table_info["param"]:
			if(table_info["param"][key]["primary_key"] == "YES"):
				sql_where += key + "=%(" + key + ")s"
			else:
				if(table_info["param"][key]["update"] == "YES"):
					if(key == "admin_user_password"):
						if password_state == True:
							sql_value += key + "=%(" + key + ")s,"
					else:
						sql_value += key + "=%(" + key + ")s,"

		sql_value = sql_value[:-1]

		sql = "UPDATE " + table_info["table"] + " SET " + sql_value + " WHERE " + sql_where
		return sql

	def safty_password(self, id, password):
		"""
		Generate encrypted password

		Parameters
		----------
		id : int
			admin_user_id
		password : str
			password

		Returns
		----------
		Encrypted password : str
			Encrypted password

		"""
		hash = hashlib.sha256()
		hash.update(str(id).encode("UTF-8") + password.encode("UTF-8"))
		return hash.hexdigest()