$(document).ready(function() {

    $('#status_field').fadeOut('fast');

    dragula([backlog_items, release_items]).on('drop', function (el, container) {
        setTimeout(function () {
            // send ajax to update the record
            trigger_ajax(el, container);
        }, 0);
    });

    function trigger_ajax(el, container) {

        var new_release = container.id.toString().replace('release','');
        var item_to_move = el.id.toString().replace('item','');

        // alert(item_to_move + '|' + new_release);

        var_url = '/projects/ajax/release_quick/';
        var_url += new_release;
        var_url += '/';
        var_url += item_to_move;

        var_csrf_data = {"csrfmiddlewaretoken": csrf_token};

        $.ajax({
            type: "POST",
            url: var_url,
            data: var_csrf_data,
            dataType: '',
            success: function(data, textStatus, xhr) {
                setTimeout( function() {
                    $('#status_field').html(data);
                    $('#status_field').fadeIn('slow');
                }, 0);
                setTimeout( function() {
                    $('#status_field').fadeOut('fast');
                }, 500);
            },
            error: function(xhr, textStatus, errorThrown) {
                setTimeout( function() {
                    $('#status_field').html(textStatus);
                    $('#status_field').fadeIn('slow');
                }, 0);
                setTimeout( function() {
                    $('#status_field').fadeOut('slow');
                }, 500);
            }
        });

    }

    /*
    // success: ajax_success,
    var status_div = document.getElementById('status_field');
    function ajax_success(returned) {
        status_div = returned;
    }
    */

});