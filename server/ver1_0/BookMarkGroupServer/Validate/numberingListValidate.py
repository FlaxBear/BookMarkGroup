# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField,ValidationError

class NumberingListValidate(FlaskForm):
	numbering_id = HiddenField()
	state = HiddenField()
	