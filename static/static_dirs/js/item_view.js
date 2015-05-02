function trigger_start(item_id){
    var_csrf_data = {"csrfmiddlewaretoken": csrf_token};

    var_url = '/ajax/item_start/' + item_id

    $.ajax({
        type: "POST",
        url: var_url,
        data: var_csrf_data,
        dataType: '',
        success: function(data, textStatus, xhr) {
            // show alert
            setTimeout( function() {
                $('#start_link').hide();
                $('#date_started').html("Start:<br> " + data)
            }, 0);
        },
    });
}

function trigger_complete(item_id){
    var_csrf_data = {"csrfmiddlewaretoken": csrf_token};

    var_url = '/ajax/item_start/' + item_id

    $.ajax({
        type: "POST",
        url: var_url,
        data: var_csrf_data,
        dataType: '',
        success: function(data, textStatus, xhr) {
            // show alert
            setTimeout( function() {
                $('#complete_link').hide();
                $('#date_completed').html("Completed:<br> " + data)
            }, 0);
        },
    });
}