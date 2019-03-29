// async function getJsonData(url, options)
// {
// 	var returnData = null
// 	await fetch(url, options)
// 	.then((resp) => resp.json())
// 	.then(function(data) 
// 	{
// 		returnData = data;
		
// 	})
// 	.catch(function(error) 
// 	{
// 		console.log(error);
// 	}); 

// 	return returnData;
// }

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
	// ||
}


async function loginAttempt()
{
	let usernameElement = document.getElementById('login-username');
	let passwordElement = document.getElementById('login-password');

	if( validString(usernameElement.value) && validString(passwordElement.value))
	{
		// console.log(true);
		url = getBaseUrl() + "loginrequest";

		let formData = new FormData();
		formData.append('username', usernameElement.value);
		formData.append('password', passwordElement.value);

		let response = await getJsonData(url,{method: "POST", body: formData});

		console.log(url);
		console.log(response);

		// TODO: check for errors
		if( setToken(response) )
		{
			window.location.href = getBaseUrl() + '';
		}
		else
		{
			// let errorElement = document.getElementById('error-display');
			let errorMessage = 'Login Failed';

			if (response != null && "error" in response) 
			{
		    	errorMessage = response.error;
			}

			displayError(errorMessage);

			// errorElement.innerHTML = errorMessage;
			// errorElement.style.display = 'block';
		}
	}
	else
	{	
		displayError('Username and password can\'t be empty or contain spaces');

		// console.log(false);
		// let errorElement = document.getElementById('error-display');

		// errorElement.innerHTML = 'Username and password can\'t be empty or contain spaces';
		// errorElement.style.display = 'block';
	}
}

// async function signupAttempt()
// {
// 	// console.log(getBaseUrl());
// 	let usernameElement = document.getElementById('signup-username');
// 	let passwordElement = document.getElementById('signup-password');
// 	let confirmpasswordElement = document.getElementById('signup-confirmpassword');
	
// 	// TODO: add validation for elements

// 	url = getBaseUrl() + "/signuprequest";

// 	let formData = new FormData();
// 	formData.append('username', usernameElement.value);
// 	formData.append('password', passwordElement.value);
// 	formData.append('confirmpassword', confirmpasswordElement.value);

// 	let response = await getJsonData(url,{method: "POST", body: formData});

// 	console.log(url);
// 	console.log(response);
// }