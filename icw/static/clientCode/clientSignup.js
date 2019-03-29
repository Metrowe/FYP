async function signupAttempt()
{

	let usernameElement = document.getElementById('signup-username');
	let passwordElement = document.getElementById('signup-password');
	let confirmpasswordElement = document.getElementById('signup-confirmpassword');
		
	if( validString(usernameElement.value) && validString(passwordElement.value) )
	{
		if ( passwordElement.value == confirmpasswordElement.value )
		{
			// TODO: add validation for elements

			url = getBaseUrl() + "signuprequest";

			let formData = new FormData();
			formData.append('username', usernameElement.value);
			formData.append('password', passwordElement.value);
			formData.append('confirmpassword', confirmpasswordElement.value);

			let result = await getJsonData(url,{method: "POST", body: formData});

			console.log(url);
			console.log(result);

			if( setToken(result) )
			{
				window.location.href = getBaseUrl() + '';
			}
			else
			{
				// let errorElement = document.getElementById('error-display');
				let errorMessage = 'Signup Failed';

				if (results != null && "error" in result) 
				{
			    	errorMessage = result.error;
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









// async function loginAttempt()
// {
// 	let usernameElement = document.getElementById('login-username');
// 	let passwordElement = document.getElementById('login-password');

// 	if( validString(usernameElement.value) && validString(passwordElement.value))
// 	{
// 		console.log(true);
// 		url = getBaseUrl() + "loginrequest";

// 		let formData = new FormData();
// 		formData.append('username', usernameElement.value);
// 		formData.append('password', passwordElement.value);

// 		let result = await getJsonData(url,{method: "POST", body: formData});

// 		console.log(url);
// 		console.log(result);

// 		// TODO: check for errors
// 		if( setToken(result) )
// 		{
// 			// window.location.href = getBaseUrl() + '';
// 		}
// 		else
// 		{
// 			let errorElement = document.getElementById('error-display');
// 			let errorMessage = 'Login Failed';

// 			if ("error" in result) 
// 			{
// 		    	errorMessage = result.error;
// 			}

// 			errorElement.innerHTML = errorMessage;
// 			errorElement.style.display = 'block';
// 		}
// 	}
// 	else
// 	{	
// 		let errorElement = document.getElementById('error-display');

// 		errorElement.innerHTML = 'Username and password can\'t be empty or contain spaces';
// 		errorElement.style.display = 'block';
// 	}
// }







// testHelper();
// console.log(window.location.href)
// console.log(window.location.hostname)
// console.log(window.location.pathname)
// console.log(window.location.protocol)

// console.log(window.location.href.slice(0, window.location.pathname.length * -1))

// console.log(window.location.href)

// console.log(window.location.assign)