# -*- coding: utf-8 -*-
"""This module contains basic processing for GroupFolder database."""
from module import baseDB
import numberingModel

class GroupFolderModel(baseDB.BaseDB):
	"""
	Connect to the database adn process groupFolder database

	Attributes
	---------
	table_info : dict
		Table name and pram info

	"""
	def __init__(self):
		""" Set attributes."""
		super().__init__()
		self.table_info = {
			"table": "group_folder",
			"param": {
				"group_folder_id": { "primary_key":"YES", "insert": "YES", "update": "YES", "version": "YES"},
				"group_folder_name": { "primary_key":"NO", "insert": "YES", "update": "NO", "version": "NO"},
				"group_folder_version": { "primary_key":"NO", "insert": "YES", "update": "YES", "version": "YES"},
				"json_directory_path": { "primary_key":"NO", "insert": "YES", "update": "NO", "version": "NO"},
				"group_folder_memo": { "primary_key":"NO", "insert": "YES", "update": "YES", "version": "NO"},
				"create_time": { "primary_key":"NO" , "insert": "YES", "update": "NO", "version": "NO"},
				"update_time": { "primary_key":"NO" , "insert": "YES", "update": "YES", "version": "NO"},
			}
		}

	def selectGroupFolder(self, form):
		"""
		Execute the SELECT statement.

		Parameters
		----------
		form :  GroupFolderEditShowValidate or GroupFolderUpdValidate
			form data

		Returns
		----------
		select_data : list
			All data in the groupFolder database
		message : str
			'Complate' messsage or Error message
		"""
		select_value = self.createRequestSqlValue(form, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertGroupFolder(self, form):
		"""
		Execute the INSERT statement.

		Parameters
		----------
		form : GroupFolderUpdValidate
			form data

		Returns
		----------
		message : str
			'Complate' message or Error message
		insert_value["group_folder_id"] : int
			group_folder_id

		"""
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
		"""
		Execute the UPDATE statement.

		Parameters
		----------
		form : GroupFolderUpdValidate

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

	def delateGroupFolder(self, form):
		"""
		Execute the DELATE statement.

		Parameters
		----------
		form : GroupFolderUpdValidate
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
		Get groupFolder data list

		Returns
		----------
		select_data : list
			groupFolder data list
		message : str
			'Complate' message or Error message

		"""
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
		"""
		For authority page
		Get groupFolder's group_folder_id and group_folder_name data list

		Returns
		----------
		select_data : list
			groupFolder's group_folder_id and group_folder_name data
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT group_folder_id, group_folder_name FROM group_folder"

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, {})
		self.finishConnect()

		return select_data, message

	def getData(self, group_folder_id):
		"""
		Get one data based on group_folder_id

		Parameters
		----------
		group_folder_id : int
			group_folder_id data

		Returns
		----------
		select_data : list
			One GroupFolder data
		message : str
			'Complate' message or Error message
		"""
		select_sql = "SELECT group_folder_id FROM " + self.table_info["table"] + " WHERE group_folder_id=%(group_folder_id)s"
		sql_value = {
			"group_folder_id": group_folder_id
		}
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, sql_value)
		self.finishConnect()

		return select_data, message

	def selectGroupFolderPlugin(self, group_folder_id):
		"""
		For Plugin
		Get one data based on group_folder_id

		Parameters
		----------
		group_folder_id : int
			group_folder_id data

		Returns
		----------
		select_data : list
			One GroupFolder data
		message : str
			'Complate' message or Error message
		"""
		select_value = self.createRequestSqlValue({}, self.table_info, "primary_key")
		select_sql = self.createSelectSql(self.table_info)

		select_value["group_folder_id"] = group_folder_id

		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)
		self.finishConnect()

		return select_data, message

	def insertGroupFolderPlugin(self, group_folder_name):
		"""
		For Plugin
		Insert one data

		Parameters
		----------
		group_folder_name : str
			group_folder_name data

		Returns
		----------
		message : str
			'Complate' message or Error message
		insert_value["group_folder_id"] : int
			group_folder_id
		"""
		numbering_class = numberingModel.NumberingModel()

		insert_value = self.createRequestSqlValue({}, self.table_info, "insert")
		insert_value["group_folder_id"], message = numbering_class.getNextValue("group_folder_id")
		insert_value["group_folder_name"] = group_folder_name
		insert_value["group_folder_version"] = 1
		insert_value["json_directory_path"] = str(insert_value["group_folder_id"]) + "_" + insert_value["group_folder_name"]
		insert_value["create_time"] = self.create_time()
		insert_value["update_time"] = self.create_time()

		insert_sql = self.createInsertSql(self.table_info)

		self.startConnect()
		message = self.insertExecute(insert_sql, insert_value)
		self.finishConnect()

		return message, insert_value["group_folder_id"]

	def updateGroupFolderPlugin(self, group_folder_id):
		"""
		For Plugin
		Update one data

		Parameters
		----------
		group_folder_id : int
			group_folder_id

		Returns
		----------
		message : str
			'Complate' message or Error message
		"""
		message = ""
		select_value = {
			"group_folder_id": group_folder_id
		}
		select_sql = "SELECT group_folder_id,group_folder_version FROM " + self.table_info["table"] + " WHERE group_folder_id=%(group_folder_id)s"
		self.startConnect()
		select_data, message = self.selectExecute(select_sql, select_value)

		if message == "Complate":
			update_value = {
				"group_folder_id": group_folder_id,
				"group_folder_version": select_data[0][1] + 1,
				"update_time": self.create_time()
			}
			update_sql = "UPDATE " + self.table_info["table"] + " SET group_folder_version = %(group_folder_version)s, update_time = %(update_time)s WHERE group_folder_id=%(group_folder_id)s"
			message = self.updateExecute(update_sql, update_value)
		self.finishConnect()
		return message
