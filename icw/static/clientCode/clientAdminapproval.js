function getSubmissionMarkup(submission)
{
	return `
		<div id="moditem${submission.id}" class="col-lg-4 col-md-6 col-sm-12 theme-colour-b" >
			<div class="row theme-colour-c" style="margin: 5px">
				<div class="col ">
					<div class="row">
						<div class="col-6 ">
							<input onclick="setapprovalAttempt(true,${submission.id});" type="button" class="btn btn-primary btn-lg btn-block" value="Approve">
						</div>
						<div class="col-6 ">
							<input onclick="setapprovalAttempt(false,${submission.id});" type="button" class="btn btn-primary btn-lg btn-block" value="Deny">
						</div>
					</div>
					<div class="row">
						<div class="col-6 ">
							<img style="max-width: 150px" src="${submission.originalPath}" alt="Failed original load">
						</div>
						<div class="col-6 ">
							<img style="max-width: 150px" src="${submission.isolatePath}" alt="Failed isolate load">
						</div>
					</div>
					<div class="row">
						<div class="col-12 ">
							<img style="max-width: 150px" src="${submission.summaryPath}" alt="Failed original load">
						</div>
					</div>
					
					<div class="row">
						<div class="col ">
							<b>Animal    :</b> ${submission.label} <b>| Correct:</b> ${submission.rateClassify}
						</div>
					</div>

					<div class="row">
						<div class="col">
							<input id="label-input${submission.id}" list="labels" class="w-100" type="text" value="" placeholder="Animal">
							<datalist id="labels">
								<option value="antelope"><option value="bat"><option value="beaver"><option value="blue whale"><option value="bobcat"><option value="buffalo"><option value="chihuahua"><option value="chimpanzee"><option value="collie"><option value="cow"><option value="dalmatian"><option value="deer"><option value="dolphin"><option value="elephant"><option value="fox"><option value="german shepherd"><option value="giant panda"><option value="giraffe"><option value="gorilla"><option value="grizzly bear"><option value="hamster"><option value="hippopotamus"><option value="horse"><option value="humpback whale"><option value="killer whale"><option value="leopard"><option value="lion"><option value="mole"><option value="moose"><option value="mouse"><option value="otter"><option value="ox"><option value="persian cat"><option value="pig"><option value="polar bear"><option value="rabbit"><option value="raccoon"><option value="rat"><option value="rhinoceros"><option value="seal"><option value="sheep"><option value="siamese cat"><option value="skunk"><option value="spider monkey"><option value="squirrel"><option value="tiger"><option value="walrus"><option value="weasel"><option value="wolf"><option value="zebra">
							</datalist>
						</div>	
					</div>

					<div class="row">
						<div class="col ">
							<b>Isolation :</b> ${submission.rateIsolate}
						</div>
					</div>
					<div class="row">
						<div class="col ">
							<b>Result txt:</b> ${submission.commentResult}
						</div>
					</div>
					<div class="row">
						<div class="col ">
							<b>Websit txt:</b> ${submission.commentSite}
						</div>
					</div>
					<div class="row">
						<div class="col ">
							<b>Username:</b> ${submission.username}
						</div>
					</div>
					<div class="row">
						<div class="col-md-12 ">
							<input onclick="deleteSubmissionAttempt(${submission.id});" type="button" class="btn btn-danger btn-lg btn-block" value="Delete">
						</div>
					</div>
				</div>
			</div>	
		</div>
		`;
}

// deleteSubmissionAttempt(${submission.id})

function removeElement(elementId) {
    // Removes an element from the document
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}

function populatePage(submissionList)
{
	let row = document.getElementById("adminRow");

	if( submissionList.length > 0 )
	{
		row.innerHTML = "";

		submissionList.forEach(function (submission) {
	  		row.innerHTML = row.innerHTML + getSubmissionMarkup(submission);
		});
	}
	else
	{
		row.innerHTML = "No results";
	}
}

async function adminapprovalAttempt()
{
	let url = getBaseUrl() + "adminapprovalrequest";
	let headers = { 'Authorization': getToken() };
	let results = await getJsonData(url,{method: 'POST', headers: headers});

	if( Array.isArray(results) )
	{
		let submissionList = results;
		populatePage(submissionList)
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

async function setapprovalAttempt(approval,submissionId)
{	
	let labelElement = document.getElementById('label-input'+submissionId);
	label = labelElement.value.replace(' ', '+');

	let url = getBaseUrl() + "setapprovalrequest";

	let headers = { 'Authorization': getToken() };
	let formData = new FormData();
	formData.append('approval', approval);
	formData.append('submissionId', submissionId);

	if (label != '')
	{
		formData.append('newLabel', label);
	}	

	let result = await getJsonData(url,{method: 'POST', headers: headers, body: formData});

	if (results != null && 'message' in result)
	{
		console.log(result.message);

		let elementId = 'moditem'+submissionId;
		removeElement(elementId);
	}
	else
	{
		let errorMessage = 'Set Approval Failed';

		if (results != null && 'error' in result) 
		{
	    	errorMessage = result.error;
		}

		displayError(errorMessage);
	}
}

async function deleteSubmissionAttempt(submissionId)
{	
	let url = getBaseUrl() + "deletesubmissionrequest";

	let headers = { 'Authorization': getToken() };
	let formData = new FormData();
	formData.append('submissionId', submissionId);

	let result = await getJsonData(url,{method: 'POST', headers: headers, body: formData});

	if (results != null && 'message' in result)
	{
		console.log(result.message);

		let elementId = 'moditem'+submissionId;
		removeElement(elementId);
	}
	else
	{
		let errorMessage = 'Delete Submission Failed';

		if (results != null && 'error' in result) 
		{
	    	errorMessage = result.error;
		}

		displayError(errorMessage);
	}
}

adminapprovalAttempt()