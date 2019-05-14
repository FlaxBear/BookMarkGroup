/**
 * Key name used by Local Strage
 * @type {String}
 */
var localStorage_key = "BookMarkGroup";

// ================================================================================================
// Basic Function
// ================================================================================================
/**
 * End callback without doing anything
 */
function callBack_pass() {return false;}

/**
 * Create objects required to create bookmarks
 * @param {String} parentId Parent directory id
 * @param {Number} index Order num
 * @param {String} title Bookmark or Folder name
 * @param {String} url URL for bookmarks, NULL for folders
 * @return {DetailsObject} Objects needed to create a bookmark
 */
function createDetailsObject(parentId, index, title, url)
{
	var obj = {
		parentId: parentId,
		index: index,
		title: title,
		url: url,
	}
	return obj;
}

/**
 * Write LocalStorage
 * @param {Object} storage_data
 */
function writeLocalStorage(storage_data)
{
	localStorage.setItem(localStorage_key, JSON.stringify(storage_data));
	return;
}

/**
 * Load LocalStorage
 * @return {Object}
 */
function loadLocalStorage()
{
	var storage_data = localStorage.getItem(localStorage_key);
	return JSON.parse(storage_data);
}

/**
 * Check if there is data in the LocalStorage
 */
function checkLocalStorage()
{
	var storage_data = localStorage.getItem(localStorage_key);
	if (storage_data == null) {
		data = {
			"user_id": "0",
			"user_password": "",
			"data":{},
		}
		writeLocalStorage(data);
	}
	return
}

// ================================================================================================
// Debug
function onGot(bookmarkItems) {
	for (item of bookmarkItems) {
		console.log(item.id + ":" + item.title + ":" + item.parentId);
	}
}

function debug_localstrage() {
	var storage_data = localStorage.getItem(localStorage_key);

	Object.keys(storage_data).forEach(function(key) {
		if(key == "data") {
			Object.keys(storage_data["data"]).forEach(function(key2) {
				console.log(key2 + ":" + storage_data["data"][key]);
			});
		} else {
			console.log(key + ":" + storage_data[key]);
		}
	});
}
// ================================================================================================

// ================================================================================================
// Processing Function
// ================================================================================================
/**
 * Process each button
 * @param {String} mode Assigned number of each button
 */
function button_proccessing(mode)
{
	switch(mode) {
		case '1':	// User
			break;
		case '2':	// All Sync
			ajaxAllSyncGroupFolder();
			break;
		case '3':	// Create
			Promise.resolve()
			.then(
				() => new Promise((resolve) => {
					setTimeout(() => {
						ajaxCreateGroupFolder();
						resolve();
					}, 1000);
				})
			)
			.then(
				() => new Promise((resolve) => {
					setTimeout(() => {
						createGroupFolder();
						resolve();
					}, 1000);
				})
			);
			break;
		case '4':	// Sync
			ajaxSyncGroupFolder();
			break;
		case '5':	// Commit
			CommitGroupFolder();
			break;
		case '6':	// Setting
			break;
		default:
			break;
	}
	return;
}
/**
 *
 */
function ajaxAllLoginUser()
{
	var req = new XMLHttpRequest();

	req.onreadystatechange = function()
	{
		if (req.readyState == 4)
		{
			if (req.status == 200)
			{
				result = JSON.parse(req.responseText)

				if(result["message"] == "Success")
				{
					var storage_data = loadLocalStorage();
				}
				else
				{

				}
			}
		}
	}
	req.open('GET', 'http://127.0.0.1:5000/user/updateGroup?group_folder_id=');
	req.send();
}
/**
 *
 */
function ajaxAllSyncGroupFolder()
{
	var req = new XMLHttpRequest();
	var group_folder_id = "";
	var message_box = document.getElementById('message');

	req.onreadystatechange = function()
	{
		if (req.readyState == 4)
		{
			if (req.status == 200)
			{
				result = JSON.parse(req.responseText);

				if(result["message"] == "Success")
				{
					checkLocalStorage();
					createBookmark(result["bookmark"], group_folder_id);
				}
			}
		}
	}

	req.open('GET', 'http://127.0.0.1:5000/user/updateGroup?group_folder_id=' + encodeURIComponent(group_folder_id));
	req.send();
}

/**
 * Create GroupFolder.
 * See the callBack_createGroupFolder() for details
 */
function createGroupFolder()
{
	if(document.menuForm.group_folder_name.value != '') {
		browser.bookmarks.getChildren('menu________', callBack_createGroupFolder)
	} else {
	}
	return;
}

/**
 * This is callback function.
 * First, Search parent folder BookMarkGroup
 * Second, If there is no parent folder, create and perform a side search
 * and If there is a parent folder, create a folder
 * @param {Array} bookmarkItems
 */
function callBack_createGroupFolder(bookmarkItems)
{
	// For judging whether to create a new BookMarkGroup folder
	var folder_flag = false;

	for(item of bookmarkItems)
	{
		if(item.title == 'BookMarkGroup' && item.url == undefined)
		{
			folder_flag = true;
			// Create Group Folder
			var group_folder_title = document.menuForm.group_folder_name.value;
			var mybookmark_obj = createDetailsObject(item.id, 0, group_folder_title, null);
			browser.bookmarks.create(mybookmark_obj, callBack_UpdateItemId);
		}
	}

	if(folder_flag == false)
	{
		Promise.resolve()
			.then(
				() => new Promise((resolve) => {
					setTimeout(() => {
						var bookmarkgroup_obj = createDetailsObject('menu________', 0, 'BookMarkGroup', null);
						browser.bookmarks.create(bookmarkgroup_obj, callBack_pass);
						resolve();
					}, 1000);
				})
			)
			.then(
				() => new Promise((resolve) => {
					setTimeout(() => {
						browser.bookmarks.getChildren('menu________', callBack_createGroupFolder);
						resolve();
					}, 1000);
				})
			);
	}
}

function callBack_UpdateItemId(bookmarkItem)
{
	var storage_data = loadLocalStorage();

	// for(key of storage_data["data"]) {
	// 	var data_json = JSON.parse(storage_data["data"][key]);
	// 	if (data_json["folder_name"] == bookmarkItem.title) {
	// 		data_json["item_id"] = bookmarkItem.item_id;
	// 		storage_data["data"][key] = JSON.stringify(data_json);
	// 	}
	// }

	// Object.keys(storage_data["data"]).forEach(function(key) {
	// 	if(storage_data["data"][key]["folder_name"] == bookmarkItem.title) {
	// 		storage_data["data"][key]["item_id"] = bookmarkItem.item_id;
	// 	}
	// });
	Object.keys(storage_data["data"]).forEach(function(key) {
		var data_json = JSON.parse(storage_data["data"][key]);

		if (data_json["folder_name"] == bookmarkItem.title) {
			data_json["item_id"] += String(bookmarkItem.id);
			storage_data["data"][key] = JSON.stringify(data_json);
		}
	});

	writeLocalStorage(storage_data);
}

/**
 *
 */
function ajaxCreateGroupFolder()
{
	var req = new XMLHttpRequest();
	var group_folder_title = document.menuForm.group_folder_name.value;
	var message_box = document.getElementById('message');

	req.onreadystatechange = function()
	{
		if (req.readyState == 4)
		{
			if (req.status == 200)
			{
				result = JSON.parse(req.responseText);

				if (result["message"] == "Success")
				{
					checkLocalStorage();
					basic_data = loadLocalStorage();
					localStorage_obj = {
						"item_id": "",
						"folder_id": result["data"]["group_folder_id"],
						"folder_name": result["data"]["group_folder_name"],
						"version": result["data"]["group_folder_version"]
					}
					basic_data["data"][result["data"]["group_folder_id"]] = JSON.stringify(localStorage_obj);
					writeLocalStorage(basic_data);
					message_box.innerHTML = "Success";
				}
				message_box.innerHTML = result["message"];
			}
		}
	}

	req.open('GET', 'http://127.0.0.1:5000/user/createGroup?group_folder_name=' + encodeURIComponent(group_folder_title));
	req.send();
}

/**
 *
 */
function ajaxSyncGroupFolder()
{
	var req = new XMLHttpRequest();
	var group_folder_id = document.menuForm.selectSyncList.value;
	var message_box = document.getElementById('message');

	req.onreadystatechange = function()
	{
		if (req.readyState == 4)
		{
			if (req.status == 200)
			{
				result = JSON.parse(req.responseText);

				if(result["message"] == "Success")
				{
					checkLocalStorage();
					deleteGroupFolder(group_folder_id);
					createBookmark(result["data"]["bookmark"], group_folder_id);
				}
			}
		}
	}

	req.open('GET', 'http://127.0.0.1:5000/user/updateGroup?group_folder_id=' + encodeURIComponent(group_folder_id));
	req.send();
}

function deleteGroupFolder(group_folder_id)
{
	var basic_data = loadLocalStorage();
	for(id in basic_data["data"]) {
		if(id == group_folder_id) {
			var data = JSON.parse(basic_data["data"][id]);
			browser.bookmarks.getChildren(data["item_id"], callBack_deleteGroupFolder);
		}
	}
}

function callBack_deleteGroupFolder(bookmarkItems)
{
	for(item of bookmarkItems)
	{
		browser.bookmarks.remove(item.id, callBack_pass);
	}
}

function createBookmark(bookmark_data, group_folder_id)
{
	var basic_data = loadLocalStorage();
	for(id in basic_data["data"]) {
		if(id == group_folder_id) {
			for(key in bookmark_data) {
				var data = JSON.parse(basic_data["data"][id]);
				var mybookmark_obj = {
					"parentId": data["item_id"],
					"title": bookmark_data[key]["bookmark_name"],
					"url": bookmark_data[key]["bookmark_url"]
				};
				browser.bookmarks.create(mybookmark_obj);
			}
		}
	}
}

function CommitGroupFolder()
{

	var group_folder_id = document.menuForm.selectCommitList.value;
	var message_box = document.getElementById('message');
	var basic_data = loadLocalStorage();

	for(id in basic_data["data"]) {
		if(id == group_folder_id) {
			var data = JSON.parse(basic_data["data"][id]);
			browser.bookmarks.getChildren(data["item_id"], callBack_ajaxCommitGroupFolder);
		}
	}

	// req.onreadystatechange = function()
	// {
	// 	if (req.readyState == 4)
	// 	{
	// 		if (req.status == 200)
	// 		{
	// 			result = JSON.parse(req.responseText);

	// 			if(result["message"] == "Success")
	// 			{
	// 			}
	// 		}
	// 	}
	// }

	// req.open('GET', 'http://127.0.0.1:5000/user/updateGroup?group_folder_id=' + encodeURIComponent(group_folder_id));
	// req.send();
}

function callBack_ajaxCommitGroupFolder(bookmarkItems) {
	var req = new XMLHttpRequest();

	var send_data = {};


	var parent_data = loadLocalStorage();
	for(id in parent_data["data"]) {
		var data = JSON.parse(parent_data["data"][id]);
		if(data["item_id"] == bookmarkItems[0].parentId) {
			// 少なくとも一つのブックマークが必要
			send_data[0] = {
				bookmark_id: data["folder_id"]
			}
		}
	}

	var count = 1;
	for(item of bookmarkItems)
	{
		send_data[count] = {
			bookmark_nama: item.title,
			bookmark_url: item.url
		}
		count++;
	}

	var send_param = JSON.stringify(send_data);
	req.onreadystatechange = function()
	{
		if (req.readyState == 4)
		{
			if (req.status == 200)
			{
				result = JSON.parse(req.responseText);

				if(result["message"] == "Success")
				{
				}
			}
		}
	}

	req.open('GET', 'http://127.0.0.1:5000/user/commitGroup?group_folder_data=' + encodeURIComponent(send_param));
	req.send();
}

function createFolderList() {
	var localStorage = loadLocalStorage();

	var selectSycn = document.menuForm.selectSyncList;
	var selectCommit = document.menuForm.selectCommitList;
	var selectSetting = document.menuForm.selectSettingList;

	var syncOptions = selectSycn.options;
	var commitOptions = selectCommit.options;
	var settingOptions = selectSetting.options;



	for (var i = 0, length = syncOptions.length; i < length; i++) {
		selectSycn.removeChild(selectSycn.firstChild);
	}

	for (var i = 0, length = commitOptions.length; i < length; i++) {
		selectCommit.removeChild(selectCommit.firstChild);
	}


	for (var i = 0, length = settingOptions.length; i < length; i++) {
		selectSetting.removeChild(selectSetting.firstChild);
	}

	for(key in localStorage["data"])
	{
		let syncoption = document.createElement("option");
		let commitoption = document.createElement("option");
		let settingoption = document.createElement("option");

		let data = JSON.parse(localStorage["data"][key]);

		syncoption.value = key;
		syncoption.text = data["folder_name"];

		commitoption.value = key;
		commitoption.text = data["folder_name"];

		settingoption.value = key;
		settingoption.text = data["folder_name"];

		document.getElementById('syncList').appendChild(syncoption);
		document.getElementById('commitList').appendChild(commitoption);
		document.getElementById('settingList').appendChild(settingoption);
	}
	return;
}

// ================================================================================================
window.onload = function () {

	checkLocalStorage();
	user_data = loadLocalStorage();

	if(user_data["user_id"] != 0 && user_data["user_password"] != "") {

		createFolderList();

		document.getElementById('user_button').addEventListener('click', function(){
			button_proccessing('1');
		}, false);

		document.getElementById('allsync_button').addEventListener('click', function(){
			button_proccessing('2');
		}, false);

		document.getElementById('create_button').addEventListener('click', function(){
			Promise.resolve()
				.then(
					() => new Promise((resolve) => {
						setTimeout(() => {
							button_proccessing('3');
							resolve();
						}, 2000);
					})
				)
				.then(
					() => new Promise((resolve) => {
						setTimeout(() => {
							createFolderList();
							resolve();
						}, 2000);
					})
				);
		}, false);

		document.getElementById('sync_button').addEventListener('click', function(){
			button_proccessing('4');
		}, false);

		document.getElementById('commit_button').addEventListener('click', function(){
			button_proccessing('5');
		}, false);

		document.getElementById('setting_button').addEventListener('click', function(){
			button_proccessing('6');
		}, false);
	} else {
		document.menuForm.action = "login.html";
		document.menuForm.submit();
	}
};
