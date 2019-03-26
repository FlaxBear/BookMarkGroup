# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, ValidationError

class SettingShowUserAdd(FlaskForm):
	user_id = HiddenField("ユーザID")
	user_mail_address = StringField("メールアドレス")

	def valiate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザIDが存在しません")
		# 存在チェック

	def validate_user_mail_address(self, user_mail_address):
		if user_mail_address.data == "":
			raise ValidationError("メールアドレスを入力してください")

		if len(user_mail_address.data) > 100:
			raise ValidationError("メールアドレスは100文字以下にしてください")

		if r"/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" in user_mail_address.data:
			raise ValidationError("メールアドレス形式の入力してください")

		# 存在チェック

