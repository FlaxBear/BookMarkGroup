# -*- coding: utf-8 -*-
""" """
# modules
import sys, json
from flask import Flask, render_template, redirect, url_for, request, make_response, session, jsonify, json
from flask_login import LoginManager, login_user, login_required
from flask_wtf import FlaskForm
from flask_sslify import SSLify
from flask_cors import CORS
import ssl

# add modules
sys.path.append('./Model')
sys.path.append('./Validate')

from Validate import (loginAdminUserValidate
, adminUserEditShowValidate, adminUserEditUpdValidate
, numberingEditShowValidate, numberingEditUpdValidate
, userEditShowValidate, userEditUpdValidate
, groupFolderEditShowValidate, groupFolderEditUpdValidate
, authorityEditShowValidate, authorityEditUpdValidate
, loginUserValidate
)
from Model import adminUserModel, userModel, groupFolderModel, numberingModel, authorityModel

app = Flask(__name__)
app.secret_key = 'aaaa'
# SSLify(app)
CORS(app)

login_maneger = LoginManager()
login_maneger.init_app(app)

""" Functions required for Admin Page """
"""====================================================================================================================================================================================================="""
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response

@login_maneger.user_loader
def user_loader(user_id):
	pass

@login_maneger.request_loader
def request_loader(request):
	pass

def login_admin_user_check(session):
	check = False
	if 'admin_user_id' in session and 'admin_user_login_id' in session:
		model = adminUserModel.AdminUserModel()
		select_data, message = model.getLoginData(session['admin_user_login_id'])

		if (message == "Complate") and (select_data[0][0] == session['admin_user_id']):
			check = True

	return check
"""====================================================================================================================================================================================================="""

""" Admin Page """
"""====================================================================================================================================================================================================="""
@app.route('/')
def root():
	"""
	Root path
	Move to login page

	Returns
	-------
	html : Response
		Processing performed by mastar()
	"""
	html = redirect(url_for("mastar"))
	return html

# Login Page
@app.route('/mastar', methods=['GET', 'POST'])
def mastar():
	"""
	/mastar path
	Perform login page processing
	"""
	message = ''
	result = ''

	if request.method == "POST":
		# Login process
		form = loginAdminUserValidate.LoginAdminUserValidate()

		# Check request data
		if form.validate_on_submit() == True:
			# If there is no error in the request data
			model = adminUserModel.AdminUserModel()
			select_data, result = model.getLoginData(form.admin_user_login_id.data) # Get Logiguser data
			crypto_password = model.safty_password(select_data[0][0], form.admin_user_password.data) # Encrypt entered password

			# Check password
			if select_data[0][2] == crypto_password:
				# If the password is the same
				# Set login information in session
				session['admin_user_id'] = select_data[0][0]
				session['admin_user_login_id'] = select_data[0][1]
				return redirect(url_for('mastarMenu'))

			else:
				# If the password is not the same
				message = "Don't User or Password"
				return render_template('mastarLogin.html', form=form, message=message)

		else:
			# If there is error in the request data
			# Create error message
			for error in form.admin_user_login_id.errors:
				message += error + '<br>'
			for error in form.admin_user_password.errors:
				message += error + '<br>'
			return render_template('mastarLogin.html', form=form, message=message)

	else:
		# Show login page
		form = FlaskForm()
		return render_template('mastarLogin.html', form=form, message=message)

# Admin Menu
@app.route('/mastar/menu', methods=['GET', 'POST'])
def mastarMenu():
	"""
	/mastar/menu path
	Show menu page
	"""

	model = adminUserModel.AdminUserModel()
	form = FlaskForm()

	# Check Login User
	if login_admin_user_check(session):
		html = render_template('mastarMenu.html', form=form)
	else:
		html = redirect(url_for('mastar'))

	return html

# AdminUser List
@app.route('/mastar/adminUserList', methods=['GET', 'POST'])
def adminUserList():
	"""
	/mastar/adminUserList path
	Show adminUserList page
	"""
	form = FlaskForm()
	model = adminUserModel.AdminUserModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		data, result = model.getList()

		if result == "Complate":
			html = render_template('mastarAdminUserList.html', data=data, form=form, message=message)
		else:
			message["state"] = "Error"
			message["message"] = result
			html = render_template('errorPage.html', message=message)
	else:
		html = redirect(url_for('mastar'))

	return html

# AdminUser Edit
@app.route('/mastar/adminUserEdit', methods=['POST'])
def adminUserEdit():
	"""
	/mastar/adminUserEdit path
	Show adminUserEdit page
	"""

	model = adminUserModel.AdminUserModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		if request.method == "POST":

			# Validate
			if request.form["state"] == "SHOW":
				# Validation for data display
				form = adminUserEditShowValidate.AdminUserEditShowValidate()

				if form.validate_on_submit() == False:
					message["state"] = "Error"
					message["message"] = form.admin_user_id.errors
					return redirect(url_for("adminUserList"))

			else:
				# Validation for data update
				form = adminUserEditUpdValidate.AdminUserEditUpdValidate()

				if form.validate_on_submit():

					if form.state.data == 'NEW':
						# Add data
						result, form.admin_user_id.data = model.insertAdminUser(form)

					elif form.state.data == 'UPD':
						# Update data
						result = model.updateAdminUser(form)

					elif form.state.data == 'DEL':
						# Delete data
						result = model.delateAdminUser(form)
						form.admin_user_id.data = '0'

					if result != "Complate":
						message["state"] = "Error"
						message["message"] = result

				else:
					# Show Error Message
					message["state"] = "Error"
					for error in form.admin_user_id.errors:
						message["message"] += error + "<br>"
					for error in form.admin_user_name.errors:
						message["message"] += error + "<br>"
					for error in form.admin_user_login_id.errors:
						message["message"] += error + "<br>"
					for error in form.admin_user_password.errors:
						message["message"] += error + "<br>"


		if form.admin_user_id.data != '0':
			# Show Edit Page
			data, result = model.selectAdminUser(form)

			if result == "Complate":
				html = render_template('mastarAdminUserEdit.html', data=data[0], form=form)
			else:
				message["state"] = "Error"
				message["message"] = result
				html = render_template('mastarAdminUserEdit.html', data=data[0], form=form)
		else:
			# Show Edit New Page
			data = ['', '', '', '', '']
			html = render_template('mastarAdminUserEdit.html', data=data, form=form)
	else:
		html = redirect(url_for('mastar'))

	return html

# Numbering List
@app.route('/mastar/numberingList', methods=['GET', 'POST'])
def numberingList():
	"""
	/mastar/numberingList path
	Show numberingList page
	"""
	form = FlaskForm()
	model = numberingModel.NumberingModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		data, result = model.getList()

		if result == "Complate":
			html = render_template('mastarNumberingList.html', data=data, form=form, message=message)
		else:
			message["state"] = "Error"
			message["message"] = result
			html = render_template('errorPage.html', message=message)
	else:
		html = redirect(url_for('mastar'))

	return html

# Numbering Edit
@app.route('/mastar/numberingEdit', methods=['POST'])
def numberingEdit():
	"""
	/mastar/numberingEdit path
	Show numberingEit page
	"""

	model = numberingModel.NumberingModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		if request.method == "POST":

			# Validate
			if request.form["state"] == "SHOW":
				# Validation for data display
				form = numberingEditShowValidate.NumberingEditShowValidate()

				if form.validate_on_submit() == False:
					message["state"] = "Error"
					message["message"] = form.numbering_id.errors
					return redirect(url_for("numberingList"))
			else:
				# Validation for data update
				form = numberingEditUpdValidate.NumberingEditUpdValidate()

				if form.validate_on_submit():

					if form.state.data == 'NEW':
						# Add data
						result, form.numbering_id.data = model.insertNumbering(form)

					elif form.state.data == 'UPD':
						# Update data
						result = model.updateNumbergin(form)

					elif form.state.data == 'DEL':
						# Delete data
						result = model.delateNumbergin(form)
						form.numbering_id.data = '0'

					if result != "Complate":
						message["state"] = "Error"
						message["message"] = result

				else:
					# Show Error Message
					message["state"] = "Error"
					for error in form.numbering_id.errors:
						message["message"] += error + "<br>"
					for error in form.numbering_name.errors:
						message["message"] += error + "<br>"
					for error in form.next_value.errors:
						message["message"] += error + "<br>"

			if form.numbering_id.data != '0':
				# Show Edit Page
				data, result = model.selectNumbering(form)

				if result == "Complate":
					html = render_template('mastarNumberingEdit.html', data=data[0], form=form, message=message)
				else:
					message["state"] = "Error"
					message["message"] = result
					html = render_template('mastarNumberingList.html', data=data, form=form, message=message)
			else:
				# Show Edit New Page
				data = ['', '', '', '', '', '']
				html = render_template('mastarNumberingEdit.html', data=data, form=form, message=message)
	else:
		html = redirect(url_for('mastar'))

	return html

# User List
@app.route('/mastar/userList', methods=['GET', 'POST'])
def userList():
	"""
	/mastar/userList path
	Show userList page
	"""
	form = FlaskForm()
	model = userModel.UserModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		data, result = model.getList()

		if result == "Complate":
			html = render_template('mastarUserList.html', data=data, form=form)
		else:
			message["state"] = "Error"
			message["message"] = result
			html = render_template('errorPage.html', message=message)
	else:
		html = redirect(url_for('mastar'))

	return html

# User Edit
@app.route('/mastar/userEdit', methods=['POST'])
def userEdit():
	"""
	/mastar/userEidt path
	Show userEdit page
	"""

	model = userModel.UserModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		if request.method == "POST":

			# Validate
			if request.form["state"] == "SHOW":
				# Validation for data display
				form = userEditShowValidate.UserEditShowValidate()

				if form.validate_on_submit() == False:
					message["state"] = "Error"
					message["message"] = form.user_id.errors
					return redirect(url_for("userList"))

			else:
				# Validation for data update
				form = userEditUpdValidate.UserEditUpdValidate()

				if form.validate_on_submit():

					if form.state.data == 'NEW':
						# Add data
						result, form.user_id.data = model.insertUser(form)

					elif form.state.data == 'UPD':
						# Update data
						result = model.updateUser(form)

					elif form.state.data == 'DEL':
						# Delete data
						result = model.delateUser(form)
						form.user_id.data = '0'

					if result != "Complate":
						message["state"] = "Error"
						message["message"] = result

				else:
					# Show Error Message
					message["state"] = "Error"
					for error in form.user_id.errors:
						message["message"] += error + "<br>"
					for error in form.user_name.errors:
						message["message"] += error + "<br>"
					for error in form.user_mail_address.errors:
						message["message"] += error + "<br>"
					for error in form.user_password.errors:
						message["message"] += error + "<br>"

			if form.user_id.data != '0':
				# Show Edit Page
				data, result = model.selectUser(form)

				if result == "Complate":
					html = render_template('mastarUserEdit.html', data=data[0], form=form)
				else:
					message["state"] = "Error"
					message["message"] = result
					html = render_template('mastarUserEdit.html', data=data[0], form=form)
			else:
				# Show Edit New Page
				data = ['', '', '', '', '']
				html = render_template('mastarUserEdit.html', data=data, form=form)
	else:
		html = redirect(url_for('mastar'))

	return html

# GroupFolder List
@app.route('/mastar/groupFolderList',  methods=['GET', 'POST'])
def groupFolderList():
	"""
	/mastar/groupFolderList path
	Show groupFolder page
	"""
	form = FlaskForm()
	model = groupFolderModel.GroupFolderModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		data, result = model.getList()

		if result == "Complate":
			html = render_template('mastarGroupFolderList.html', data=data, form=form, message=message)
		else:
			message["state"] = "Error"
			message["message"] = result
			html = render_template('errorPage.html', message=message)
	else:
		html = redirect(url_for('mastar'))

	return html

# GroupFolder Edit
@app.route('/mastar/groupFolderEdit', methods=['GET', 'POST'])
def groupFolderEdit():
	"""
	/mastar/groupFolderEdit path
	Show groupFolder page
	"""
	model = groupFolderModel.GroupFolderModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		if request.method == 'POST':

			# Validate
			if request.form["state"] == "SHOW":
				# Validation for data display
				form = groupFolderEditShowValidate.GroupFolderEditShowValidate()

				if form.validate_on_submit() == False:
					message["state"] = "Error"
					message["message"] = form.group_folder_id.errors
					return redirect(url_for("groupFolderList"))
			else:
				# Validation for data update
				form = groupFolderEditUpdValidate.GroupFolderUpdValidate()

				if form.validate_on_submit():

					if form.state.data == 'NEW':
						# Add data
						result, form.group_folder_id.data = model.insertGroupFolder(form)

					elif form.state.data == 'UPD':
						# Update data
						result = model.updateGroupFolder(form)

					elif form.state.data == 'DEL':
						# Delete data
						result = model.delateGroupFolder(form)
						form.group_folder_id.data = '0'

					if result != "Complate":
						message["state"] = "Error"
						message["message"] = result

				else:
					# Show Error Message
					message["state"] = "Error"
					for error in form.group_folder_id.errors:
						message["message"] += error + "<br>"
					for error in form.group_folder_name.errors:
						message["message"] += error + "<br>"
					for error in form.group_folder_version.errors:
						message["message"] += error + "<br>"
					for error in form.group_folder_memo.errors:
						message["message"] += error + "<br>"

			if form.group_folder_id.data != '0':
				# Show Edit Page
				data, result = model.selectGroupFolder(form)

				if result == "Complate":
					html = render_template('mastarGroupFolderEdit.html', data=data[0], form=form)
				else:
					message["state"] = "Error"
					message["message"] = result
					html = render_template('mastarGroupFolderEdit.html', data=data[0], form=form)
			else:
				# Show Edit New Page
				data = ['', '', '', '', '', '', '']
				html = render_template('mastarGroupFolderEdit.html', data=data, form=form)
	else:
		html = redirect(url_for('mastar'))

	return html

# Authoriry List
@app.route('/mastar/authorityList', methods=['GET', 'POST'])
def authorityList():
	"""
	/mastar/authorityList path
	Show authorityList page
	"""
	form = FlaskForm()
	model = authorityModel.AuthorityModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		data, result = model.getList()

		if result == "Complate":
			html = render_template('mastarAuthorityList.html', data=data, form=form)
		else:
			message["state"] = "Error"
			message["message"] = result
			html = render_template('errorPage.html', message=message)
	else:
		html = redirect(url_for('mastar'))

	return html

# Authoriy Edit
@app.route('/mastar/authorityEdit', methods=['GET', 'POST'])
def authorityEdit():
	"""
	/mastar/authorityEdit path
	Show authorityEdit page
	"""
	model = authorityModel.AuthorityModel()
	message = {
		"state": "",
		"message": ""
	}

	# Check Login User
	if login_admin_user_check(session):
		if request.method == "POST":

			# Validate
			if request.form["state"] == "SHOW":
				# Validation for data display
				form = authorityEditShowValidate.AuthorityEditShowValidate()

				if form.validate_on_submit() == False:
					message["state"] = "Error"
					message["message"] += form.user_id.errors
					message["message"] += form.group_folder_id.errors
					return redirect(url_for("authorityList"))
			else:
				# Validation for data update
				form = authorityEditUpdValidate.AuthorityEditUpdValidate()

				if form.validate_on_submit():

					if form.state.data == 'NEW':
						# Add data
						result, form.user_id.data, form.group_folder_id.data = model.insertAuthority(form)

					elif form.state.data == 'UPD':
						# Update data
						result = model.upadteAuthority(form)

					elif form.state.data == 'DEL':
						# Delete data
						result = model.delateAuthority(form)
						form.user_id.data = '0'
						form.group_folder_id.data = '0'

					if result != "Complate":
						message["state"] = "Error"
						message["message"] = result

				else:
					# Show Error Message
					message["state"] = "Error"
					for error in form.user_id.errors:
						message["message"] += error + "<br>"
					for error in form.group_folder_id.errors:
						message["message"] += error + "<br>"

			# Get User List
			user_model = userModel.UserModel()
			user_list, message = user_model.getSelectList()
			# Get GroupFolder List
			groupFolder_model = groupFolderModel.GroupFolderModel()
			groupFolder_list, message = groupFolder_model.getSelectList()

			if form.user_id.data != '0' or form.group_folder_id.data != '0':
				# Show Edit Page
				data, result = model.selectAuthority(form)
				state_bit = []

				if result == "Complate":
					# Restore using shift because you save the authority in bits
					for shift in range(0, 5):
						if (int(data[0][2])>>shift) & 1:
							state_bit.append(True)
						else:
							state_bit.append(False)

					html = render_template('mastarAuthorityEdit.html', data=data[0], user_list=user_list, groupFolder_list=groupFolder_list, state_bit=state_bit, form=form)

				else:
					message["state"] = "Error"
					message["message"] = result
					html = render_template('mastarAuthorityEdit.html', data=data[0], user_list=user_list, groupFolder_list=groupFolder_list, state_bit=state_bit, form=form)
			else:
				# Show Edit New Page
				data = ['', '', '', '', '', '']
				state_bit = [False, False, False, False, False]
				html = render_template('mastarAuthorityEdit.html', data=data, user_list=user_list, groupFolder_list=groupFolder_list, state_bit=state_bit,form=form)
	else:
		html = redirect(url_for('mastar'))

	return html

# Logout
@app.route('/mastar/logout', methods=['GET', 'POST'])
def logout():
	"""
	/mastar/logout path
	Logout process
	"""
	session.pop('admin_user_id', None)
	session.pop('admin_user_login_id', None)
	return redirect(url_for('mastar'))
"""====================================================================================================================================================================================================="""


""" Functions required for Plugin """
"""====================================================================================================================================================================================================="""
def create_new_json_file(group_folder_id, group_folder_name):
	"""
		Create a new json file in a folder
	"""
	json_data = {
		"bookmark_id": group_folder_id,
		"bookmark_name": group_folder_name,
		"bookmark":{}
	}

	# Created in json_data folder
	folder_path = "json_data\\" + str(group_folder_id) + "_" + group_folder_name + ".json"

	with open(folder_path, 'w') as f:
		json.dump(json_data, f, ensure_ascii=False)

	return

def create_update_json_file(json_bookmark, select_data):
	"""
		Update json file
	"""
	json_data = {
		"bookmark_id": select_data[0][0],
		"bookmark_name": select_data[0][1],
		"bookmark" : {}
	}
	for value in json_bookmark["bookmark"]:
		# Create data to save
		json_data["bookmark"][str(value)] = json_bookmark["bookmark"][str(value)]

	folder_path = "json_data\\" + select_data[0][3] + ".json"

	with open(folder_path, 'w') as f:
		json.dump(json_data, f, ensure_ascii=False)

	return

def input_json_file(group_folder_path):
	"""
	Get json file data
	"""
	folder_path = "json_data\\" + group_folder_path + ".json"
	f = open(folder_path, 'r')
	json_data = json.load(f)
	return json_data

def check_group_folder_name(group_folder_name):
	"""
	Validate mail address
	"""
	result = True
	if group_folder_name == "":
		result = False

	if len(group_folder_name) > 20:
		result = False

	if r"[^.!#$%&'*+\/=?^_`{|}~-]" in group_folder_name:
		result = False

	return result
# =====================================================================================================================================================================================================

""" Plugin """
# =====================================================================================================================================================================================================
# Login User
@app.route('/user/loginUser', methods=['GET', 'POST'])
def loginUser():
	"""
	Plugin Only
	/user/loginUser path
	User login processing
	"""

	# Basic json data
	json_data = {
		"message": "",
		"data": {
			"user_id": "",
			"password": "",
		}
	}

	if request.method == "POST":
		# Login process
		form = loginUserValidate.LoginUserValidate()

		# Check request data
		if form.validate_on_submit() == True:
			# If there is no error in create request data
			model = userModel.UserModel()
			select_data, result = model.getLoginData(form.login_mail.data)
			crypto_password = model.safty_password(select_data[0][0], form.password.data)

			#Check password
			if select_data[0][2] == crypto_password:
				# If the password is the same
				# Set login information in session
				session['user_id'] = select_data[0][0]
				session['user_login_mail'] = select_data[0][1]
				# create json data
				json_data["message"] = "Success"
				json_data["user_id"] = select_data[0][0]
				json_data["password"] = select_data[0][2]
			else:
				# If the password is not the same
				json_data["message"] = "Error"
		else:
			json_data["message"] = "Error"
	else:
		json_data["message"] = "Request Error"

	return jsonify(json_data)
	# if request.method == "GET":
	# 	model = userModel.UserModel()
	# 	mail_address = request.args.get("mail_address")
	# 	login_password = request.args.get("login_password")
	# 	message, data = model.getLoginData(mail_address)

	# 	crypto_password = model.safty_password(data["user_id"], login_password)
	# 	if data["user_password"] == crypto_password:
	# 		json_data["message"] = "Success"
	# 		json_data["data"]["mail_address"] = mail_address
	# 		json_data["data"]["login_password"] = login_password
	# 		session['user_id'] = select_data[0][0]
	# 		session['user_login_id'] = select_data[0][1]
	# 	else:
	# 		json_data["message"] = "Login Falied"
	# else:
	# 	json_data["message"] = "Request Error"

# Sync GroupFolders
@app.route('/user/allSyncGroupFolders', methods=['GET', 'POST'])
def allSyncGroupFolders():
	"""
	Plugin Only
	/user/allSyncGroupFolders path
	Get all folder data
	"""

	# Basic json data
	json_data = {
		"message" : "",
		"data" : {
			"group_folder_id": "0",
			"group_folder_name": "",
			"group_folder_version": "0",
		}
	}

	if request.method == "GET":
		# not Create
		pass
	else:
		json_data["message"] = "Request Error"

	return jsonify(json_data)

# Create Folder
@app.route('/user/createGroup', methods=['GET', 'POST'])
def userCreateFolder():
	"""
	Plugin Only
	/user/createGroup path
	Create folder process
	"""

	groupfolder_model = groupFolderModel.GroupFolderModel()

	# Basic json data
	json_data = {
		"message" : "",
		"data" : {
			"group_folder_id": "0",
			"group_folder_name": "",
			"group_folder_version": "0",
		}
	}

	if request.method == "GET":
		#Folder name validate
		if check_group_folder_name(request.args.get('group_folder_name')):
			# Create folder process
			group_folder_name = request.args.get('group_folder_name')
			user_id = request.args.get('user_id')
			message, group_folder_id = groupfolder_model.insertGroupFolderPlugin(group_folder_name)

			# Create mastar authoriy data
			# マスター管理者データ作成
			# not create

			# Create json data
			json_data["message"] = "Success"
			json_data["data"]["group_folder_id"] = group_folder_id
			json_data["data"]["group_folder_name"] = group_folder_name
			json_data["data"]["group_folder_version"] = "1"

			# Create json data file for storage
			create_new_json_file(group_folder_id, group_folder_name)
		else:
			json_data["message"] = "Validate Error"
	else:
		json_data["message"] = "Request Error"

	return jsonify(json_data)

# Update Folder
@app.route('/user/updateGroup', methods=['GET', 'POST'])
def userUpdateGroup():
	"""
	Plugin Only
	/user/updateGroup path
	Update folder data
	"""
	model = groupFolderModel.GroupFolderModel()

	# Basic json data
	json_data = {
		"message" : "",
		"data" : {}
	}

	if request.method == "GET":
		# Check if file data exists
		select_data, message = model.selectGroupFolderPlugin(request.args.get('group_folder_id'))
		if message == "Complate" and select_data != []:
			# Get json file
			bookmark_data = input_json_file(select_data[0][3])
			json_data["data"] = bookmark_data
		json_data["message"] = "Success"
	else:
		json_data["message"] = "Request Error"

	return jsonify(json_data)

# Commit Folder
@app.route('/user/commitGroup', methods=['GET', 'POST'])
def userCommitGroup():
	"""
	Plugin Only
	/user/commitGroup path
	Commit folder data
	"""

	model = groupFolderModel.GroupFolderModel()
	# Basic json data
	json_data = {
		"message" : "",
		"data": {}
	}

	if request.method == "GET":
		temp_json = {}
		url_query = request.args.get('group_folder_data')
		json_bookmark = json.loads(url_query)

		# Check if file data exists
		select_data, message = model.selectGroupFolderPlugin(json_bookmark["0"]["bookmark_id"])
		if message == "Complate" and select_data != []:
			# Since the array of 0 contains folder information
			json_bookmark.pop("0")
			temp_json["bookmark"] = json_bookmark
			# Update json file
			create_update_json_file(temp_json, select_data)
			message = model.updateGroupFolderPlugin(select_data[0][0])
		json_data["message"] = "Success"
	else:
		json_data["message"] = "Request Error"

	return jsonify(json_data)

# Sync Folders
@app.route('/user/syncFolders', methods=['GET', 'POST'])
def syncFolders():
	"""
	Plugin Only
	/user/syncFolders path
	Get folder data
	"""
	model = groupFolderModel.GroupFolderModel()

	# Basic json data
	json_data = {
		"message" : "",
		"data": {}
	}

	if request.method == "GET":
		url_query = request.args.get('data')
		json_bookmark = json.loads(url_query)

		for value in json_bookmark["bookmark_id"]:
			# Check if file data exists
			select_data, message = model.selectGroupFolderPlugin(value)
			if message == "Complate" and select_data != []:
				bookmark_id = select_data[0][0]
				# Update json file
				bookmark_data = input_json_file(select_data[0][3])
				json_data["data"][bookmark_id] = bookmark_data

		json_data["message"] = "Success"
	else:
		json_data["message"] = "Request Error"

	return jsonify(json_data)

# Setting Folder
@app.route('/user/settingFolder', methods=['GET', 'POST'])
def settingFolder():
	"""
	Plugin Only
	/user/settingFolder path
	Update setting folder info
	"""
	model = authorityModel.AuthorityModel()


	if request.method == "POST":
		# not create
		pass
	elif request.method == "GET":
		# Show info
		form = FlaskForm()
		group_folder_id = request.args.get('group_folder_id')
		data, message = model.getFolderAuthority(group_folder_id)

		state_bit = {}

		for value in data:
			state_temp = []
			for shift in range(0, 5):
				if (int(value[2])>>shift) & 1:
					state_temp.append(True)
				else:
					state_temp.append(False)
			state_bit[value[0]] = state_temp
		html = render_template('userFolderSetting.html', form=form, data=data, state_bit=state_bit)

	return html

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=443, ssl_context=('openssl/cert.crt', 'openssl/server_secret.key'), threaded=True, debug=True)
