# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, ValidationError

class CreateGroupFolderValidate(FlaskForm):
	user_id = HiddenField("ユーザID")
	group_folder_name = StringField("グループフォルダー名")

	def validate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザーIDが存在しません")

		# 存在チェック

	def validate_group_folder_name(self, group_folder_name):
		if group_folder_name.data == "":
			raise ValidationError("グループフォルダー名を入力してください")

		if len(group_folder_name.data) > 20:
			raise ValidationError("グループフォルダー名は20文字以下にしてください")

		if if r"[^.!#$%&'*+\/=?^_`{|}~-]" in group_folder_name.data:
			raise ValidationError("グループフォルダー名に無効な記号が含まれています")

		