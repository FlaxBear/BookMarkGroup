# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError

class LoginUserValidate(FlaskForm):
	login_mail = StringField()
	password = StringField()

	def validate_login_mail(self, login_mail)
		if login_mail.data == "":
			raise ValidationError("メールアドレスを入力してください")

		if len(login_mail.data) > 100:
			raise ValidationError("メールアドレスは100文字以下にしてください")

		if r"/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" in user_mail_address.data:
			raise ValidationError("メールアドレス形式の入力してください")

	def validate_password(self, password)
		if user_password.data == "":
			raise ValidationError("パスワードを入力してください")

		if len(user_password.data) > 150:
			raise ValidationError("パスワードは100文字以下にしてください")