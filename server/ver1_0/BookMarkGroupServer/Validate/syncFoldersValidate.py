# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError

class SyncFoldersValidate(FlaskForm):
	user_id = HiddenField("ユーザID")s

	def validate_user_id(self, user_id):
		if user_id.data == "":
			raise ValidationError("ユーザーIDが存在しません")

		# 存在チェック