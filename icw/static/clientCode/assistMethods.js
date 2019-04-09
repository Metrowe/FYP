var baseUrl;

function clickTest()
{
	console.log('click')
}

function getBaseUrl()
{
	if(baseUrl == null)
	{
		baseUrl = window.location.href.slice(0, window.location.href.indexOf(window.location.pathname)) + '/';
	}

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

async function getImageFromUrl(url)
{
	let imageFile = null;

	await fetch(url)
    .then(function(resp) 
	{ 
		if(resp.status == 200)
		{
			return resp.blob();
		}
		else
		{
			return null;
		}
	})
    .then(function(blob) 
    {
    	if(blob != null)
    	{
    		imageFile = new File([blob], "uploaded_file.jpg", { type: "image/jpeg", lastModified: Date.now() });
    	}
    });

	return imageFile;
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

function getCheckedRadioValue(...args) 
{
	let checked = null;
	//args is an Array
	//You can pass this array as parameters to another function
	args.forEach(function(element) {
  		if(element.checked)
  		{
  			checked = element.value;
  		}
	});

	return checked
}

function logout()
{
	deleteToken();
	window.location.href = getBaseUrl() + '';
}

adjustNavbar();