# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError

class UserEditShowValidate(FlaskForm):
	state = HiddenField()
	user_id = HiddenField()

	def validate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザIDが選択されていません")
		if user_id.data != "0":
			pass
			#存在チェック