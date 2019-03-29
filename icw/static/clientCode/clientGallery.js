function getImageMarkup(path,label)
{
	return `
		<div class="col-md-4 theme-colour-c">
			<div style="margin:3%">
				<img class="img-responsive border mx-auto d-block" src="${path}" width="100%" ">
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
	  		row.innerHTML = row.innerHTML + getImageMarkup(image.path,image.label);
		});
	}
	else
	{
		row.innerHTML = "No results";
	}
}

async function galleryAttempt()
{
	let url = getBaseUrl() + "galleryrequest";

	let labelElement = document.getElementById('label-input');

	let typeInputElement1 =  document.getElementById('type-input1');
	let typeInputElement2 =  document.getElementById('type-input2');
	let typeInputElement3 =  document.getElementById('type-input3');
	let typeInputElement4 =  document.getElementById('type-input4');

	label = label = labelElement.value.replace(' ', '+');
	type = getCheckedRadioValue(typeInputElement1,typeInputElement2,typeInputElement3,typeInputElement4);
	labelElement.value = '';

	let formData = new FormData();
	formData.append('category', type);
	formData.append('label', label);

	let response = await getJsonData(url,{method: "POST", body: formData});

	if( Array.isArray(response) )
	{
		let imageList = response.filter(result => result.path != null && result.label != null);
		populateGallery(imageList)
	}
	else
	{
		let errorMessage = 'Search Failed';

		if (response != null && "error" in response) 
		{
	    	errorMessage = response.error;
		}

		displayError(errorMessage);
	}
}

galleryAttempt()