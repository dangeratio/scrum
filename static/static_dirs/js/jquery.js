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

});