function validString(str)
{
	if(!/ /.test(str) && str!='')
	{
		return true;
	}
	else
	{
		return false;
	}
}


async function loginAttempt()
{
	let usernameElement = document.getElementById('login-username');
	let passwordElement = document.getElementById('login-password');

	if( validString(usernameElement.value) && validString(passwordElement.value))
	{
		url = getBaseUrl() + "loginrequest";

		let formData = new FormData();
		formData.append('username', usernameElement.value);
		formData.append('password', passwordElement.value);

		let response = await getJsonData(url,{method: "POST", body: formData});

		console.log(url);
		console.log(response);

		if( setToken(response) )
		{
			window.location.href = getBaseUrl() + '';
		}
		else
		{
			let errorMessage = 'Login Failed';

			if (response != null && "error" in response) 
			{
		    	errorMessage = response.error;
			}

			displayError(errorMessage);
		}
	}
	else
	{	
		displayError('Username and password can\'t be empty or contain spaces');
	}
}