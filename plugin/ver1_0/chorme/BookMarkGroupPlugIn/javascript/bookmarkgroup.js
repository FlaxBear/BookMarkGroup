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
 *
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
 *
 * @param {Object} storage_data
 */
function writeLocalStorage(storage_data)
{
	localStorage.setItem(localStorage_key, storage_data);
	return;
}

/**
 * @return {Object}
 */
function loadLocalStorage()
{
	var storage_data = localStorage.getItem(localStorage_key);
	return storage_data;
}
// ================================================================================================


/**
 * Process each button
 * @param {String} mode Assigned number of each button
 */
function button_proccessing(mode)
{
	var message = "";
	switch(mode) {
		case '1':	// User
			break;
		case '2':	// All Sync
			break;
		case '3':	// Create
			message = createGroup();
			message = ajaxCreateGroup();
			break;
		case '4':	// Sync
			break;
		case '5':	// Commit
			break;
		case '6':	// Setting
			break;
		default:
			break;
	}
	return;
}

/**
 * @return {String}
 */
function createGroup()
{
	var message = '';
	if(document.menuForm.group_folder_name.value != '') {
		chrome.bookmarks.getChildren('1', callBack_createGroup)
		message = "Success";
	} else {
		message = "Enter file name"
	}
	return message;
}

/**
 *
 * @param {Array} bookmarkItems
 */
function callBack_createGroup(bookmarkItems)
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
			chrome.bookmarks.create(mybookmark_obj, callBack_pass);
		}
	}

	if(folder_flag == false)
	{

		//If there is no BookMarkGroup Folder , Create BookMarkGroup Folder
		var bookmarkgroup_obj = createDetailsObject('1', 0, 'BookMarkGroup', null);
		chrome.bookmarks.create(bookmarkgroup_obj, callBack_pass);
		// Regularly search again, and group folders are created
		chrome.bookmarks.getChildren('1', callBack_createGroup);
	}
}

function ajaxCreateGroup()
{
	var req = new XMLHttpRequest();
	var group_folder_title = document.menuForm.group_folder_name.value;
	var message = "";
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
					basic_data = loadLocalStorage();
					localStorage_obj = {
						"folder_id": result["data"]["group_folder_id"],
						"folder_name": result["data"]["group_folder_name"],
						"version": result["data"]["group_folder_version"]
					}
					basic_data["data"] += localStorage_obj;
					writeLocalStorage(basic_data);
					message_box.innerHTML = "Success";
				}
				message_box.innerHTML = result["message"];
			}
		}
	}

	req.open('GET', 'Access-Control-Allow-Origin: https://127.0.0.1/user/createGroup?group_folder_name=' + encodeURIComponent(group_folder_title), true);
	//req.open('GET', 'chrome-extension://oalfeofdhodfbhhbndlladgameppjohm: http://127.0.0.1:5000/user/createGroup?group_folder_name=' + encodeURIComponent(group_folder_title), true);

	req.send(null);
}