# -*- coding: utf-8 -*-
"""This module is used when updateing the Group Folder edit page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

from Model import groupFolderModel

class GroupFolderUpdValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_group_folder_id :
		Function that performs validation on group_folder_id

	validate_group_folder_name :
		Function that performs validation on group_folder_name

	validate_group_folder_version :
		Function that performs validation on group_folder_version

	validate_group_folder_memo :
		Function that performs validation on group_folder_memo

	"""

	def validate_group_folder_id(self, group_folder_id):
		"""
		Perform validation on group_folder_id

		Parameters
		----------
		group_folder_id : str
		"""
		if group_folder_id.data == "":
			raise ValidationError("Group folder ID is not selected")
		if group_folder_id.data != "0":
			model = groupFolderModel.GroupFolderModel()
			data = model.getData(group_folder_id.data)
			if data == []:
				raise ValidationError("Not Found group folder data")


	def validate_group_folder_name(self, group_folder_name):
		"""
		Perform validation on group_folder_name

		Parameters
		----------
		group_folder_name : str
		"""
		if group_folder_name.data == "":
			raise ValidationError("Please enter a group folder name")

		if len(group_folder_name.data) > 20:
			raise ValidationError("Group folder name must be 20 characters or less")

		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in group_folder_name.data:
			raise ValidationError(r"Group folder names can not contain.! # $% & '* + \ / =? ^ _ `{|} ~-.")

	def validate_group_folder_version(self, group_folder_version):
		"""
		Perform validation on group_folder_version

		Parameters
		----------
		group_folder_version : str
			group_folder_version data
		"""
		if group_folder_version.data == "":
			raise ValidationError("Please enter group folder version")
		# if group_folder_version.data.isdigit():
		# 	raise ValidationError("グループフォルダーバージョンは数値で設定してください")

	def validate_group_folder_memo(self, group_folder_memo):
		"""
		Perform validation on group_folder_memo

		Parameters
		----------
		group_folder_memo : str
			group_folder_memo data
		"""
		if len(group_folder_memo.data) > 200:
			raise ValidationError("Please enter remarks within 200 characters")