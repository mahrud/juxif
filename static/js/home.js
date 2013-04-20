/////////// Tool Tip Show/Hide

var showTooltip = function(element, tooltip){
    document.getElementById(element).className = "tooltip_visible";
    document.getElementById(element).innerHTML = tooltip;
};

var hideTooltip = function(element) {
    document.getElementById(element).className = "tooltip";
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
