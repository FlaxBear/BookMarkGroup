# -*- coding: utf-8 -*-
"""This module contains basic processing for Authority database."""
from module import baseDB

class AuthorityModel(baseDB.BaseDB):
	"""
	Connect to the database adn process Authority database

	Attributes
	---------
	table_info : dict
		Table name and param info

	"""
	def __init__(self):
		"""Set attributes."""
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
		"""
		Execute the SELECT statement.

		Parameters
		----------
		form : AuthorityEditUpdValidate or authorityEditShowValidate
			form data

		Returns
		----------
		select_data : list
			All data in the Authority database
		message : str
			'Complate' message or Error message
		"""
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertAuthority(self, form):
		"""
		Execute the INSERT statement.

		Parameters
		----------
		form : AuthorityEditUpdValidate
			form data

		Returns
		----------
		message : str
			'Complate' message or Error message
		insert_value["user_id"] : int
			user_id
		insert_value["group_folder_id"] : int
			group_folder_id

		"""
		insert_value = self.createRequestSqlValue(form, self.table_info, "insert")
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		insert_sql = self.createInsertSql(self.table_info)

		self.startConnect()
		message = self.insertExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["user_id"], insert_value["group_folder_id"]

	def upadteAuthority(self, form):
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

		update_sql = self.createUpdateSql(self.table_info)

		self.startConnect()
		message = self.updateExecute(update_sql, update_value)
		self.finishConnect()

		return message

	def delateAuthority(self, form):
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
		Get Authority data list

		Returns
		----------
		select_data : list
			authority data list
		message : str
			'Complate' message or Error message

		"""
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
		"""
		Get one data based on group_folder_id

		Parameters
		----------
		group_folder_id : int
			group_folder_id data

		Returns
		----------
		select_data : list
			One authority data
		message : str
			'Complate' message or Error message
		"""
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

	def insertMastarFolderAuthority(self, group_folder_id, user_id):
		"""
		Insert Mastar data

		Parameters
		----------
		group_folder_id : int
			group_folder_id
		user_id : int
			user_id

		Returns
		----------
		message : str
			'Complate' message or Error message
		insert_value["user_id"]
			user_id
		insert_value["group_folder_id"]
			group_folder_id
		"""
		insert_value = {
			"group_folder_id": group_folder_id,
			"user_id": user_id,
			"authority_state": 16
		}
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		insert_sql = self.createInsertSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["user_id"], insert_value["group_folder_id"]
