# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

class NumberingEditShowValidate(FlaskForm):
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