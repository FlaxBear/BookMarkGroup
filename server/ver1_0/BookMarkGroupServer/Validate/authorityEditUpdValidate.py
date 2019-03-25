# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField, TimeField, ValidationError

class AuthorityEditUpdValidate(FlaskForm):
	state = HiddenField()
	user_id = HiddenField()
	group_folder_id = HiddenField()
	authority_state = IntegerField()
	create_time = TimeField()
	update_time = TimeField()

	def validate_state(self, state):
		if state.data == "":
			raise ValidationError("")

	def validate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザIDが選択されていません")
		if user_id.data != "0":
			pass
			# 存在チェック

	def validate_group_folder_id(self, group_folder_id):
		if group_folder_id.data == "":
			raise ValidationError("グループフォルダーIDが選択されていません")
		if group_folder_id.data != "0":
			pass
			# 存在チェック
		