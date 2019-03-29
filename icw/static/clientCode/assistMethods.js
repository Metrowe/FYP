var baseUrl;

function clickTest()
{
	console.log('click')
}

function getBaseUrl()
{

	console.log('href: ' + window.location.href);
	console.log('path: ' + window.location.pathname);
	// 'a nice string'.indexOf('nice') !== -1

	// window.location.href.indexOf(window.location.pathname)

	if(baseUrl == null)
	{
		// baseUrl = window.location.href.slice(0, window.location.pathname.length * -1) + '/';
		baseUrl = window.location.href.slice(0, window.location.href.indexOf(window.location.pathname)) + '/';
	}

	console.log('bUrl: ' + baseUrl);


	// baseUrl = 'http://127.0.0.1:5000/';

	return baseUrl;
}

//## START TOKEN MANAGEMENT ##//
function getToken()
{
	var token = null;

	if ("token" in sessionStorage) 
	{
    	token = sessionStorage.token;
	}

	return token;
}

function setToken(result)
{
	if ("token" in result) 
	{
    	sessionStorage.token = result.token;
    	return true;
	}
	else
	{
		return false;
	}
	// else
	// {
	// 	sessionStorage.token = null;
	// }



	// var token = null;

	// if ("token" in sessionStorage) 
	// {
 //    	token = sessionStorage.token;
	// }

	// return token;
}

function deleteToken()
{
	if (getToken() != null) 
	{
    	delete sessionStorage.token;
	}
}
//## END TOKEN MANAGEMENT ##//




function adjustNavbar()
{
	// console.log('entered adjust navbar')
	if (getToken() != null) 
	{
    	document.getElementById('nav-myuploads').style.display = 'block';
    	document.getElementById('nav-login').style.display = 'none';
    	document.getElementById('nav-signup').style.display = 'none';
    	document.getElementById('nav-logout').style.display = 'block';
	}
	else
	{
		document.getElementById('nav-myuploads').style.display = 'none';
    	document.getElementById('nav-login').style.display = 'block';
    	document.getElementById('nav-signup').style.display = 'block';
    	document.getElementById('nav-logout').style.display = 'none';
	}
}

async function getJsonData(url, options)
{
	var returnData = null
	await fetch(url, options)
	.then((resp) => resp.json())
	.then(function(data) 
	{
		returnData = data;
		
	})
	.catch(function(error) 
	{
		console.log(error);
	}); 

	return returnData;
}

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

function displayError(str)
{
	let errorElement = document.getElementById('error-display');

	if(errorElement != null)
	{
		errorElement.innerHTML = str;
		errorElement.style.display = 'block';
	}
	else
	{
		console.log('NO ERROR DISPLAY ELEMENT');
	}
}

function hideError()
{
	let errorElement = document.getElementById('error-display');

	if(errorElement != null)
	{
		errorElement.innerHTML = '';
		errorElement.style.display = 'none';
	}
	else
	{
		console.log('NO ERROR DISPLAY ELEMENT');
	}
}

// ###################################################################
function displayElement(id,str)
{
	let element = document.getElementById(id);

	if(element != null)
	{
		element.style.display = 'block';

		if(str != null)
		{
			element.innerHTML = str;
		}
	}
	else
	{
		console.log('NO ELEMENT FOUND');
	}
}

function displayFlexElement(id,str)
{
	let element = document.getElementById(id);

	if(element != null)
	{
		element.style.display = 'flex';

		if(str != null)
		{
			element.innerHTML = str;
		}
	}
	else
	{
		console.log('NO ELEMENT FOUND');
	}
}

function hideElement(id)
{
	let element = document.getElementById(id);

	if(element != null)
	{
		element.style.display = 'none';
	}
	else
	{
		console.log('NO ELEMENT FOUND');
	}
}
// ###################################################################

function getCheckedRadioValue(...args) 
{
	let checked = null;
	args.forEach(function(element) {
  		// console.log(element);
  		// console.log(element.checked);
  		if(element.checked)
  		{
  			checked = element.value;
  		}
	});

	return checked

     //args is an Array
     // console.log(args);
     // //You can pass this array as parameters to another function
     // console.log(...args);
}

function logout()
{
	deleteToken();
	window.location.href = getBaseUrl() + '';
	// adjustNavbar();
}

adjustNavbar();