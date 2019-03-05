async function signupAttempt()
{
	// console.log(getBaseUrl());
	let usernameElement = document.getElementById('signup-username');
	let passwordElement = document.getElementById('signup-password');
	let confirmpasswordElement = document.getElementById('signup-confirmpassword');
	
	// TODO: add validation for elements

	url = getBaseUrl() + "/signuprequest";

	let formData = new FormData();
	formData.append('username', usernameElement.value);
	formData.append('password', passwordElement.value);
	formData.append('confirmpassword', confirmpasswordElement.value);

	let result = await getJsonData(url,{method: "POST", body: formData});

	console.log(url);
	console.log(result);
}

// testHelper();
// console.log(window.location.href)
// console.log(window.location.hostname)
// console.log(window.location.pathname)
// console.log(window.location.protocol)

// console.log(window.location.href.slice(0, window.location.pathname.length * -1))

// console.log(window.location.href)

// console.log(window.location.assign)