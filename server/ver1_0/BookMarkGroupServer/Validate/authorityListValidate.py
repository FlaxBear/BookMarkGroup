# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField,ValidationError

class AuthorityValidate(FlaskForm):
	user_id = HiddenField()
	group_folder_id = HiddenField()
	state = HiddenField()