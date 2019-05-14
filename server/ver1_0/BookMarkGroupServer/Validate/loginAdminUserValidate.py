# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError

class LoginAdminUserValidate(FlaskForm):
	admin_user_login_id = StringField()
	admin_user_password = StringField()

	def validate_admin_user_login_id(self, admin_user_login_id):
		if admin_user_login_id.data == "":
			raise ValidationError("ログインIDを入力してください")

		if len(admin_user_login_id.data) > 100:
			raise ValidationError("ログインIDは100文字以下にしてください")

	def validate_admin_user_password(self, admin_user_password):
		if admin_user_password.data == "":
			raise ValidationError("パスワードを入力してください")

		if len(admin_user_password.data) > 150:
			raise ValidationError("パスワードは100文字以下にしてください")