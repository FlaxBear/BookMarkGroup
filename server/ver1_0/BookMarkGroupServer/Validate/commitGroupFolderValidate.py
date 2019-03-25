# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError

class CommitGroupFolderValidate(FlaskForm):
	user_id = HiddenField("ユーザID")
	group_folder_id = HiddenField("グループフォルダーID")

	def validate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザーIDが存在しません")

		# 存在チェック

	def validate_group_folder_id(self, group_folder_id):
		if group_folder_id == "":
			raise ValidationError("グループフォルダーIDが存在していません")

		#存在チェック