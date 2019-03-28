import sys, json
from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_login import LoginManager, login_user, login_required, UserMixin
from flask_wtf import FlaskForm

sys.path.append('./Model')
sys.path.append('./Validate')

from Validate import ( loginUserValidate
, adminUserEditShowValidate, adminUserEditUpdValidate
, numberingEditShowValidate, numberingEditUpdValidate
, userEditShowValidate, userEditUpdValidate
, groupFolderEditShowValidate, groupFolderEditUpdValidate
, authorityEditShowValidate, authorityEditUpdValidate
, createUserValidate, loginUserValidate)
from Model import adminUserModel, userModel, groupFolderModel, numberingModel, authorityModel

app = Flask(__name__)
app.secret_key = 'aaaa'

login_maneger = LoginManager()
login_maneger.init_app(app)

class User(UserMixin):
	pass

# =====================================================================================================================================================================================================
# Admin
# Root
@app.route('/')
def root():
	return redirect(url_for("mastar"))

# Login Page
@app.route('/mastar', methods=['GET', 'POST'])
def mastar():
	message = ''
	result = ''

	if request.method == "POST":
		form = loginUserValidate.LoginUserValidate()

		if form.validate_on_submit() == True:
			model = adminUserModel.AdminUserModel()
			select_data, result = model.getLoginData(form.user_mail_address.data)
			crypto_password = model.safty_password(select_data[0], form.user_password.data)

			if select_data[2] == crypto_password:
				user = User()
				user.id = select_data[0]
				login_user(user)
				return redirect(url_for('mastarMenu'))

			else:
				message = 'Error'
				return render_template('mastarLogin.html', form=form, message=message)

		else:
			message += form.user_mail_address.errors + '<br>'
			message += form.user_password.errors
			return render_template('mastarLogin.html', form=form, message=message)

	else:
		return render_template('mastarLogin.html', form=form, message=message)

# Admin Menu
@app.route('/mastar/menu', methods=['GET', 'POST'])
def mastarMenu():
	form = FlaskForm()
	html = render_template('mastarMenu.html', form=form)
	return html

# AdminUser List
@app.route('/mastar/adminUserList', methods=['GET', 'POST'])
def adminUserList():
	form = FlaskForm()
	model = adminUserModel.AdminUserModel()
	message = {
		"state": "",
		"message": ""
	}

	data, result = model.getList()

	if result == "Complate":
		html = render_template('mastarAdminUserList.html', data=data, form=form, message=message)
	else:
		message["state"] = "Error"
		message["message"] = result
		html = render_template('errorPage.html', message=message)
	return html

# AdminUser Edit
@app.route('/mastar/adminUserEdit', methods=['POST'])
def adminUserEdit():
	model = adminUserModel.AdminUserModel()
	message = {
		"state": "",
		"message": ""
	}

	if request.method == "POST":

		if request.form["state"] == "SHOW":
			form = adminUserEditShowValidate.AdminUserEditShowValidate()

			if form.validate_on_submit() == False:
				message["state"] = "Error"
				message["message"] = form.admin_user_id.errors
				return redirect(url_for("adminUserList"))

		else:
			form = adminUserEditUpdValidate.AdminUserEditUpdValidate()

			if form.validate_on_submit():

				if form.state.data == 'NEW':
					result, form.user_id.data = model.insertAdminUser(form)

				elif form.state.data == 'UPD':
					result = model.updateAdminUser(form)

				elif form.state.data == 'DEL':
					result = model.delateAdminUser(form)
					form.admin_user_id.data = '0'

				if result != "Complate":
					message["state"] = "Error"
					message["message"] = result

			else:
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
			data, result = model.selectAdminUser(form)

			if result == "Complate":
				html = render_template('mastarUserEdit.html', data=data[0], form=form)
			else:
				message["state"] = "Error"
				message["message"] = result
				html = render_template('mastarUserEdit.html', data=data[0], form=form)
		else:
			data = ['', '', '', '', '']
			html = render_template('mastarUserEdit.html', data=data, form=form)

	return html

# Numbering List
@app.route('/mastar/numberingList', methods=['GET', 'POST'])
def numberingList():
	form = FlaskForm()
	model = numberingModel.NumberingModel()
	message = {
		"state": "",
		"message": ""
	}

	data, result = model.getList()

	if result == "Complate":
		html = render_template('mastarNumberingList.html', data=data, form=form, message=message)
	else:
		message["state"] = "Error"
		message["message"] = result
		html = render_template('errorPage.html', message=message)
	return html

# Numbering Edit
@app.route('/mastar/numberingEdit', methods=['POST'])
def numberingEdit():
	model = numberingModel.NumberingModel()
	message = {
		"state": "",
		"message": ""
	}

	if request.method == "POST":

		if request.form["state"] == "SHOW":
			form = numberingEditShowValidate.NumberingEditShowValidate()

			if form.validate_on_submit() == False:
				message["state"] = "Error"
				message["message"] = form.numbering_id.errors
				return redirect(url_for("numberingList"))
		else:
			form = numberingEditUpdValidate.NumberingEditUpdValidate()

			if form.validate_on_submit():

				if form.state.data == 'NEW':
					result, form.numbering_id.data = model.insertNumbering(form)

				elif form.state.data == 'UPD':
					result = model.updateNumbergin(form)

				elif form.state.data == 'DEL':
					result = model.delateNumbergin(form)
					form.numbering_id.data = '0'

				if result != "Complate":
					message["state"] = "Error"
					message["message"] = result
			else:
				message["state"] = "Error"
				for error in form.numbering_id.errors:
					message["message"] += error + "<br>"
				for error in form.numbering_name.errors:
					message["message"] += error + "<br>"
				for error in form.next_value.errors:
					message["message"] += error + "<br>"

		if form.numbering_id.data != '0':
			data, result = model.selectNumbering(form)

			if result == "Complate":
				html = render_template('mastarNumberingEdit.html', data=data[0], form=form, message=message)
			else:
				message["state"] = "Error"
				message["message"] = result
				html = render_template('mastarNumberingList.html', data=data, form=form, message=message)
		else:
			data = ['', '', '', '', '', '']
			html = render_template('mastarNumberingEdit.html', data=data, form=form, message=message)

	return html

# User List
@app.route('/mastar/userList', methods=['GET', 'POST'])
def userList():
	form = FlaskForm()
	model = userModel.UserModel()
	message = {
		"state": "",
		"message": ""
	}

	data, result = model.getList()

	if result == "Complate":
		html = render_template('mastarUserList.html', data=data, form=form)
	else:
		message["state"] = "Error"
		message["message"] = result
		html = render_template('errorPage.html', message=message)
	return html

# User Edit
@app.route('/mastar/userEdit', methods=['POST'])
def userEdit():
	model = userModel.UserModel()
	message = {
		"state": "",
		"message": ""
	}

	if request.method == "POST":

		if request.form["state"] == "SHOW":
			form = userEditShowValidate.UserEditShowValidate()

			if form.validate_on_submit() == False:
				message["state"] = "Error"
				message["message"] = form.user_id.errors
				return redirect(url_for("userList"))

		else:
			form = userEditUpdValidate.UserEditUpdValidate()

			if form.validate_on_submit():

				if form.state.data == 'NEW':
					result, form.user_id.data = model.insertUser(form)

				elif form.state.data == 'UPD':
					result = model.updateUser(form)

				elif form.state.data == 'DEL':
					result = model.delateUser(form)
					form.user_id.data = '0'

				if result != "Complate":
					message["state"] = "Error"
					message["message"] = result

			else:
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
			data, result = model.selectUser(form)

			if result == "Complate":
				html = render_template('mastarUserEdit.html', data=data[0], form=form)
			else:
				message["state"] = "Error"
				message["message"] = result
				html = render_template('mastarUserEdit.html', data=data[0], form=form)
		else:
			data = ['', '', '', '', '']
			html = render_template('mastarUserEdit.html', data=data, form=form)

	return html

# GroupFolder List
@app.route('/mastar/groupFolderList',  methods=['GET', 'POST'])
def groupFolderList():
	form = FlaskForm()
	model = groupFolderModel.GroupFolderModel()
	message = {
		"state": "",
		"message": ""
	}

	data, result = model.getList()

	if result == "Complate":
		html = render_template('mastarGroupFolderList.html', data=data, form=form, message=message)
	else:
		message["state"] = "Error"
		message["message"] = result
		html = render_template('errorPage.html', message=message)
	return html

# GroupFolder Edit
@app.route('/mastar/groupFolderEdit', methods=['GET', 'POST'])
def groupFolderEdit():
	model = groupFolderModel.GroupFolderModel()
	message = {
		"state": "",
		"message": ""
	}

	if request.method == 'POST':

		if request.form["state"] == "SHOW":
			form = groupFolderEditShowValidate.GroupFolderEditShowValidate()

			if form.validate_on_submit() == False:
				message["state"] = "Error"
				message["message"] = form.group_folder_id.errors
				return redirect(url_for("groupFolderList"))
		else:
			form = groupFolderEditUpdValidate.GroupFolderUpdValidate()

			if form.validate_on_submit():

				if form.state.data == 'NEW':
					result, form.group_folder_id.data = model.insertGroupFolder(form)

				elif form.state.data == 'UPD':
					result = model.updateGroupFolder(form)

				elif form.state.data == 'DEL':
					result = model.delateGroupFolder(form)
					form.group_folder_id.data = '0'

				if result != "Complate":
					message["state"] = "Error"
					message["message"] = result

			else:
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
			data, result = model.selectGroupFolder(form)

			if result == "Complate":
				html = render_template('mastarGroupFolderEdit.html', data=data[0], form=form)
			else:
				message["state"] = "Error"
				message["message"] = result
				html = render_template('mastarGroupFolderEdit.html', data=data[0], form=form)
		else:
			data = ['', '', '', '', '', '', '']
			html = render_template('mastarGroupFolderEdit.html', data=data, form=form)

	return html

# Authoriry List
@app.route('/mastar/authorityList', methods=['GET', 'POST'])
def authorityList():
	form = FlaskForm()
	model = authorityModel.AuthorityModel()
	message = {
		"state": "",
		"message": ""
	}

	data, result = model.getList()

	if result == "Complate":
		html = render_template('mastarAuthorityList.html', data=data, form=form)
	else:
		message["state"] = "Error"
		message["message"] = result
		html = render_template('errorPage.html', message=message)

	return html

# Authoriy Edit
@app.route('/mastar/authorityEdit', methods=['GET', 'POST'])
def authorityEdit():
	model = authorityModel.AuthorityModel()
	message = {
		"state": "",
		"message": ""
	}

	if request.method == "POST":

		if request.form["state"] == "SHOW":
			form = authorityEditShowValidate.AuthorityEditShowValidate()

			if form.validate_on_submit() == False:
				message["state"] = "Error"
				message["message"] += form.user_id.errors
				message["message"] += form.group_folder_id.errors
				return redirect(url_for("authorityList"))
		else:
			form = authorityEditUpdValidate.AuthorityEditUpdValidate()

			if form.validate_on_submit():

				if form.state.data == 'NEW':
					result, form.user_id.data, form.group_folder_id.data = model.insertAuthority(form)

				elif form.state.data == 'UPD':
					result = model.upadteAuthority(form)

				elif form.state.data == 'DEL':
					result = model.delateAuthority(form)
					form.user_id.data = '0'
					form.group_folder_id.data = '0'

				if result != "Complate":
					message["state"] = "Error"
					message["message"] = result

			else:
				message["state"] = "Error"
				for error in form.user_id.errors:
					message["message"] += error + "<br>"
				for error in form.group_folder_id.errors:
					message["message"] += error + "<br>"

		# User List
		user_model = userModel.UserModel()
		user_list, message = user_model.getSelectList()
		# GroupFolder List
		groupFolder_model = groupFolderModel.GroupFolderModel()
		groupFolder_list, message = groupFolder_model.getSelectList()

		if form.user_id.data != '0' or form.group_folder_id.data != '0':
			data, result = model.selectAuthority(form)
			state_bit = []

			if result == "Complate":
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
			data = ['', '', '', '', '', '']
			state_bit = [False, False, False, False, False]
			html = render_template('mastarAuthorityEdit.html', data=data, user_list=user_list, groupFolder_list=groupFolder_list, state_bit=state_bit,form=form)

	return html

# =====================================================================================================================================================================================================
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
