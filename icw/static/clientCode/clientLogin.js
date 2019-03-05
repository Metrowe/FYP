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

async function loginAttempt()
{
	let usernameElement = document.getElementById('login-username');
	let passwordElement = document.getElementById('login-password');

	url = getBaseUrl() + "loginrequest";

	let formData = new FormData();
	formData.append('username', usernameElement.value);
	formData.append('password', passwordElement.value);

	let result = await getJsonData(url,{method: "POST", body: formData});

	setToken(result)

	console.log(url);
	console.log(result);
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

// 	let result = await getJsonData(url,{method: "POST", body: formData});

// 	console.log(url);
// 	console.log(result);
// }