# -*- coding: utf-8 -*-
"""This module is used when updateing the login page"""
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError

class LoginAdminUserValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_admin_user_login_id :
		Function that performs validation on admin_user_login_id

	validate_admin_user_password :
		Function that performs validation on admin_user_password

	"""

	def validate_admin_user_login_id(self, admin_user_login_id):
		"""
		Perform validation on admin_user_login_id

		Parameters
		----------
		admin_user_login_id : str
		"""
		if admin_user_login_id.data == "":
			raise ValidationError("Please enter your login ID")

		if len(admin_user_login_id.data) > 100:
			raise ValidationError("Login ID should not exceed 100 characters")

	def validate_admin_user_password(self, admin_user_password):
		if admin_user_password.data == "":
			raise ValidationError("Please enter your password")

		if len(admin_user_password.data) > 150:
			raise ValidationError("Password should not exceed 100 characters")