from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_url, login_required
from module.BookMarkGroupController import BookMarkGroupController

app = Flask(__name__)
app.secret_key = 'BookMarkGroup Secret Key'

login_maneger = LoginManager()
login_maneger.init_app(app)

bookMarkGroup_class = BookMarkGroupController.BookMarkGroupController()

# Root
@app.route('/', methods=['GET'])
def root():
	return redirect(url_for('g_loginUser'))

# Create User
@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
	bookMarkGroup_class.createUser()
	return

# Login User
@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
	bookMarkGroup_class.loginUser()
	return

# Sync Folders
@app.route('/syncFolders', methods=['GET'])
def syncFolders():
	bookMarkGroup_class.syncFolders()
	return

# Create GroupFolder
@app.route('/createGroupFolder', methods=['POST'])
def createGroupFolder():
	bookMarkGroup_class.createGroupFolder()
	return

# Commit GroupFolder
@app.route('/commitGroupFolder', methods=['POST'])
def commitGroupFolder():
	bookMarkGroup_class.commitGroupFolder()
	return

# Update GroupFolder
@app.route('/updateGroupFolder', methods=['POST'])
def updateGroupFloder():
	bookMarkGroup_class.updateGroupFolder()
	return

# Delete GroupFolder
@app.route('/deleteGroupFolder', methods=['POST'])
def deleteGroupFolder():
	bookMarkGroup_class.deleteGroupFolder()
	return

# Setting GroupFolder
@app.route('/settingShowUser', methods=['POST'])
def settingShowUser():
	bookMarkGroup_class.settingShowUser()
	return

#Setting GroupFolder (Add user)
@app.route('/settingAddUser', methods=['POST'])
def settingAddUser():
	bookMarkGroup_class.settingAddUser()
	return
	
#Setting GroupFolder (Del usr)
@app.route('/settginDelUser', methods=['POST'])
def settingDelUser():
	bookMarkGroup_class.settingDelUser()
	return

#Setting GroupFolder (Setting Authority)
@app.route('/settingSetAuthority', methods=['POST'])
def settingSetAuthority():
	bookMarkGroup_class.settingSetAuthority()
	return

@app.route('/settingShowAuthority', methods=['POST'])
def settingShowAuthority():
	bookMarkGroup_class.settingShowAuthority()
	return