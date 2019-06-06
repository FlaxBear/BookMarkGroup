# -*- coding: utf-8 -*-
"""This module is used when displaying the Authority edit page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

from Model import userModel, groupFolderModel

class AuthorityEditShowValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_state :
		Function that performs validation on state

	validate_user_id :
		Function that performs validation on user_id

	validate_group_folder_id :
		Function that performs validation on group_folder_id

	"""
	def validate_state(self, state):
		"""
		Perform validation on state

		Parameters
		----------
		state : str

		"""
		if state.data == "":
			raise ValidationError("")

	def validate_user_id(self, user_id):
		"""
		Perform validation on admin_user_id

		Parameters
		----------
		admin_user_id : str
			admin_user_id data
		"""
		if user_id.data == "":
			raise ValidationError("User ID not selected")
		if user_id.data != "0":
			model = userModel.numberingModel()
			data = model.getData(user_id.data)
			if data == []:
				raise ValidationError("Not Found user data")

	def validate_group_folder_id(self, group_folder_id):
		"""
		Perform validation on admin_user_id

		Parameters
		----------
		group_folder_id : str
			group_folder_id data
		"""
		if group_folder_id.data == "":
			raise ValidationError("Group folder ID is not selected")
		if group_folder_id.data != "0":
			model = groupFolderModel.GroupFolderModel()
			data = model.getData(group_folder_id.data)
			if data == []:
				raise ValidationError("Not Found group folder data")
