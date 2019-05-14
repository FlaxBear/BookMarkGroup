// ================================================================================================
// Basic Function
// ================================================================================================

// ================================================================================================

// ================================================================================================
// Processing Function
// ================================================================================================
function login_processing()
{
	var req = new XMLHttpRequest();

	var login_mail = document.loginForm.login_mail.value;
	var password = document.loginForm.password.value;
	var send_data = {
		"login_mail": login_mail,
		"password": password
	}

	req.onreadystatechange = function()
	{
		if (req.readyState == 4)
		{
			if (req.status == 200)
			{
				result = JSON.parse(req.responseText);

				if(result["message"] == "") {
					document.menuForm.action = "menu.html";
					document.menuForm.submit();
				} else {
				}
			}
		}
	}

	req.open('POST', 'http://127.0.0.1:5000/user/loginUser');
	req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	req.send(EncodeHTMLForm(send_data));
}

// ================================================================================================
window.onload = function () {
	document.getElementById('login_button').addEventListener('click', function() {
		login_processing();
	}, false);
}