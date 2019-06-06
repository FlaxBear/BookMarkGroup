# -*- coding: utf-8 -*-
"""This module is used when updateing the Admin User edit page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

from Model import adminUserModel

class AdminUserEditUpdValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_admin_user_id :
		Function that performs validation on admin_user_id

	validate_adminUser_name :
		Function that performs validation on adminUser_name

	validate_admin_user_login_id :
		Function that performs validation on admin_user_login_id

	validate_admin_user_password :
		Function that performs validation on admin_user_login_id

	"""
	def validate_admin_user_id(self, admin_user_id):
		"""
		Perform validation on admin_user_id

		Parameters
		----------
		admin_user_id : str
			admin_user_id data
		"""
		if admin_user_id.data == "":
			raise ValidationError("Administrator user ID is not selected")
		if admin_user_id.data != "0":
			model = adminUserModel.AdminUserModel()
			data = model.getLoginData(admin_user_id.data)
			if data == []:
				raise ValidationError("Not Found administrator user data")

	def validate_adminUser_name(self, admin_user_name):
		"""
		Perform validation on admin_user_name

		Parameters
		----------
		admin_user_name : str
			admin_user_name data
		"""
		if admin_user_name.data == "":
			raise ValidationError("Please enter admin username")
		if len(admin_user_name.data) > 20:
			raise ValidationError("Admin user should be within 20 characters")
		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in admin_user_name.data:
			raise ValidationError(r"The administrator username can not include.! # $% & '* + \ / =? ^ _ `{|} ~-.")

	def validate_admin_user_login_id(self, admin_user_login_id):
		"""
		Perform validation on admin_user_login_id

		Parameters
		----------
		admin_user_login_id : str
			admin_user_login_id data
		"""
		if admin_user_login_id.data == "":
			raise ValidationError("Please enter your login ID")

		if len(admin_user_login_id.data) > 100:
			raise ValidationError("Login ID should not exceed 100 characters")

		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in admin_user_login_id.data:
			raise ValidationError(r"Login ID does not include.! # $% & '* + \ / =? ^ _ `{|} ~-.")

		if admin_user_login_id.data != "0":
			model = adminUserModel.AdminUserModel()
			data = model.getLoginData(admin_user_login_id.data)
			if data == []:
				raise ValidationError("Not Found administrator user data")

	def validate_admin_user_password(self, admin_user_password):
		"""
		Perform validation on admin_user_password

		Parameters
		----------
		admin_user_password : str
			admin_user_password data
		"""
		if admin_user_password.data == "":
			raise ValidationError("Please enter your password")

		if len(admin_user_password.data) > 150:
			raise ValidationError("Password should not exceed 100 characters")
