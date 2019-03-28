# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

class AdminUserEditUpdValidate(FlaskForm):
	state = HiddenField()
	admin_user_id = HiddenField()
	admin_user_name = StringField()
	admin_user_login_id = StringField()
	admin_user_password = StringField()


	def validate_admin_user_id(self, admin_user_id):
		if admin_user_id.data == "":
			raise ValidationError("管理者ユーザIDが選択されていません")
		if admin_user_id.data != "0":
			pass
			#存在チェック

	def validate_adminUser_name(self, admin_user_name):
		if admin_user_name.data == "":
			raise ValidationError("管理者ユーザ名を入力してください")
		if len(admin_user_name.data) > 20:
			raise ValidationError("管理者ユーザは20文字以内にしてください")
		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in admin_user_name.data:
			raise ValidationError(r"管理者ユーザ名に.!#$%&'*+\/=?^_`{|}~-は含められません。")

	def validate_admin_user_login_id(self, admin_user_login_id):
		if admin_user_login_id.data == "":
			raise ValidationError("ログインIDを入力してください")

		if len(admin_user_login_id.data) > 100:
			raise ValidationError("ログインIDは100文字以下にしてください")

		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in admin_user_login_id.data:
			raise ValidationError(r"ログインIDに.!#$%&'*+\/=?^_`{|}~-は含められません。")

		# ログインIDの重複チェック

	def validate_admin_user_password(self, admin_user_password):
		if admin_user_password.data == "":
			raise ValidationError("パスワードを入力してください")

		if len(admin_user_password.data) > 150:
			raise ValidationError("パスワードは100文字以下にしてください")
