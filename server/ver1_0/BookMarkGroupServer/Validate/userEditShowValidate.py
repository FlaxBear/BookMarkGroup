# -*- coding: utf-8 -*-
"""This module is used when updateing the user edit page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError

class UserEditShowValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_user_id :
		Function that performs validation on user_id

	"""

	def validate_user_id(self, user_id):
		"""
		Perform validation on user_id

		Parameters
		----------
		user_id : str
		"""
		if user_id.data == "":
			raise ValidationError("User ID not selected")
		if user_id.data != "0":
			pass
			#存在チェック