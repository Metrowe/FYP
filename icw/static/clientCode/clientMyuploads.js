function getImageMarkup(path,label)
{
	return `
		<div class="col-md-4 theme-colour-c">
			<div style="margin:3%" class=" card mb-4 ">
				<img style="margin:0%" class=" rounded " src="${path}" alt="Display Image" width="100%">
			</div>
			<div class="card-body">
				<p class="card-text text-center">
					Animal: ${label}
				</p>
			</div>
		</div>
		`;
}

function populateGallery(imageList)
{
	let row = document.getElementById("galleryRow");

	if( imageList.length > 0 )
	{
		row.innerHTML = "";

		imageList.forEach(function (image) {
			// console.log(path);
	  		row.innerHTML = row.innerHTML + getImageMarkup(image.path,image.label);
		});
	}
	else
	{
		row.innerHTML = "No results";
	}
}

async function myuploadsAttempt()
{
	let url = getBaseUrl() + 'myuploadsrequest';

	let labelElement = document.getElementById('label-input');

	let typeInputElement1 =  document.getElementById('type-input1');
	let typeInputElement2 =  document.getElementById('type-input2');
	let typeInputElement3 =  document.getElementById('type-input3');

	label = labelElement.value.replace(' ', '+');
	type = getCheckedRadioValue(typeInputElement1,typeInputElement2,typeInputElement3);
	labelElement.value = '';

	let headers = { 'Authorization': getToken() };
	let formData = new FormData();
	formData.append('type', type);
	formData.append('label', label);

	// console.log('label: ' + label);

	let results = await getJsonData(url,{method: 'POST', headers: headers, body: formData});

	if( Array.isArray(results) )
	{
		let imageList = results.filter(result => result.path != null && result.label != null);
		// let pathList = results.map(result => result.path).filter(path => path != null);
		populateGallery(imageList)
	}
	else
	{
		let errorMessage = 'Search Failed';

		if ("error" in results) 
		{
	    	errorMessage = results.error;
		}

		displayError(errorMessage);
	}

	console.log(url);
	console.log(results);
}

myuploadsAttempt()