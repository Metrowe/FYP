async function signupAttempt()
{

	let usernameElement = document.getElementById('signup-username');
	let passwordElement = document.getElementById('signup-password');
	let confirmpasswordElement = document.getElementById('signup-confirmpassword');
		
	if( validString(usernameElement.value) && validString(passwordElement.value) )
	{
		if ( passwordElement.value == confirmpasswordElement.value )
		{
			url = getBaseUrl() + "signuprequest";

			let formData = new FormData();
			formData.append('username', usernameElement.value);
			formData.append('password', passwordElement.value);
			formData.append('confirmpassword', confirmpasswordElement.value);

			let response = await getJsonData(url,{method: "POST", body: formData});

			console.log(url);
			console.log(response);

			if( setToken(response) )
			{
				window.location.href = getBaseUrl() + '';
			}
			else
			{
				let errorMessage = 'Signup Failed';

				if (response != null && "error" in response) 
				{
			    	errorMessage = response.error;
				}

				displayError(errorMessage);
			}
		}
		else
		{
			displayError('Password confirmation does not match');
		}
	}
	else
	{
		displayError('Username and password can\'t be empty or contain spaces');
	}
}