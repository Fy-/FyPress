$(document).ready(function(){
    $('[data-toggle="confirmation"]').confirmation({
        'btnOkLabel': 'Yes',
        'btnCancelLabel': 'No',
        'btnOkClass': 'btn-success btn btn-xs ',
        'btnCancelClass': 'btn  btn-danger btn-xs pull-right ',
        'title': '{{_('Are you sure? ')}}',
        'singleton': true,
        'popout': true,
        'content': 'test'
    });
});