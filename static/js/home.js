/////////// Show/Hide

function showTooltip(element, message) {
    document.getElementById(element).style.opacity = 0.6;
    document.getElementById(element).innerHTML = message;
};

function hideTooltip(element) {
    document.getElementById(element).style.opacity = 0;
    document.getElementById(element).innerHTML = '';
};


/////////// Search Box

var __searchbox_active = false;

var __active_searchbox = function() {
    if (!__searchbox_active) {
        __searchbox_active = true;
        document.getElementById("searchbox").value="";
    }
};

var __deactive_searchbox=function() {
    if (document.activeElement != document.getElementById("searchbox")) {
        __searchbox_active = false;
        document.getElementById("searchbox").value="جستجو ...";
    }
};

var __search_request = function() {
    alert(document.getElementById("searchbox").value);
};

var __key_handler = function(key_event) {
    if (__searchbox_active && key_event.keyCode == 13) {
        __search_request();
    }
};

function clicked(element) {
    element.value='';
    element.onclick='';
    element.style.color='black';
};

function match(element2, id) {
    element1 = document.getElementById(id);
    if(element1.value != element2.value)
        element2.style.borderColor="#dd4b39";
    else
        element.style.borderColor="rgba(0,0,0,0.2)";
};

function secure(element) {
    if(element.value.length < 8)
        element.style.borderColor="#dd4b39";
    else
        element.style.borderColor="rgba(0,0,0,0.2)";
};
