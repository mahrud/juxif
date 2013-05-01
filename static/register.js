function match(element2, id) {
    element1 = document.getElementById(id);
    if(element1.value == element2.value) {
        element2.style.borderColor="";
        return true;
    } else {
        element2.style.borderColor="#dd4b39";
        return false;
    };
};

function secure(element) {
    if(element.value.length > 6) {
        element.style.borderColor="";
        return true;
    } else {
        element.style.borderColor="#dd4b39";
        return false;
    };
};
