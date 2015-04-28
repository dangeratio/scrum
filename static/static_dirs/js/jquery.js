$(document).ready(function() {
    // js to build an auto-key-title
    $('input#id_title').keyup(function(){
        var tmp = $('input#id_title').val().replace(' ', '').substring(0,5).toUpperCase();
        $('input#id_key').val(tmp);
    });

    // release hovers for project detail pagej - a7cadb

    $('.parent-border-hover').hover(
        function() {
            $(this).parent().addClass('parent-hover-style');
        }, function() {
            $(this).parent().removeClass('parent-hover-style');
        }
    );

    // version control for releases

    $('input#id_number').after(" \
        Minor <input type='button' onclick='javascript:id_number_decrease_sm()' value='-' /> \
        <input type='button' onclick='javascript:id_number_increase_sm()' value='+' />&nbsp;&nbsp;&nbsp; \
        Major <input type='button' onclick='javascript:id_number_decrease()' value='-' /> \
        <input type='button' onclick='javascript:id_number_increase()' value='+' /> \
        ");


});


// version control for releases

function id_number_decrease() {
    id_number = document.getElementById('id_number');
    id_number.value = parseFloat(id_number.value) - 1;
}

function id_number_increase() {
    id_number = document.getElementById('id_number');
    id_number.value = parseFloat(id_number.value) + 1;
}

function id_number_decrease_sm() {
    id_number = document.getElementById('id_number');
    id_number.value = parseFloat(id_number.value) - 0.1;
}

function id_number_increase_sm() {
    id_number = document.getElementById('id_number');
    id_number.value = parseFloat(id_number.value) + 0.1;
}
