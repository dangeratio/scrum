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

function trigger_tab(tab) {

    hide_tabs();

    trigger_ajax_chart(tab);

    select_tab(tab);

}

