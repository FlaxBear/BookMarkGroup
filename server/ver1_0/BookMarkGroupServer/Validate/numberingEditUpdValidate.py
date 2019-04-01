# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

class NumberingEditUpdValidate(FlaskForm):
	state = HiddenField()
	numbering_id = HiddenField()
	numbering_name = StringField()
	next_value = StringField()
	create_time = TimeField()
	update_time = TimeField()

	def validate_numbering_id(self, numbering_id):
		if numbering_id.data == "":
			raise ValidationError("採番IDが選択されていません")
		if numbering_id.data != "0":
			pass
			# 存在チェック
			
	def validate_numbering_name(self, numbering_name):
		if numbering_name.data == "":
			raise ValidationError("カラム名を入力してください")
		if len(numbering_name.data) > 20:
			raise ValidationError("カラム名は20文字以内にしてください")

	# def validate_next_value(self, next_value):
	# 	if next_value.data.isdecimal():
	# 		raise ValidationError("次回採番値は数値を入力してください")