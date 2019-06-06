# -*- coding: utf-8 -*-
"""This module is used when displaying the Admin User edit page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError

from Model import adminUserModel

class AdminUserEditShowValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_admin_user_id :
		Function that performs validation on admin_user_id

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
			data = model.getData(admin_user_id.data)
			if data == []:
				raise ValidationError("Not Found administrator user data")