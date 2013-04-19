var page;

var correctHighlight = function() {
	var doc = document;
	
	doc.getElementById("nav_home").src = "/static/img/whitesmall/home.png";
	doc.getElementById("nav_profile").src = "/static/img/whitesmall/profile.png";
	doc.getElementById("nav_problem").src = "/static/img/whitesmall/problem.png";
	doc.getElementById("nav_algorithm").src = "/static/img/whitesmall/algorithm.png";
	doc.getElementById("nav_course").src = "/static/img/whitesmall/course.png";
	doc.getElementById("nav_event").src = "/static/img/whitesmall/event.png";
	doc.getElementById("nav_news").src = "/static/img/whitesmall/news.png";
	
	doc.getElementById("session_log_in").src = "/static/img/whitesmall/log-in.png";
    doc.getElementById("session_sign_up").src = "/static/img/whitesmall/signup.png";
	
	if (page == "home") doc.getElementById("nav_home").src = "/static/img/orangesmall/home.png";
	if (page == "profile") doc.getElementById("nav_profile").src = "/static/img/orangesmall/profile.png";
	if (page == "problem") doc.getElementById("nav_problem").src = "/static/img/orangesmall/problem.png";
	if (page == "algorithm") doc.getElementById("nav_algorithm").src = "/static/img/orangesmall/algorithm.png";
	if (page == "course") doc.getElementById("nav_course").src = "/static/img/orangesmall/course.png";
	if (page == "event") doc.getElementById("nav_event").src = "/static/img/orangesmall/event.png";
	if (page == "news") doc.getElementById("nav_news").src = "/static/img/orangesmall/news.png";
	
	if (page == "login") doc.getElementById("session_log_in").src = "/static/img/orangesmall/log-in.png";
    if (page == "register") doc.getElementById("session_sign_up").src = "/static/img/orangesmall/signup.png";

};

var navigationInit = function() {
	navigate('home');
};

var checkPage = function() {
	//setTimeout("checkupPage();", 100);
	checkupPage();
};

var ends_with = function(a, b) {
	if (a.length < b.length) return false;
	return a.substring(a.length - b.length) == b;
}

var checkupPage = function() {
	var addr;
	try {
		addr = document.getElementById("page").value;
	}
	catch (error) {
		//oops, there are some security problems not letting us access, so...
		addr = 'none';
	}
	page = addr;
	correctHighlight();
};

var navigate = function(dest) {
	var doc = document;
	page = dest;

    // Using jQuery's ajax method since it automatically sets the HTTP_X_REQUESTED_WITH header so that
    // we can determine ajax requests in views via the request.is_ajax method
    $.get(navigation_map(dest), function(data){
        doc.getElementById("main_section").innerHTML = data;
    });
//	xmlhttp = new XMLHttpRequest();
//	xmlhttp.open("GET", navigation_map(dest), false);
//	xmlhttp.send();
//	doc.getElementById("main_section").innerHTML = xmlhttp.responseText;
    
	checkupPage();
	correctHighlight();
};

var navigation_map = function(dest_id) {
	if (dest_id == "home") return "home";
	if (dest_id == "login") return "accounts/login";
    if (dest_id == "register") return "accounts/register";
    if (dest_id == "news") return "news";
	return  "notfound";
};
