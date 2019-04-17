# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

class PluginGroupFolderCreateValidate(FlaskForm):
	group_folder_name = StringField()

	def validate_group_folder_name(self, group_folder_name):
		if group_folder_name.data == "":
			raise ValidationError("グループフォルダー名を入力してください")

		if len(group_folder_name.data) > 20:
			raise ValidationError("グループフォルダー名は20文字以内にしてください")

		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in group_folder_name.data:
			raise ValidationError(r"グループフォルダー名に.!#$%&'*+\/=?^_`{|}~-は含められません。")
