# -*- coding: utf-8 -*-
"""This module contains basic processing for database operations."""
import mysql.connector
import datetime

class BaseDB:
	"""
	Connect to the database and create and execute SQL for each processing.
	
	Attributes
	----------
	__user : str
		User name to connect to the database
	__password : str
		Password to connect to the database
	__host : str
		Host to connect to the database
	__db : str
		Database to connect to the database
	__conn : mysql.connector.connection_cext.CMySQLConnection
		Variable for database connection
	__cur : mysql.connector.cursor_cext.CMySQLCursor
		Variable for database connection

	"""

	def __init__(self):
		"""Set attributes."""
		self.__user = ""
		self.__password = ""
		self.__host = ""
		self.__db = ""
		self.__conn = None
		self.__cur = None

	def startConnect(self):
		"""Connect to the database."""
		self.__conn = mysql.connector.connect(user=self.__user, password=self.__password, host=self.__host, db=self.__db)
		self.__cur = self.__conn.cursor()
		return 

	def finishConnect(self):
		"""Disconnect to the database."""
		self.__cur.close
		self.__conn.close
		return
		
	def selectExecute(self, sql, condition_value):
		"""
		Execute the SELECT statement.

		Parameters
		----------
		sql : str
			SQL statement
		condition_value : dict
			Value of parameter required for processing

		Returns
		----------
		select_data : list
			The acquired data list
		message : str
			'Complate' message or Error message

		"""
		select_data = ""
		message = ""
		try:
			self.__cur.execute(sql, condition_value)
			select_data = self.__cur.fetchall()
			self.__conn.commit()
			message = "Complate"
		except Exception as e:
			self.__conn.rollback()
			message = e
		finally:
			pass
		return select_data, message

	def insertExecute(self, sql, insert_data):
		"""
		Execute the INSERT statement.

		Parameters
		----------
		sql : str
			SQL statement
		insert_data : dict
			Value of parameter required for processing

		Returns
		----------
		message : str
			'Complate' message or Error message

		"""
		message = ""
		try:
			self.__cur.execute(sql, insert_data)
			self.__conn.commit()
			message = "Complate"
		except Exception as e:
			self.__conn.rollback()
			message = e
		finally:
			pass
		return message

	def updateExecute(self, sql, update_data):
		"""
		Execute the UPDATE statement.

		Parameters
		----------
		sql : str
			SQL statement
		update_data : dict
			Value of parameter required for processing

		Returns
		----------
		message : str
			'Complate' message or Error message

		"""
		message = ""
		try:
			self.__cur.execute(sql, update_data)
			self.__conn.commit()
			message = "Complate"
		except Exception as e:
			self.__conn.rollback()
			message = e
		finally:
			pass
		return message

	def delateExecute(self, sql, delate_data):
		"""
		Execute the DELATE statement.

		Parameters
		----------
		sql : str
			SQL statement
		delate_data : dict
			Value of parameter required for processing

		Returns
		----------
		message : str
			'Complate' message or Error message

		"""
		message = ""
		try:
			self.__cur.execute(sql, delate_data)
			self.__conn.commit()
			message = "Complate"
		except Exception as e:
			self.__conn.rollback()
			message = e
		finally:
			pass
		return message

	def createSelectSql(self, table_info):
		"""
		Create SELECT statement.

		Parameters
		----------
		table_info : dict
			Table information

		Returns
		----------
		sql : str
			SELECT statement

		"""
		sql_where = ""
		sql_value = ""

		for key in table_info["param"]:
			if(table_info["param"][key]["primary_key"] == "YES"):
				sql_where += key + "=%(" + key + ")s"
			sql_value += key + ","

		sql_value = sql_value[:-1]

		sql = "SELECT " + sql_value + " FROM " + table_info["table"] + " WHERE " + sql_where
		return sql


	def createInsertSql(self, table_info):
		"""
		Create INSERT statement.

		Parameters
		----------
		table_info : dict
			Table information

		Returns
		----------
		sql : str
			INSERT statement
			
		"""
		sql_key = "("
		sql_value = "("

		for key in table_info["param"]:
			if(table_info["param"][key]["insert"] == "YES"):
				sql_key += key + ","
				sql_value += "%(" + key + ")s,"

		sql_key = sql_key[:-1]
		sql_value = sql_value[:-1]

		sql_key += ")"
		sql_value += ")"

		sql = "INSERT INTO " + table_info["table"] + sql_key + "VALUES" + sql_value
		return sql
		
	def createUpdateSql(self, table_info):
		"""
		Create UPDATE statement.

		Parameters
		----------
		table_info : dict
			Table information

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
					sql_value += key + "=%(" + key + ")s,"

		sql_value = sql_value[:-1]

		sql = "UPDATE " + table_info["table"] + " SET " + sql_value + " WHERE " + sql_where
		return sql

	def createDelateSql(self, table_info):
		"""
		Create DELATE statement.

		Parameters
		----------
		table_info : dict
			Table information

		Returns
		----------
		sql : str
			DELATE statement
			
		"""
		sql_where = ""

		for key in table_info["param"]:
			if(table_info["param"][key]["primary_key"] == "YES"):
				if(sql_where != ""):
					sql_where += " AND " + key + "=%(" + key + ")s"
				else:
					sql_where += key + "=%(" + key + ")s"

		sql = "DELETE FROM " + table_info["table"] + " WHERE " + sql_where
		return sql

	def createRequestSqlValue(self, request):
		"""
		Create Sql value dict

		Parameters
		----------
		request : dict
			Post data

		Returns
		----------
		return_request : dict
			Sql value dict
			
		"""
		if request.method == "POST":
			return_request = request.form
		else :
			return_request = {}
		return return_request

	def create_time(self):
		"""
		Create datetime.

		Returns
		----------
		datetime : str
			Current time
			
		"""
		return datetime.datetime.now()