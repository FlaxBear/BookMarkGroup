# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import HiddenField,ValidationError

class GroupFolderValidate(FlaskForm):
	group_folder_id = HiddenField()
	state = HiddenField()
	