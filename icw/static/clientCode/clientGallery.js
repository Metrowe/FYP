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

	// if( Array.isArray(pathList) && pathList.length > 0 )
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

// async function initialGalleryContents(type,label)
// {
// 	let url = getBaseUrl() + "galleryImages";

// 	let formData = new FormData();
// 	formData.append('type', type);
// 	formData.append('label', label);

// 	let result = await getJsonData(url,{method: "POST", body: formData});

// 	// let results = await getJsonData(url,null);

// 	pathList = results.map(result => result.path);

// 	populateGallery(pathList)

// 	console.log(url);
// 	console.log(results);
// }


async function galleryAttempt()
{
	let url = getBaseUrl() + "galleryrequest";

	let labelElement = document.getElementById('label-input');

	let typeInputElement1 =  document.getElementById('type-input1');
	let typeInputElement2 =  document.getElementById('type-input2');
	let typeInputElement3 =  document.getElementById('type-input3');

	label = label = labelElement.value.replace(' ', '+');
	type = getCheckedRadioValue(typeInputElement1,typeInputElement2,typeInputElement3);
	labelElement.value = '';

	let formData = new FormData();
	formData.append('type', type);
	formData.append('label', label);

	console.log('label: ' + label);

	let results = await getJsonData(url,{method: "POST", body: formData});

	if( Array.isArray(results) )
	{
		let imageList = results.filter(result => result.path != null && result.label != null);
		// let pathList = results.map(result => result.path).filter(path => path != null);
		populateGallery(imageList)
	}
	else
	{
		let errorMessage = 'Search Failed';

		if (results != null && "error" in results) 
		{
	    	errorMessage = results.error;
		}

		displayError(errorMessage);
	}

	console.log(url);
	console.log(results);
}

galleryAttempt()

// async function galleryImagesGetAttempt(type,label)
// async function galleryImagesGetAttempt()
// {
// 	let url = getBaseUrl() + "galleryImages";

// 	let labelElement = document.getElementById('label-input');
// 	// let typeElement = document.getElementById('label-input');

// 	let typeInputElement1 =  document.getElementById('type-input1');
// 	let typeInputElement2 =  document.getElementById('type-input2');
// 	let typeInputElement3 =  document.getElementById('type-input3');



// 	console.log('label: ' + labelElement.value);

// 	// console.log(labelElement);

// 	// let passwordElement = document.getElementById('login-password');

// 	// if( validString(usernameElement.value) && validString(passwordElement.value))
// 	// {
// 		// console.log(true);
// 		// url = getBaseUrl() + "loginrequest";

// 		// let formData = new FormData();
// 		// formData.append('username', usernameElement.value);
// 		// formData.append('password', passwordElement.value);


	

// 	label = labelElement.value;


// 	if(label == undefined)
// 	{
// 		console.log('label is undefined: ' + label);
// 	}

// 	if(label == '')
// 	{
// 		label == null;
// 		console.log('label is empty string: ' + label);

// 	}
// 	else
// 	{
// 		label = labelElement.value.replace(' ', '+');
// 	}
// 	labelElement.value = '';

// 	type = getCheckedRadioValue(typeInputElement1,typeInputElement2,typeInputElement3);

// 	// console.log(type);

// 	// return;

// 	let formData = new FormData();
// 	formData.append('type', 'Original');
// 	formData.append('label', label);

// 	console.log('label: ' + label);


// 	let results = await getJsonData(url,{method: "POST", body: formData});

// 	if( Array.isArray(results) )
// 	{
// 		let pathList = results.map(result => result.path).filter(path => path != null);
// 		populateGallery(pathList)
// 	}
// 	else
// 	{
// 		// let errorElement = document.getElementById('error-display');
// 		let errorMessage = 'Search Failed';

// 		if ("error" in results) 
// 		{
// 	    	errorMessage = results.error;
// 		}

// 		displayError(errorMessage);

// 		// errorElement.innerHTML = errorMessage;
// 		// errorElement.style.display = 'block';
// 	}

// 	// let pathList = results.map(result => result.path).filter(path => path != null);

// 	// var sources = images.filter(function(img) {
// 	// 	if (img.src.split('.').pop() === "json") {
// 	// 		return false; // skip
// 	// 	}
// 	// 		return true;
// 	// }).map(function(img) { return img.src; });


// 	// let pathList = results.map(result => result.path);

// 	// populateGallery(pathList)

// 	console.log(url);
// 	console.log(results);
// }



// async function initialGalleryContents()
// {
// 	let row = document.getElementById("galleryRow");

// 	//prepare get jsondata
// 	// url = window.location.href + "galleryImages";
// 	let url = getBaseUrl() + "galleryImages";

// 	let results = await getJsonData(url,null);

// 	row.innerHTML = "";
// 	// for (const result in results) {
// 	results.forEach(function (result) {
// 		console.log(result.path);
//   		row.innerHTML = row.innerHTML + getImageMarkup(result.path);
// 	});

// 	console.log(url);
// 	console.log(results);
// }

// const markup = `
// <div class="col-md-4 theme-colour-c">
// 	<div style="margin:3%" class=" card mb-4 ">
// 		<img style="margin:0%" class=" rounded " src="static/images/examples/elephant-example.jpg" alt="Display Image" width="100%">
// 	</div>
// 	<div class="card-body">
// 		<p class="card-text">
// 			This will have the label of the animal and possibly the user who uploaded.
// 		</p>
// 	</div>
// </div>
// `;

// async function testget()
// {
// 	url = window.location.href + "testreq"
// 	let testData = await getJsonData(url, null);

// 	console.log(url);
// 	console.log(testData);

// 	// document.getElementById("profileAvatar").src = userData.avatar_url;	
// }
// window.location = "https://www.example.com";
// console.log( "message" );
// console.log( document.getElementById("galleryRow").innerHTML );

// initialGalleryContents()
// galleryImagesGetAttempt('All',null);
// galleryImagesGetAttempt('All','blue+whale');
// galleryImagesGetAttempt('All','dalmation');
// galleryImagesGetAttempt('Original','bat');

// document.getElementById("galleryRow").innerHTML = markup