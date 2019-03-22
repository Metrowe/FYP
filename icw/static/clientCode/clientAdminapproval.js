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
						<div class="col ">
							<b>Animal    :</b> ${submission.label} <b>| Correct:</b> ${submission.rateClassify}
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

		if ("error" in results) 
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
	let url = getBaseUrl() + "setapprovalrequest";

	let headers = { 'Authorization': getToken() };
	let formData = new FormData();
	formData.append('approval', approval);
	formData.append('submissionId', submissionId);

	let result = await getJsonData(url,{method: 'POST', headers: headers, body: formData});

	if ('message' in result)
	{
		console.log(result.message);

		let elementId = 'moditem'+submissionId;
		removeElement(elementId);
	}
	else
	{
		let errorMessage = 'Set Approval Failed';

		if ('error' in result) 
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

	if ('message' in result)
	{
		console.log(result.message);

		let elementId = 'moditem'+submissionId;
		removeElement(elementId);
	}
	else
	{
		let errorMessage = 'Delete Submission Failed';

		if ('error' in result) 
		{
	    	errorMessage = result.error;
		}

		displayError(errorMessage);
	}
}

adminapprovalAttempt()