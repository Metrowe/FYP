var baseUrl;

function getBaseUrl()
{
	if(baseUrl == null)
	{
		baseUrl = window.location.href.slice(0, window.location.pathname.length * -1) + '/';
	}

	return baseUrl;
}

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