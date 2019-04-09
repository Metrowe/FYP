let submissionToken = null;

async function uploadAttempt()
{
	let galleryinputElement1 = document.getElementById('gallery-input1');
	let galleryinputElement2 = document.getElementById('gallery-input2');
	let datasetinput1 = document.getElementById('dataset-input1');
	let datasetinput2 = document.getElementById('dataset-input2');

	let fileUploadElement = document.getElementById('upload-file');
	let urlUploadElement = document.getElementById('upload-url');

	let uploadUrl = urlUploadElement.value;

	let uploadFile = null;

	hideElement('feedback-form');

	if(fileUploadElement.files[0] != null)
	{
		uploadFile = fileUploadElement.files[0];
	}
	else if(validString(uploadUrl))
	{
		try 
		{
			let tempFile = await getImageFromUrl(uploadUrl)

			if(tempFile != null)
			{
				uploadFile = tempFile;
			}
			else
			{
				displayError('Invalid image URL');
				return;
			}
		}
		catch(err) 
		{
			console.log(err);
			displayError('Image url denied external access')
			return;
		}
	}

	if(uploadFile != null)
	{
		let permissionGallery = getCheckedRadioValue(galleryinputElement1,galleryinputElement2);
		let permissionDataset = getCheckedRadioValue(datasetinput1,datasetinput2);

		hideElement('message-display');
		hideError()

		let heading = document.getElementById('upload-heading');
		let inputImage = document.getElementById('upload-input');
		let outputImage = document.getElementById('upload-output');
		let summaryImage = document.getElementById('upload-summary');
		let label = document.getElementById('upload-label');
		
		heading.textContent = "Your upload"
		inputImage.src = "";
		outputImage.src = "";
		summaryImage.src = "";
		label.textContent = "loading...";

		//prepare get jsondata
		url = getBaseUrl() + "uploadRequest";

		let headers = { 'Authorization': getToken() };
		let formData = new FormData();
		formData.append("image", uploadFile);
		formData.append("permissionGallery", permissionGallery);
		formData.append("permissionDataset", permissionDataset);

		let response = null;

		if(headers.Authorization == null)
		{
			response = await getJsonData(url,{method: "POST", body: formData});
		}
		else
		{
			response = await getJsonData(url,{method: 'POST', headers: headers, body: formData});
		}

		if( response != null && 'inputPath' in response && 'outputPath' in response && 'summaryPath' in response && 'label' in response && 'submissionToken' in response)
		{
			inputImage.src = response.inputPath;
			outputImage.src = response.outputPath;
			label.textContent = response.label;
			summaryImage.src = response.summaryPath;

			submissionToken = response.submissionToken;

			displayElement('feedback-form',null);
		}
		else
		{
			inputImage.src = 'static/images/examples/walrus-input-example.png';
			outputImage.src = 'static/images/examples/walrus-output-example.png';
			summaryImage.src = 'static/images/examples/walrus-summary-example.png';
			label.textContent = 'Walrus';
			heading.textContent = 'Example';

			let errorMessage = 'Upload Failed';

			if (response != null && 'error' in response) 
			{
		    	errorMessage = response.error;
			}

			displayError(errorMessage);
		}
	}
	else
	{
		displayError('No file selected for upload');
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

		hideElement('message-display');
		hideElement('error-display');
		
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

			let response = await getJsonData(url,{method: "POST", body: formData});

			if (response != null && "error" in response) 
			{
		    	errorMessage = response.error;
		    	displayError(errorMessage);
			}
			else
			{
				submissionToken = null;
				hideElement('feedback-form');
				displayElement('message-display','Thanks for your feedback');
			}
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

var rateVisible = null;

function toggleRateExample()
{
	if(rateVisible == null)
	{
		rateVisible = false;
	}

	rateVisible = !rateVisible;

	if(rateVisible)
	{
		displayFlexElement('example-rateIsolate');
	}
	else
	{
		hideElement('example-rateIsolate');
	}
}