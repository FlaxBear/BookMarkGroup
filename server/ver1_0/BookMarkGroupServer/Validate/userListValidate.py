# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField,ValidationError

class UserListValidate(FlaskForm):
	user_id = HiddenField()
	state = HiddenField()