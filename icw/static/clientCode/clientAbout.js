sessionStorage.aaa = 'aaa';
sessionStorage.bbb = 'bbb';

console.log(typeof sessionStorage);
console.log(sessionStorage);
console.log(getToken());


async function validateTokenExample()
{
	// let usernameElement = document.getElementById('login-username');
	// let passwordElement = document.getElementById('login-password');

	url = getBaseUrl() + 'ggggg';

	let formData = new FormData();
	formData.append('token', getToken());

	let headers = { 'Authorization': getToken() };

	let result = await getJsonData(url,{method: 'POST', headers: headers, body: formData});

	console.log(url);
	console.log(result);
}

validateTokenExample();


// fetch('www.example.net', {
//   method: 'POST',
//   headers: { 'Authorization': 'Bearer ' + token }
// });