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
                $('#date_started').html("Start:<br> " + data);
            }, 0);
        },
    });
}

function trigger_complete_action(item_id){
    var_csrf_data = {"csrfmiddlewaretoken": csrf_token};

    var_url = '/ajax/item_complete_action/' + item_id;

    $.ajax({
        type: "POST",
        url: var_url,
        data: var_csrf_data,
        dataType: '',
        success: function(data, textStatus, xhr) {
            // show alert
            setTimeout( function() {
                $('#complete_link').hide();
                $('#date_completed').html("Completed:<br> " + data);
            }, 0);
        },
    });
}

function trigger_complete_no_action(item_id){
    var_csrf_data = {"csrfmiddlewaretoken": csrf_token};

    var_url = '/ajax/item_complete_no_action/' + item_id;

    $.ajax({
        type: "POST",
        url: var_url,
        data: var_csrf_data,
        dataType: '',
        success: function(data, textStatus, xhr) {
            // show alert
            setTimeout( function() {
                $('#complete_link').hide();
                $('#date_completed').html("Completed:<br> " + data);
            }, 0);
        },
    });
}

function trigger_add_comment(item_id){

    var_url = '/ajax/item_add_comment/' + item_id;

    // comment_text = document.getElementById('comment_text').value;
    comment_text = $('#comment_text').val();
    send_data = {"csrfmiddlewaretoken": csrf_token, 'comment_text': comment_text};

    $.ajax({
        type: "POST",
        url: var_url,
        data: send_data,
        dataType: '',
        success: function(data, textStatus, xhr) {
            // show alert
            setTimeout( function() {
                $('#comment_text').val('');
                $('#comments_panel').html(data)
            }, 0);
        },
    });
}