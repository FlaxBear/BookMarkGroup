# -*- coding: utf-8 -*-
"""This module is used when updateing the user edit page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

from Model import userModel

class UserEditUpdValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_state :
		Function that performs validation on state

	validate_user_id :
		Function that performs validation on user_id

	validate_user_name :
		Function that performs validation on user_name

	validate_user_mail_address :
		Function that performs validation on user_mail_address

	validate_user_password:
		Function that performs validation on user_password
	"""

	def validate_state(self, state):
		"""
		Perform validation on

		Parameters
		----------
		: str
		"""
		if state.data == "":
			raise ValidationError("")

	def validate_user_id(self, user_id):
		"""
		Perform validation on user_id

		Parameters
		----------
		user_id : str
		"""
		if user_id.data == "":
			raise ValidationError("ユーザIDが選択されていません")
		if user_id.data != "0":
			model = userModel.UserModel()
			data = model.getData(user_id.data)
			if data == []:
				raise ValidationError("Not Found user data")

	def validate_user_name(self, user_name):
		"""
		Perform validation on user_name

		Parameters
		----------
		user_name : str
		"""
		if user_name.data == "":
			raise ValidationError("ユーザ名を入力して下さい")
		if len(user_name.data) > 20:
			raise ValidationError("ユーザ名は20文字以内にしてください")
		if r"[^.!#$%&'*+\/=?^_`{|}~-]" in user_name.data:
			raise ValidationError(r"ユーザ名に.!#$%&'*+\/=?^_`{|}~-は含められません。")

	def validate_user_mail_address(self, user_mail_address):
		"""
		Perform validation on user_mail_address

		Parameters
		----------
		user_mail_address : str
		"""
		if user_mail_address.data == "":
			raise ValidationError("メールアドレスを入力してください")

		if len(user_mail_address.data) > 100:
			raise ValidationError("メールアドレスは100文字以下にしてください")

		if r"/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" in user_mail_address.data:
			raise ValidationError("メールアドレス形式の入力してください")

		model = userModel.UserModel()
		data = model.getLoginData(user_mail_address.data)
		if data != []:
			raise ValidationError("Already user data")

	def validate_user_password(self, user_password):
		"""
		Perform validation on user_password

		Parameters
		----------
		user_password : str
		"""
		if user_password.data == "":
			raise ValidationError("パスワードを入力してください")

		if len(user_password.data) > 150:
			raise ValidationError("パスワードは100文字以下にしてください")