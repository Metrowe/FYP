

async function getJsonData(url)
{
	var returnData = null
	await fetch(url)
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

async function testget()
{
	url = window.location.href + "testreq"
	let testData = await getJsonData(url);

	console.log(url);
	console.log(testData);

	// document.getElementById("profileAvatar").src = userData.avatar_url;	
}
// window.location = "https://www.example.com";
console.log("ssadasdsasdasdsasdsasd");
testget();