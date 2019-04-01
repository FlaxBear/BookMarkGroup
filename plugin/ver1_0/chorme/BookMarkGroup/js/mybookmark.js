var localStorage_key = "BookMarkGroup";

// Function: button_processing
// Description: Perform processing of each button
// Input: [String] mode: Number allocated to each button
// Output: None
function button_processing(mode) {
	switch(mode) {
		case '2':
			createGroup(); // ok
			//updateGroup();
		break;
		case '6':
			removeGroup();
		break;
		default:
	}
	return;
}

// Function: callBack_pass
// Description: End callback without doing anything
// Input: None
// Output: None
function callBack_pass() {return false;}

// Function: createCreateDetailsObject
// Description: Create the DetailsObject type needed to create a new bookmark or folder property
// Input: [String] parentId: Parent directory id
//		  [Int] index: Order num
//		  [String] title: Name of bookmark or folder
//		  [String] url: url
// Output: [DetailsObject型] obj
function createCreateDetailsObject(parentId, index, title, url)
{
	var obj = {
		parentId: parentId,
		index: index,
		title: title,
		url: url,
	}
	return obj;
}

// Function: writeLocalStorage
// Description: Save data to localStorage
// Input: [JSON] storage_data
// Output: None
function writeLocalStorage(storage_data) 
{
	localStorage.setItem(localStorage_key, storage_data);
	return;
}

// Function: loadLocalStorage
// Description: Extract data to localStorage
// Input: None
// Output: [JSON] storage_data
function loadLocalStorage() 
{
	var storage_data = localStorage.getItem(localStorage_key);
	return storage_data;
}

// Function: createGroup
// Description: Create a GroupFolder(See callBack_createGroup())
// Input: None
// Output: None
function createGroup() {
	// Look inside the text box of make_bookmark_group and make it if it is not empty
	if(document.main.make_bookmark_group.value != '') {
		chrome.bookmarks.getChildren('1', callBack_createGroup);
	} else {
		// Show Error Message
	}
	return;
}

// 関数: callBack_reateGroup
// 説明: Obtain a list of bookmarks, create a BookMarkGroup folder, create it, and create a group folder
// 入力: [BookmarkTreeNode][List]: bookmarkItems Information list of each folder in bookmark
// 出力: None
function callBack_createGroup(bookmarkItems) {
	// For judging whether to create a new BookMarkGroup folder
	var folder_flag = false;

	for(item of bookmarkItems) 
	{
		if(item.title == 'BookMarkGroup' && item.url == undefined) 
		{
			folder_flag = true;
			// Create 
			var group_folder_title = document.main.make_bookmark_group.value;
			var mybookmark = createCreateDetailsObject(item.id, 0, group_folder_title, null);
			chrome.bookmarks.create(mybookmark, callBack_pass);
		}
	}
	if(folder_flag == false) 
	{
		// 新規でBookMarkGroupフォルダーを作成を行い、グループファイルを作成する
		var mybookmark = createCreateDetailsObject('1', 0, 'BookMarkGroup', null);
		chrome.bookmarks.create(mybookmark, callBack_pass);
		// Regularly search again, and group folders are created
		chrome.bookmarks.getChildren('1', callBack_reateGroup);
	}
}

// Function: updateGroup
// Description: Update data to LocalStorage
// Input: None
// Output: None
function updateGroup()
{
	var localstorage = loadLocalStorage();
	if(localstorage != null) {
		if(localstorage.mybookmark.folder_id != "") {
			// localstoregeの更新
		} else {
			
		}
	} else {

	}
}

// Function: removeGroup
// Description: Delete GroupFolder(See callBack_removeGroup())
// Input: None
// Output: None
function removeGroup()
{
	// make_bookmark_groupのテキストボックスの中身を見て、空でなければ削除を行う
	if(document.main.make_bookmark_group.value != '') {
		chrome.bookmarks.getChildren('1', callBack_removeGroup);
	} else {
		// エラーメッセージを表示（未作成）
	}
	return;
}

// 関数: callBack_removeGroup
// 説明: ブックマークの一覧を取得し、MyBookMarkフォルダーがなければエラーメッセージを表示し、存在するならばグループフォルダーの削除を行う
// 入力: BookmarkTreeNode型(リスト型) bookmarkItems ブックマークに入っている各フォルダーの情報リスト(コールバック関数の呼び出し時取得)
// 出力: なし
function callBack_removeGroup(bookmarkItems) {
	var remove_flag = false;
	for(item of bookmarkItems) 
	{
		if(item.title == 'MyBookMark' && item.url == undefined) 
		{
			//グループファイルを削除する
			var group_folder_id = document.main.remove_bookmark_group.value;
			chrome.bookmarks.remove(group_folder_id, callBack_pass)
			remove_flag = true;
		}
	}
	if(remove_flag == true){
		// 削除メッセージの表示
	} else {
		// エラーメッセージを表示
	}
}


function callBack_writeLocalStorage(bookmarkItem)
{
	// var key = "MyBookMark";
	// var storage_data = localStorage.getItem(key);

	console.log(bookmarkItem.id);
	var test = document.getElementById("debug_result");
	test.innerHTML = bookmarkItem.id;

	// var test = document.getElementById("debug_result");
	// test.innerHTML = bookmarkItems[0].id;

	// localStorage.setItem(key, bookmarkItems);
}
