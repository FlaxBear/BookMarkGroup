# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, ValidationError, PasswordField

class CreateUserValidate(FlaskForm):
	user_name = StringField("ユーザ名")
	user_mail_address = StringField("メールアドレス")
	user_password = PasswordField("パスワード")

	def validate_user_name(self, user_name):
		if user_name.data == "":			
			raise ValidationError("ユーザ名を入力してください")

		if len(user_name.data) > 20:
			raise ValidationError("ユーザ名は10文字以下にしてください")

		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in user_name.data:
			raise ValidationError(r"ユーザ名に.!#$%&'*+\/=?^_`{|}~-は含められません。")

	def validate_user_mail_address(self, user_mail_address):
		if user_mail_address.data == "":
			raise ValidationError("メールアドレスを入力してください")

		if len(user_mail_address.data) > 100:
			raise ValidationError("メールアドレスは100文字以下にしてください")

		if r"/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" in user_mail_address.data:
			raise ValidationError("メールアドレス形式の入力してください")

		# メールアドレスの重複チェック
		
	def validate_user_password(self, user_password):
		if user_password.data == "":
			raise ValidationError("パスワードを入力してください")

		if len(user_password.data) > 150:
			raise ValidationError("パスワードは100文字以下にしてください")