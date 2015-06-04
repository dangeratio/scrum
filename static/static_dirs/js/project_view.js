function hide_tabs() {
    $('.active').removeClass('active');
}

function select_tab(tab) {
    selector = "#" + tab;
    $(selector).addClass('active');
}

function trigger_ajax_chart(tab) {

    // alert('asdf');

    switch (tab) {
        case 'ic':
            chart_id = 'item_completion';
            break;

        case 'bd':
            chart_id = 'burndown';
            break;

        case '...':
            chart_id = '...';
            break;
    }

    var_csrf_data = { "csrfmiddlewaretoken" : csrf_token };

    var_url = '/ajax/get_chart/' + project_id + '/' + chart_id;

    $.ajax({
        type: "POST",
        url: var_url,
        data: var_csrf_data,
        dataType: '',
        success: function(data, textStatus, xhr) {
            // show alert
            setTimeout( function() {
                $('#chart').html(data);
            }, 0);
        },
    });
}

function hide_all_charts() {
    $('#item_completion_chart_container').hide();
    $('#burndown_chart_container').hide();
}

function trigger_chart_display(tab) {

    // alert('asdf');

    switch (tab) {
        case 'ic':
            $('#item_completion_chart_container').show();
            break;

        case 'bd':
            $('#burndown_chart_container').show();
            break;

        case '...':
            chart_id = '...';
            break;
    }
}

function trigger_tab(tab) {

    hide_tabs();
    hide_all_charts();

    // trigger_ajax_chart(tab);

    trigger_chart_display(tab);

    select_tab(tab);

}
