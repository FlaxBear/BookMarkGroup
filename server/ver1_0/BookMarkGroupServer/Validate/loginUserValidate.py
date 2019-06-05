# -*- coding: utf-8 -*-
"""This module is used when updateing the login User page"""
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError

class LoginUserValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_login_mail :
		Function that performs validation on login_mail

	validate_password :
		Function that performs validation on password

	"""

	def validate_login_mail(self, login_mail):
		"""
		Perform validation on login_mail

		Parameters
		----------
		login_mail : str

		"""

		if login_mail.data == "":
			raise ValidationError("Please enter your e-mail address")

		if len(login_mail.data) > 100:
			raise ValidationError("Email address should not exceed 100 characters")

		if r"/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" in login_mail.data:
			raise ValidationError("Please enter email address format")

	def validate_password(self, password):
		"""
		Perform validation on password

		Parameters
		----------
		password : str

		"""

		if password.data == "":
			raise ValidationError("Please enter your password")

		if len(password.data) > 150:
			raise ValidationError("Password should not exceed 100 characters")