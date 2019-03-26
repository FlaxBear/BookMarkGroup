import sys
from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_login import LoginManager, login_user, login_required
from flask_wtf import FlaskForm

import json

sys.path.append('./Model')
sys.path.append('./Validate')

from Validate import (numberingListValidate, numberingEditShowValidate, numberingEditUpdValidate
, userListValidate, userEditShowValidate, userEditUpdValidate
, groupFolderListValidate, groupFolderEditShowValidate, groupFolderEditUpdValidate
, authorityListValidate, authorityEditShowValidate, authorityEditUpdValidate
, createUserValidate, loginUserValidate)

from Model import userModel, groupFolderModel, numberingModel, authorityModel

import loginUser

app = Flask(__name__)
app.secret_key = 'aaaa'

login_maneger = LoginManager()
login_maneger.init_app(app)

# Admin
@app.route('/')
def root():
	return redirect(url_for("mastar"))

# Mastar
# @app.route('/mastar', methods=['GET', 'POST'])
# def mastar():
# 	form = FlaskForm()
# 	if request.method == "POST":
# 		model = loginUser.User()
# 		login_user(model)
# 		return redirect(url_for('mastarMenu'))
# 	else:
# 		return render_template('mastarLogin.html', form=form)

@app.route('/mastar/menu', methods=['GET', 'POST'])
def mastarMenu():
	form = FlaskForm()
	html = render_template('mastar.html', form=form)
	return html

@app.route('/mastar/numberingList', methods=['GET', 'POST'])
def numberingList():
	form = numberingListValidate.NumberingListValidate()
	model = numberingModel.NumberingModel()

	data, message = model.getList()
	html = render_template('numberingList.html', data=data, form=form)
	return html

@app.route('/mastar/numberingEdit', methods=['POST'])
def numberingEdit():
	model = numberingModel.NumberingModel()

	if request.method == "POST":
		if request.form["state"] == "SHOW":
			form = numberingEditShowValidate.NumberingEditShowValidate()
		else:
			form = numberingEditUpdValidate.NumberingEditUpdValidate()
			if form.validate_on_submit():
				if form.state.data == 'NEW':
					message, form.numbering_id.data = model.insertNumbering(form)
				elif form.state.data == 'UPD':
					message = model.updateNumbergin(form)
				elif form.state.data == 'DEL':
					message = model.delateNumbergin(form)
					form.numbering_id.data = '0'

		if form.numbering_id.data != '0':
			data, message = model.selectNumbering(form)
			html = render_template('numberingEdit.html', data=data[0], form=form)
		else:
			data = ['', '', '', '', '', '']
			html = render_template('numberingEdit.html', data=data, form=form)

	return html

@app.route('/mastar/groupFolderList',  methods=['GET', 'POST'])
def groupFolderList():
	form = groupFolderListValidate.GroupFolderValidate()
	model = groupFolderModel.GroupFolderModel()

	data, message = model.getList()
	html = render_template('groupFolderList.html', data=data, form=form)
	return html

@app.route('/mastar/groupFolderEdit', methods=['GET', 'POST'])
def groupFolderEdit():
	model = groupFolderModel.GroupFolderModel()

	if request.method == 'POST':
		if request.form["state"] == "SHOW":
			form = groupFolderEditShowValidate.GroupFolderEditShowValidate()
		else:
			form = groupFolderEditUpdValidate.GroupFolderUpdValidate()
			if form.validate_on_submit():
				if form.state.data == 'NEW':
					message, form.group_folder_id.data = model.insertGroupFolder(form)
				elif form.state.data == 'UPD':
					message = model.updateGroupFolder(form)
				elif form.state.data == 'DEL':
					message = model.delateGroupFolder(form)
					form.group_folder_id.data = '0'

		if form.group_folder_id.data != '0':
			data, message = model.selectGroupFolder(form)
			html = render_template('groupFolderEdit.html', data=data[0], form=form)
		else:
			data = ['', '', '', '', '', '', '']
			html = render_template('groupFolderEdit.html', data=data, form=form)
	return html

@app.route('/mastar/userList', methods=['GET', 'POST'])
def userList():
	form = userListValidate.UserListValidate()
	model = userModel.UserModel()

	data, message = model.getList()
	html = render_template('userList.html', data=data, form=form)
	return html

@app.route('/mastar/userEdit', methods=['POST'])
def userEdit():
	model = userModel.UserModel()

	if request.method == "POST":
		if request.form["state"] == "SHOW":
			form = userEditShowValidate.UserEditShowValidate()
		else:
			form = userEditUpdValidate.UserEditUpdValidate()
			if form.validate_on_submit():
				if form.state.data == 'NEW':
					message, form.user_id.data = model.insertUser(form)
				elif form.state.data == 'UPD':
					message = model.updateUser(form)
				elif form.state.data == 'DEL':
					message = model.delateUser(form)
					form.user_id.data = '0'

		if form.user_id.data != '0':
			data, message = model.selectUser(form)
			html = render_template('userEdit.html', data=data[0], form=form)
		else:
			data = ['', '', '', '', '']
			html = render_template('userEdit.html', data=data, form=form)
	return html

@app.route('/mastar/authorityList', methods=['GET', 'POST'])
def authorityList():
	form = authorityListValidate.AuthorityValidate()
	model = authorityModel.AuthorityModel()

	data, message = model.getList()
	
	html = render_template('authorityList.html', data=data, form=form)
	return html

@app.route('/mastar/authorityEdit', methods=['GET', 'POST'])
def authorityEdit():
	model = authorityModel.AuthorityModel()

	if request.method == "POST":
		if request.form["state"] == "SHOW":
			form = authorityEditShowValidate.AuthorityEditShowValidate()
		else:
			form = authorityEditUpdValidate.AuthorityEditUpdValidate()
			if form.validate_on_submit():
				if form.state.data == 'NEW':
					message, form.user_id.data, form.group_folder_id.data = model.insertAuthority(form)
				elif form.state.data == 'UPD':
					message = model.upadteAuthority(form)
				elif form.state.data == 'DEL':
					message = model.delateAuthority(form)
					form.user_id.data = '0'
					form.group_folder_id.data = '0'

		# ユーザリスト
		user_model = userModel.UserModel()
		user_list, message = user_model.getSelectList()
		# グループフォルダー
		groupFolder_model = groupFolderModel.GroupFolderModel()
		groupFolder_list, message = groupFolder_model.getSelectList()

		if form.user_id.data != '0' or form.group_folder_id.data != '0':
			data, message = model.selectAuthority(form)
			state_bit = []

			for shift in range(0, 5):
				if (int(data[0][2])>>shift) & 1:
					state_bit.append(True)
				else:
					state_bit.append(False)

			html = render_template('authorityEdit.html', data=data[0], user_list=user_list, groupFolder_list=groupFolder_list, state_bit=state_bit, form=form)
		else:
			data = ['', '', '', '', '', '']
			state_bit = [False, False, False, False, False]
			html = render_template('authorityEdit.html', data=data, user_list=user_list, groupFolder_list=groupFolder_list, state_bit=state_bit,form=form)
	return html

# Plugin
# Create User
@app.route('/createUser', methods=['GET','POST'])
def createUser():
	model = userModel.UserModel()
	form = None

	if request.method == "POST":
		if form.validate_on_submit():
			message, form.user_id.data = model.insertUser(form)

			if message != 'Complate':
				pass
			else:
				return redirect(url_for("loginUser"))
	else:
		return render_template('')


# Login User
@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
	pass

# Sync Folders
@app.route('/syncFolders', methods=['GET'])
def syncFolders():
	model = groupFolderModel.GroupFolderModel()
	form = None

	send_data = {}
	data = []
	message = ""
	json_data = {}

	if request.method == 'POST':
		if form.validate_on_submit():
			for value in form.folder_list.data:
				data, message = model.selectGroupFolder(value)
				f = open(data[3] + "/bookmarkList.json", "r")
				json_data = json.load(f)
				data += json_data
		else:
			message = "Error"
			json_data = {}
	else:
		message = "Error"
		json_data = {}
	
	send_data["message"] = message
	send_data["data"] = data

	return make_response(json.dumps(send_data, ensure_ascii=False))

# Create GroupFolder
@app.route('/createGroupFolder', methods=['POST'])
def createGroupFolder():
	model = groupFolderModel.GroupFolderModel()
	form = None

	send_data = {}
	message = ""
	name_id = {}

	if request.method == 'POST':
		if form.validate_on_submit():
			message, form.group_folder_id.data = model.insertGroupFolder(form)

			if message == "Complate":
				name_id["folder_id"] = form.group_folder_id.data
				name_id["folder_name"] = form.group_folder_name.data
			else:
				message = "Error"
				name_id["folder_id"] = 0
				name_id["folder_name"] = form.group_folder_name.data
		else:
			message = "Error"
			name_id["folder_id"] = 0
			name_id["folder_name"] = form.group_folder_name.data
	else:
		message = "Error"
		name_id["folder_id"] = 0
		name_id["folder_name"] = form.group_folder_name.data

	send_data["message"] = message
	send_data["data"] = name_id

	return make_response(json.dumps(send_data, ensure_ascii=False))

# Commit GroupFolder
@app.route('/commitGroupFolder', methods=['POST'])
def commitGroupFolder():
	model = groupFolderModel.GroupFolderModel()
	form = None

	send_data = {}
	message = ""
	json_data = {}

	if request.method == 'POST':
		if form.validate_on_submit():
			data, message = model.selectGroupFolder(form)
			f = open(data[3] + "/bookmarkList.json", "r")
			json_data = json.load(f)
		else:
			message = "Error"
			json_data = {}
	else:
		message = "Error"
		json_data = {}
	
	send_data["message"] = message
	send_data["data"] = json_data

	return make_response(json.dumps(send_data, ensure_ascii=False))

# Update GroupFolder
@app.route('/updateGroupFolder', methods=['POST'])
def updateGroupFolder():
	pass

# Delete GroupFolder
@app.route('/deleteGroupFolder', methods=['POST'])
def deleteGroupFolder():
	# バリデーション作成
	pass

# Setting GroupFolder
@app.route('/settingUser', methods=['POST'])
def settingShowUser():
	pass

# #Setting GroupFolder (Add user)
# @app.route('/settingAddUser', methods=['POST'])
# def settingAddUser():
# 	pass
	
# #Setting GroupFolder (Del usr)
# @app.route('/settginDelUser', methods=['POST'])
# def settingDelUser():
# 	pass

#Setting GroupFolder (Setting Authority)
@app.route('/settingSetAuthority', methods=['POST'])
def settingSetAuthority():
	pass

@app.route('/settingShowAuthority', methods=['POST'])
def settingShowAuthority():
	pass