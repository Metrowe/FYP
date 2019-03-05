async function initialGalleryContents()
{
	let row = document.getElementById("galleryRow");

	//prepare get jsondata
	// url = window.location.href + "galleryImages";
	url = getBaseUrl() + "galleryImages";

	let results = await getJsonData(url,null);

	row.innerHTML = "";
	// for (const result in results) {
	results.forEach(function (result) {
		console.log(result.path)
  		row.innerHTML = row.innerHTML + 
  		`
			<div class="col-md-4 theme-colour-c">
				<div style="margin:3%" class=" card mb-4 ">
					<img style="margin:0%" class=" rounded " src="${result.path}" alt="Display Image" width="100%">
				</div>
				<div class="card-body">
					<p class="card-text">
						This will have the label of the animal and possibly the user who uploaded.
					</p>
				</div>
			</div>
		`;
	});

	console.log(url);
	console.log(results);
}

const markup = `
<div class="col-md-4 theme-colour-c">
	<div style="margin:3%" class=" card mb-4 ">
		<img style="margin:0%" class=" rounded " src="static/images/examples/elephant-example.jpg" alt="Display Image" width="100%">
	</div>
	<div class="card-body">
		<p class="card-text">
			This will have the label of the animal and possibly the user who uploaded.
		</p>
	</div>
</div>
`;

async function testget()
{
	url = window.location.href + "testreq"
	let testData = await getJsonData(url, null);

	console.log(url);
	console.log(testData);

	// document.getElementById("profileAvatar").src = userData.avatar_url;	
}
// window.location = "https://www.example.com";
console.log( "message" );
// console.log( document.getElementById("galleryRow").innerHTML );

initialGalleryContents()

// document.getElementById("galleryRow").innerHTML = markup