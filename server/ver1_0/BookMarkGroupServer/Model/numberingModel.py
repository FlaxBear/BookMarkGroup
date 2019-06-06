# -*- coding: utf-8 -*-
"""This module contains basic processing for Numbering database."""
from module import baseDB

class NumberingModel(baseDB.BaseDB):
	"""
	Connect to the database adn process numbering database

	Attributes
	---------
	table_info : dict
		Table name and pram info

	"""
	def __init__(self):
		""" Set attributes."""
		super().__init__()
		self.table_info = {
			"table": "numbering",
			"param": {
				"numbering_id": { "primary_key":"YES", "insert": "YES", "update": "YES" },
				"numbering_name": { "primary_key":"NO" , "insert": "YES", "update": "YES"},
				"next_value": { "primary_key":"NO",  "insert": "YES", "update": "YES"},
				"create_time": { "primary_key":"NO",  "insert": "YES", "update": "NO" },
				"update_time": { "primary_key":"NO",  "insert": "YES", "update": "YES"},
			}
		}

	def selectNumbering(self, form):
		"""
		Execute the SELECT statement.

		Parameters
		----------
		form : NumberingEditShowValidate or NumberingEditUpdValidate
			form data

		Returns
		----------
		select_data : list
			All data in the numbering database
		message : str
			'Complate' messsage or Error message
		"""
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertNumbering(self, form):
		"""
		Execute the INSERT statement.

		Parameters
		----------
		form : NumberingEditUpdValidate
			form data

		Returns
		----------
		message : str
			'Complate' message or Error message
		insert_value["numbering_id"] : int
			numbering_id

		"""
		insert_value = self.createRequestSqlValue(form, self.table_info, "insert")

		insert_value["numbering_id"], message = self.getNextValue("numbering_id")
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		insert_sql = self.createInsertSql(self.table_info)

		self.startConnect()
		message = self.insertExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["numbering_id"]

	def updateNumbergin(self, form):
		"""
		Execute the UPDATE statement.

		Parameters
		----------
		form : NumberingEditUpdValidate

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

	def delateNumbergin(self, form):
		"""
		Execute the DELATE statement.

		Parameters
		----------
		form : NumberingEditUpdValidate
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

	def getNextValue(self, numbering_name):
		"""
		Get next value for numbering data

		Parameters
		----------
		numbering_name : str
			numbering_name

		Returns
		----------
		next_value : int
			next numbering
		message : str
			'Complate' message or Error message

		"""
		select_value = {
			'numbering_name' : numbering_name
		}
		select_sql = "SELECT numbering_id,next_value FROM " + self.table_info["table"] + " WHERE numbering_name=%(numbering_name)s"

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)

		if message == "Complate":
			next_value = select_data[0][1]
			update_value = {
				"numbering_id": select_data[0][0],
				"next_value": next_value + 1,
				"update_time": self.create_time()
			}
			update_sql = "UPDATE " + self.table_info["table"] + " SET next_value = %(next_value)s, update_time = %(update_time)s WHERE numbering_id=%(numbering_id)s"
			message = self.updateExecute(update_sql, update_value)
			if message != "Complate":
				next_value = 0
		else :
			next_value = 0
		self.finishConnect()
		return next_value, message

	def getList(self):
		"""
		Get NUmbering data list

		Returns
		----------
		select_data : list
			numbering data list

		message : str
			'Complate' message or Error message
		"""
		select_sql = """
					SELECT numbering_id, numbering_name, next_value
					, create_time, update_time
					FROM numbering
					"""
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	def getData(self, numbering_id):
		"""
		Get one data based on numbering_id

		Parameters
		----------
		numbering_id : str
			group_folder_id data

		Returns
		----------
		select_data : list
			One GroupFolder data
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT numbering_id FROM " + self.table_info["table"] + " WHERE numbering_id=%(numbering_id)s"
		sql_value = {
			"numbering_id": numbering_id
		}
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, sql_value)
		self.finishConnect()

		return select_data, message
