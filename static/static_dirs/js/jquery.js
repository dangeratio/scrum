$(document).ready(function() {
    // js to build an auto-key-title
    $('input#id_title').keyup(function(){
        var tmp = $('input#id_title').val().replace(' ', '').substring(0,3).toUpperCase();
        $('input#id_key_title').val(tmp);
    });
});