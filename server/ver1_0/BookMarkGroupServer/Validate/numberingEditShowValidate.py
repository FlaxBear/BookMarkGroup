# -*- coding: utf-8 -*-
"""This module is used when updateing the numbering page"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TimeField, ValidationError

from Model import numberingModel

class NumberingEditShowValidate(FlaskForm):
	"""
	Specify a validation rule for each item and execute

	Functions
	----------
	validate_numbering_id :
		Function that performs validation on validate_numbering_id
	"""

	def validate_numbering_id(self, numbering_id):
		"""
		Perform validation on numbering_id

		Parameters
		----------
		numbering_id : str
		"""
		if numbering_id.data == "":
			raise ValidationError("Numbering ID not selected")
		if numbering_id.data != "0":
			model = numberingModel.NumberingModel()
			data = model.getData(numbering_id.data)
			if data == []:
				raise ValidationError("Not Found numbering data")
