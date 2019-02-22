

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

//Rename this or mix it with
async function tempgetJsonData(url)
{
	let formData = new FormData();
	formData.append("image", document.getElementById("changeid").files[0]);
	


	var returnData = null
	// await fetch(url)
	await fetch(url, {method: "POST", body: formData})
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

async function postUpload()
{
	console.log("postupload called");



	// url = window.location.href + "oldupload"
	url = window.location.href + "upload"
	let testData = await tempgetJsonData(url);

	document.getElementById('upload-input').src = testData.inputPath
	document.getElementById('upload-output').src = testData.outputPath

	document.getElementById('upload-label').textContent = testData.label


	console.log(url);
	console.log(testData);

	// document.getElementById("profileAvatar").src = userData.avatar_url;	
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