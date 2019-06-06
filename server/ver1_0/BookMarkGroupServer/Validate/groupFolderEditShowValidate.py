# -*- coding: utf-8 -*-
"""This module is used when updateing the Group Folder edit page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

from Model import groupFolderModel

class GroupFolderEditShowValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_state :
		Function that performs validation on state

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
