# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, ValidationError

class LoginUserValidate(FlaskForm):
	user_mail_address = StringField("ユーザ名")
	user_password = StringField("パスワード")

	def validate_user_mail_address(self, user_mail_address):
		if user_mail_address.data == "":
			raise ValidationError("メールアドレスを入力してください")

		if len(user_mail_address.data) > 100:
			raise ValidationError("メールアドレスは100文字以下にしてください")

		if r"/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" in user_mail_address.data:
			raise ValidationError("メールアドレス形式の入力してください")

	def validate_user_password(self, user_password):
		if user_password.data == "":
			raise ValidationError("パスワードを入力してください")

		if len(user_password.data) > 150:
			raise ValidationError("パスワードは100文字以下にしてください")