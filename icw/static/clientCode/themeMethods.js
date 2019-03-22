const themes = ['dark', 'electricity','sunset', 'pastel'];

//## START THEME MANAGEMENT ##//
function getTheme()
{
	console.log('gettheme()');
	var theme = themes[0];

	if ("theme" in sessionStorage) 
	{
		console.log('theme in sessionStorage');
    	theme = sessionStorage.theme;
	}

	return theme;
}

function assignTheme()
{
	theme = getTheme();

	themePath = 'static/themes/theme-' + theme + '.css';

	document.getElementById('style-theme').href = themePath;

	return themePath;
}

function setTheme(theme)
{
	if (themes.includes(theme)) 
	{
    	sessionStorage.theme = theme;
    	assignTheme();
	}
}
//## END THEME MANAGEMENT ##//

assignTheme();