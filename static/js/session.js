$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});



	var login_handler = function(result) {
		if (result == true) {
			navigate('home');
		}
	};
	
	var __login = function() {
		var username = document.getElementById("id_username").value;
		var password = document.getElementById("id_password").value;
		var stay = "false";
		if (document.getElementById("stay").value == "on")
			stay = "true";
		sessionLogin(username, password, stay, login_handler);
	};

var sessionPanelOn = function() {
	document.getElementById("session").className = "session";
	document.getElementById("extpanel").className = "extpanel_invis";
};

var sessionPanelOff = function() {
	document.getElementById("session").className = "session_invis";
	document.getElementById("extpanel").className = "extpanel";
};

var sessionInit = function() {
};

var sessionClear = function() {
	if (localStorage['keep logged in'] &&
		localStorage['keep logged in'] == 'true') {
		
	}
	else {
		localStorage['username'] = '';
	}
};

var sessionLogin = function(username, password, stay, handler) {
	//TODO: write this to go confirm login request from server
	//using websocket;
	$.post(navigation_map("login"),
	  { id_username: username, id_password: password },
	  function(data){
	    if (data == "valid") {
                localStorage['username'] = username;

                if (stay == 'true')
                        localStorage['keep logged in'] = 'true';
                else
                        localStorage.removeItem('keep logged in');

                handler(true);

	    } else if (data == "invalid") {
            document.getElementById("alert").innerHTML = "کاربری با این مشخصات وجود ندارد ";
        } else if (data == "inactive") {
            document.getElementById("alert").innerHTML = "کاربر غیر فعال است ";
        }

	  }, "html"
	);
    
};
var sessionLogoff = function() {
	localStorage['username'] = "";
	updateSessionPanel();
};

var updateSessionPanel = function() {
	if (localStorage['username'] && localStorage['username'] != "") {
		document.getElementById("session_uname").innerHTML = localStorage['username'];
		sessionPanelOn();
	}
	else
		sessionPanelOff();
};


//var __register = function() {
//    $.post(navigation_map("register"),
//	   $("#inputArea").serialize(),
//	  function(data){
//	    document.getElementById("main_section").innerHTML = data;
//          alert(data);
//	    checkupPage();
//	    correctHighlight();
//	  }, "html"
//	);
//};
