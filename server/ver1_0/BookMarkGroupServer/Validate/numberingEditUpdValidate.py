# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

class NumberingEditUpdValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_numbering_id :
		Function that performs validation on numbering_id

	validate_numbering_name :
		Function that performs validation on numbering_name

	"""

	def validate_numbering_id(self, numbering_id):
		"""
		Perform validation on numbering_id

		Parameters
		----------
		numbering_id : str
		"""
		if numbering_id.data == "":
			raise ValidationError("Numbering ID not selected")
		if numbering_id.data != "0":
			pass
			# 存在チェック

	def validate_numbering_name(self, numbering_name):
		"""
		Perform validation on numbering_name
		"""
		if numbering_name.data == "":
			raise ValidationError("Please enter a column name")
		if len(numbering_name.data) > 20:
			raise ValidationError("Column name must be 20 characters or less")

	# def validate_next_value(self, next_value):
	# 	if next_value.data.isdecimal():
	# 		raise ValidationError("次回採番値は数値を入力してください")