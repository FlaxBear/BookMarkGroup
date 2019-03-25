# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, ValidationError

class SettingAuthoritySet(FlaskForm):
	user_id = HiddenField("ユーザID")
	# 権限の状態のバリデーションが未作成

	def validate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザIDが存在しません")
		# 存在チェック