# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

class GroupFolderUpdValidate(FlaskForm):
	state = HiddenField()
	group_folder_id = HiddenField()
	group_folder_name = StringField()
	group_folder_version = StringField()
	json_directory_path = StringField()
	group_folder_memo = StringField()
	create_time = TimeField()
	update_time = TimeField()

	def validate_group_folder_id(self, group_folder_id):
		if group_folder_id.data == "":
			raise ValidationError("グループフォルダーIDが選択されていません")
		if group_folder_id.data != "0":
			pass
			# 存在チェック
			
	def validate_group_folder_name(self, group_folder_name):
		if group_folder_name.data == "":
			raise ValidationError("グループフォルダー名を入力してください")

		if len(group_folder_name.data) > 20:
			raise ValidationError("グループフォルダー名は20文字以内にしてください")

		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in group_folder_name.data:
			raise ValidationError(r"グループフォルダー名に.!#$%&'*+\/=?^_`{|}~-は含められません。")

	def validate_group_folder_version(self, group_folder_version):
		if group_folder_version.data == "":
			raise ValidationError("グループフォルダーバージョンを入力してください")
		# if group_folder_version.data.isdigit():
		# 	raise ValidationError("グループフォルダーバージョンは数値で設定してください")

	def validate_group_folder_memo(self, group_folder_memo):
		if len(group_folder_memo.data) > 200:
			raise ValidationError("備考は200文字内で入力してください")