from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_url, login_required

app = Flask(__name__)
app.secret_key = 'BookMarkGroup Secret Key'

login_maneger = LoginManager()
login_maneger.init_app(app)

#Root
@app.route('/', methods=['GET'])
def root():
	return redirect(url_for('g_loginUser'))

#Create User
@app.route('/createUser', methods=['GET'])
def g_createUser():
	pass
@app.route('/createUser', methods=['POST'])
def p_createUser():
	pass

#Login User
@app.route('/loginUser', methods=['GET'])
def g_loginUser():
	pass
@app.route('/loginUser', methods=['POST'])
def p_loginUser():
	pass

#Sync Folders
@app.route('/syncFolders', methods=['GET'])
def g_syncFolders():
	pass

#Create GroupFolder
@app.route('/createGroupFolder', methods=['POST'])
def p_createGroupFolder():
	pass

#Commit GroupFolder
@app.route('/commitGroupFolder', methods=['POST'])
def p_commitGroupFolder():
	pass

#Update GroupFolder
@app.route('/updateGroupFolder', methods=['POST'])
def p_updateGroupFloder():
	pass

#Delete GroupFolder
@app.route('/deleteGroupFolder', methods=['POST'])
def p_deleteGroupFolder():
	pass

#Setting GroupFolder
@app.route('/settingShowUser', methods=['POST'])
def p_settingShowUser():
	pass

#Setting GroupFolder (Add user)
@app.route('/settingAddUser', methods=['POST'])
def p_settingAddUser():
	pass
	
#Setting GroupFolder (Del usr)
@app.route('/settginDelUser', methods=['POST'])
def p_settingDelUser():
	pass

#Setting GroupFolder (Setting Authority)
@app.route('/settingSetAuthority', methods=['POST'])
def p_settingSetAuthority():
	pass

@app.route('/settingShowAuthority', methods=['POST'])
def p_settingShowAuthority():
	pass