$(document).ready(function() {

    var time_to_leave_status_messages = 5000

    //$('#status_field').fadeOut('fast');

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

        var_url = '/ajax/release_quick/';
        var_url += new_release;
        var_url += '/';
        var_url += item_to_move;

        var_csrf_data = {"csrfmiddlewaretoken": csrf_token};

        var new_el_id = guid();
        var new_el_s = "<div id='" + new_el_id + "' class='alert alert-success alert-dismissible'>";
        new_el_s += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
        var new_el_s_error = "<div id='" + new_el_id + "' class='alert alert-danger alert-dismissible'>";
        new_el_s_error += '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
        var new_el_e = "</div>";

        $.ajax({
            type: "POST",
            url: var_url,
            data: var_csrf_data,
            dataType: '',
            success: function(data, textStatus, xhr) {
                // show alert
                setTimeout( function() {
                    curr_html = $('#status_field').html();
                    $('#status_field').html(curr_html + new_el_s + data + new_el_e);
                    $('#' + new_el_id).fadeIn('slow');
                }, 0);
                // remove alert
                setTimeout( function() {
                    $('#' + new_el_id).fadeOut('slow');
                }, time_to_leave_status_messages);
            },
            error: function(xhr, textStatus, errorThrown) {
                setTimeout( function() {
                    curr_html = $('#status_field').html();
                    $('#status_field').html(curr_html + new_el_s_error + textStatus + new_el_e);
                    $('#' + new_el_id).fadeIn('slow');
                }, 0);
                setTimeout( function() {
                    $('#' + new_el_id).fadeOut('slow');
                }, time_to_leave_status_messages);
            }
        });

    }

});

function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}