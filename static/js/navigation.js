function navbar()
{
	var addr;
	try {
		addr = document.getElementById("page").value;
	}
	catch (error) {
		//oops, there are some security problems not letting us access, so...
		addr = 'none';
	}
	var page = addr;
	correctHighlight();

	document.getElementById("nav_home").src = "/static/img/whitesmall/home.png";
	document.getElementById("nav_profile").src = "/static/img/whitesmall/profile.png";
	document.getElementById("nav_problem").src = "/static/img/whitesmall/problem.png";
	document.getElementById("nav_algorithm").src = "/static/img/whitesmall/algorithm.png";
	document.getElementById("nav_course").src = "/static/img/whitesmall/course.png";
	document.getElementById("nav_event").src = "/static/img/whitesmall/event.png";
	document.getElementById("nav_news").src = "/static/img/whitesmall/news.png";
	document.getElementById("nav_login").src = "/static/img/whitesmall/login.png";
    document.getElementById("nav_register").src = "/static/img/whitesmall/register.png";
	
	if (page == "home")
        document.getElementById("nav_home").src = "/static/img/orangesmall/home.png";
	if (page == "profile")
        document.getElementById("nav_profile").src = "/static/img/orangesmall/profile.png";
	if (page == "problem")
        document.getElementById("nav_problem").src = "/static/img/orangesmall/problem.png";
	if (page == "algorithms")
        document.getElementById("nav_algorithm").src = "/static/img/orangesmall/algorithm.png";
	if (page == "course")
        document.getElementById("nav_course").src = "/static/img/orangesmall/course.png";
	if (page == "event")
        document.getElementById("nav_event").src = "/static/img/orangesmall/event.png";
	if (page == "news")
        document.getElementById("nav_news").src = "/static/img/orangesmall/news.png";
	if (page == "login")
        document.getElementById("nav_login").src = "/static/img/orangesmall/login.png";
    if (page == "register")
        document.getElementById("nav_register").src = "/static/img/orangesmall/register.png";
};

function navigate(dest)
{
//  page = dest;

//  Using jQuery's ajax method since it automatically sets the HTTP_X_REQUESTED_WITH header so that
//  we can determine ajax requests in views via the request.is_ajax method
  
//  $.get(nav_map(dest), 
//      function(data) {
//          document.getElementById("html").innerHTML = data;
//          document.write(data);
//      }
//  );
//  navbar();
  
    window.location = "/"+nav_map(dest);
};


function nav_map(dest)
{
    if (dest == "home")
        return "";

    if (dest == "admin")
        return "admin";
    if (dest == "news")
        return "news";

    if (dest == "course")
        return "course";
    if (dest == "article")
        return "article";

    if (dest == "algorithm")
        return "algorithm";
    if (dest == "problem")
        return "problem";
    if (dest == "contest")
        return "contest";

    if (dest == "register")
        return "accounts/register";
    if (dest == "logout")
        return "accounts/logout";
    if (dest == "login")
        return "accounts/login";

    if (dest == "404")
        return  "four-oh-four";

    return  "four-oh-four";
};
