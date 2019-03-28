# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError

class AdminUserEditShowValidate(FlaskForm):
	state = HiddenField()
	admin_user_id = HiddenField()

	def validate_admin_user_id(self, admin_user_id):
		if admin_user_id.data == "":
			raise ValidationError("管理者ユーザIDが選択されていません")
		if admin_user_id != "0":
			pass
			#存在チェック