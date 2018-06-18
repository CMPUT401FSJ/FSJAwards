function toggle(source) {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < checkboxes.length; i++) {
        if ( !checkboxes[i].disabled ) {
            checkboxes[i].checked = source.checked;
        }
    }
}

function award_toggle(source) {
    var checkboxes = document.getElementsByName("awards");
    //var checkboxes = $("input[name='awards']:checkbox");

    for (var i = 0; i < checkboxes.length; i++) {
        if ( !checkboxes[i].disabled ) {
            checkboxes[i].checked = source.checked;
        }
    }
}