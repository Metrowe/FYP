
//If no options set as null
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

async function postUpload()
{
	let inputImage = document.getElementById('upload-input');
	let outputImage = document.getElementById('upload-output');
	let label = document.getElementById('upload-label');
	
	inputImage.src = "";
	outputImage.src = "";
	label.textContent = "loading...";

	//prepare get jsondata
	url = window.location.href + "upload";

	let formData = new FormData();
	formData.append("image", document.getElementById("changeid").files[0]);

	let result = await getJsonData(url,{method: "POST", body: formData});

	inputImage.src = result.inputPath;
	outputImage.src = result.outputPath;
	label.textContent = result.label;

	console.log(url);
	console.log(result);
}



async function testget()
{
	url = window.location.href + "testreq"
	let testData = await getJsonData(url, null);

	console.log(url);
	console.log(testData);

	// document.getElementById("profileAvatar").src = userData.avatar_url;	
}
// window.location = "https://www.example.com";
console.log("ssadasdsasdasdsasdsasd");
testget();