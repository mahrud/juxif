function navbar()
{
    page = location.pathname.split('/')[1];
    section = location.pathname.split('/')[2];

	document.getElementById("navbar_home").src = "/static/img/whitesmall/home.png";
	document.getElementById("navbar_accounts").src = "/static/img/whitesmall/accounts.png";
	document.getElementById("navbar_problem").src = "/static/img/whitesmall/problem.png";
	document.getElementById("navbar_algorithm").src = "/static/img/whitesmall/algorithm.png";
	document.getElementById("navbar_course").src = "/static/img/whitesmall/course.png";
	document.getElementById("navbar_contest").src = "/static/img/whitesmall/contest.png";
	document.getElementById("navbar_news").src = "/static/img/whitesmall/news.png";

	document.getElementById("navbar_register").src = "/static/img/whitesmall/register.png";
	document.getElementById("navbar_login").src = "/static/img/whitesmall/login.png";
	
	if (page == "")
        document.getElementById("navbar_home").src = "/static/img/orangesmall/home.png";
	if (page == "news")
        document.getElementById("navbar_news").src = "/static/img/orangesmall/news.png";

	if (page == "problem")
        document.getElementById("navbar_problem").src = "/static/img/orangesmall/problem.png";
	if (page == "algorithm")
        document.getElementById("navbar_algorithm").src = "/static/img/orangesmall/algorithm.png";
	if (page == "course")
        document.getElementById("navbar_course").src = "/static/img/orangesmall/course.png";
	if (page == "contest")
        document.getElementById("navbar_contest").src = "/static/img/orangesmall/contest.png";

	if (page == "accounts" && section == "login")
        document.getElementById("navbar_login").src = "/static/img/orangesmall/login.png";
	if (page == "accounts" && section == "register")
        document.getElementById("navbar_register").src = "/static/img/orangesmall/register.png";
	else if (page == "accounts")
        document.getElementById("navbar_accounts").src = "/static/img/orangesmall/accounts.png";
};

function navigate(dest)
{
//  page = dest;

//  Using jQuery's ajax method since it automatically sets the HTTP_X_REQUESTED_WITH header so that
//  we can determine ajax requests in views via the request.is_ajax method
  
//  $.get(navbar_map(dest), 
//      function(data) {
//          document.getElementById("html").innerHTML = data;
//          document.write(data);
//      }
//  );
//  navbar();
  
    window.location = navbar_map(dest);
};


function navbar_map(dest)
{
    urls = {
        "home":         "/",
        "news":         "/news",
        "course":       "/course",
        "contest":      "/contest",
        "problem":      "/problem",
        "algorithm":    "/algorithm",
        "accounts":     "/accounts",
        "register":     "/accounts/register",
        "logout":       "/accounts/logout",
        "login":        "/accounts/login",
        "404":          "/four-oh-four",
        };

    try
    {
        return urls[dest];
    }
    catch(err)
    {
        return "/four-oh-four";
    }

};
