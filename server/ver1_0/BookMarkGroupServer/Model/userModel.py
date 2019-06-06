# -*- coding: utf-8 -*-
"""This module contains basic processing for User database."""
import hashlib, binascii
from module import baseDB
import numberingModel

class UserModel(baseDB.BaseDB):
	"""
	Connect to the database adn process User database

	Attributes
	---------
	table_info : dict
		Table name and pram info

	"""

	def __init__(self):
		""" Set attributes. """
		super().__init__()
		self.table_info = {
			"table": "user",
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
		"""
		Execute the SELECT statement.

		Parameters
		----------
		form :  UserEditShowValidate or UserEditUpdValidate
			form data

		Returns
		----------
		select_data : list
			All data in the User database
		message : str
			'Complate' messsage or Error message
		"""
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertUser(self, form):
		"""
		Execute the INSERT statement.

		Parameters
		----------
		form : UserEditUpdValidate
			form data

		Returns
		----------
		message : str
			'Complate' message or Error message
		insert_value["user_id"] : int
			user_id

		"""
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
		"""
		Execute the UPDATE statement.

		Parameters
		----------
		form : UserEditUpdValidate

		Returns
		----------
		message : str
			'Complate' message or Error message

		"""
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
		"""
		Execute the DELATE statement.

		Parameters
		----------
		form : UserEditUpdValidate
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
		Get user data list

		Returns
		----------
		select_data : list
			user data list
		message : str
			'Complate' message or Error message

		"""
		select_sql = """
					 SELECT user_id, user_name, user_mail_address, user_password
					 , create_time, update_time
					 FROM user
					"""
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	def getSelectList(self):
		"""
		For authority page
		Get user's user_id and user_name data list

		Returns
		----------
		select_data : list
			user's user_id and user_name data list
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT user_id, user_name FROM user"

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	def createUpdateSql(self, table_info, password_state):
		"""
		Over write
		Create UPDATE statement

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
					if(key == "user_password"):
						if password_state == True:
							sql_value += key + "=%(" + key + ")s,"
					else:
						sql_value += key + "=%(" + key + ")s,"

		sql_value = sql_value[:-1]

		sql = "UPDATE " + table_info["table"] + " SET " + sql_value + " WHERE " + sql_where
		return sql

	def getData(self, user_id):
		"""
		Get user's user_id, user_mail_address and user_id

		Parameters
		----------
		user_id : str
			user_id

		Returns
		----------
		select_data : list
			user's user_id, user_mail_address and user_password
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT user_id, user_mail_address, user_password FROM " + self.table_info["table"] + " WHERE user_id=%(user_id)s"
		sql_value = {
			"user_id": user_id
		}
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, sql_value)
		self.finishConnect()

		return select_data, message

	def getLoginData(self, user_mail_address):
		"""
		For Plugin
		Get user's user_id, user_mail_address and user_password

		Parameters
		----------
		user_mail_address : str
			user mail address

		Returns
		----------
		select_data : list
			user's user_id, user_mail_address and user_password
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT user_id, user_mail_address, user_password FROM " + self.table_info["table"] + " WHERE user_mail_address=%(user_mail_address)s"
		sql_value = {
			"user_mail_address": user_mail_address
		}

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, sql_value)
		self.finishConnect()

		return select_data, message

	def safty_password(self, id, password):
		"""
		Generate encrypted password

		Parameters
		----------
		id : int
			user_id
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