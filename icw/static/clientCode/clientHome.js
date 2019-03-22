console.log(window.location.pathname)
console.log(window.location.href)

let submissionToken = null;

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

async function uploadAttempt()
{
	hideElement('message-display');
	
	console.log('submissionToken',submissionToken);

	let inputImage = document.getElementById('upload-input');
	let outputImage = document.getElementById('upload-output');
	let label = document.getElementById('upload-label');
	
	inputImage.src = "";
	outputImage.src = "";
	label.textContent = "loading...";

	//prepare get jsondata
	url = getBaseUrl() + "upload";

	let headers = { 'Authorization': getToken() };
	let formData = new FormData();
	formData.append("image", document.getElementById("changeid").files[0]);
	formData.append("token", "placeholderToken");

	let result = null;

	if(headers.Authorization == null)
	{
		result = await getJsonData(url,{method: "POST", body: formData});
	}
	else
	{
		result = await getJsonData(url,{method: 'POST', headers: headers, body: formData});
	}

	// console.log('result = ', result);
	// console.log('inputPath' in result);
	// console.log('inputPath' in result);
	// console.log('inputPath' in result);
	// console.log('inputPath' in result);

	// console.log('result = ', result.inputPath);

	if( 'inputPath' in result && 'outputPath' in result && 'label' in result && 'submissionToken' in result)
	{
		inputImage.src = result.inputPath;
		outputImage.src = result.outputPath;
		label.textContent = result.label;

		submissionToken = result.submissionToken;

		displayElement('feedback-form',null);

		console.log(url);
		console.log(result);
	}
	else
	{
		let errorMessage = 'Upload Failed';

		if ('error' in result) 
		{
	    	errorMessage = result.error;
		}

		displayError(errorMessage);
	}
}

async function feedbackAttempt()
{
	hideError();

	if(submissionToken != null)
	{
		let rateclassElement1 = document.getElementById('feedback-rateclass1');
		let rateclassElement2 = document.getElementById('feedback-rateclass2');

		let rateisolateElement1 = document.getElementById('feedback-rateisolate1');
		let rateisolateElement2 = document.getElementById('feedback-rateisolate2');
		let rateisolateElement3 = document.getElementById('feedback-rateisolate3');
		let rateisolateElement4 = document.getElementById('feedback-rateisolate4');

		let resultcommentElement = document.getElementById('feedback-resultcomment');
		let sitecommentElement = document.getElementById('feedback-sitecomment');


		let rateClassify = getCheckedRadioValue(rateclassElement1,rateclassElement2);
		let rateIsolate = getCheckedRadioValue(rateisolateElement1,rateisolateElement2,rateisolateElement3,rateisolateElement4);
		let commentResult = resultcommentElement.value;
		let commentSite = sitecommentElement.value;

		
		if(rateClassify != null && rateIsolate != null)
		{

			//prepare get jsondata
			url = getBaseUrl() + "givefeedbackrequest";

			let formData = new FormData();
			formData.append('submissionToken', submissionToken);
			formData.append('rateClassify', rateClassify);
			formData.append('rateIsolate', rateIsolate);
			formData.append('commentResult', commentResult);
			formData.append('commentSite', commentSite);


			let result = await getJsonData(url,{method: "POST", body: formData});

			if ("error" in result) 
			{
		    	errorMessage = result.error;
		    	displayError(errorMessage);
			}
			else
			{
				submissionToken = null;
				hideElement('feedback-form');
				displayElement('message-display','Thanks for your feedback');
				// document.getElementById('feedback-form').style.display = 'none';
			}

			console.log(url);
			console.log(result);
		}
		else
		{
			displayError('Required fields are not all completed')
		}
	}
	else
	{
		displayError('No image has been uploaded')
	}
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
// testget();

// sessionStorage.accessToken = "placeholderToken";
// sessionStorage.temp = "canThisBeAccessed";
