# -*- coding: utf-8 -*-
"""This module contains basic processing for database operations."""
import mysql.connector
import datetime

class Base_db:
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
		self.__user = "root"
		self.__password = ""
		self.__host = "localhost"
		self.__db = "bookmarkgroup"
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
		select_data : 
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
		try:
			self.__cur.execute(sql, insert_data)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			return e
		finally:
			pass
		return "Complate"

	def updateExecute(self, sql, update_data):
		try:
			self.__cur.execute(sql, update_data)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			return e
		finally:
			pass
		return "Complate"

	def delateExecute(self, sql, delate_data):
		try:
			self.__cur.execute(sql, delate_data)
			self.__conn.commit()
		except Exception as e:
			self.__conn.rollback()
			return e
		finally:
			pass
		return "Complate"

	def createSelectSql(self, table_info):
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
		sql_key = "("
		sql_value = "("

		for key in table_info["param"]:
			sql_key += key + ","
			sql_value += "%(" + key + ")s,"

		sql_key = sql_key[:-1]
		sql_value = sql_value[:-1]

		sql_key += ")"
		sql_value += ")"

		sql = "INSERT INTO " + table_info["table"] + sql_key + "VALUES" + sql_value
		return sql
		
	def createUpdateSql(self, table_info):
		sql_where = ""
		sql_value = ""

		for key in table_info["param"]:
			if(table_info["param"][key]["primary_key"] == "YES"):
				sql_where += key + "=%(" + key + ")s"
			else:
				sql_value += key + "=%(" + key + ")s,"

		sql_value = sql_value[:-1]

		sql = "UPDATE " + table_info["table"] + " SET " + sql_value + " WHERE " + sql_where
		return sql

	def createDelateSql(self, table_info):
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
		dummy = {id: 19}
		return dummy

	def create_time(self):
		return datetime.datetime.now()