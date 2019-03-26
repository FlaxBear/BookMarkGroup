# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

class UserEditShowValidate(FlaskForm):
	state = HiddenField()
	user_id = HiddenField()

	def validate_state(self, state):
		if state.data == "":
			raise ValidationError("")

	def validate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザIDが選択されていません")
		if user_id.data != "0":
			pass
			#存在チェック