$(document).ready(function(){
    $('#fp_slug').slugify('#fp_name');

    $('.sortable').nestedSortable({
        handle: 'div',
        items: 'li',
        maxLevels: 5,
        rootID: 'folder_1',
        isTree: true,
        toleranceElement: '> div',
        excludeRoot: true,
        protectRoot: true,
        placeholder: 'placeholder',
        forcePlaceholderSize: true,
        tabSize: 40,
        opacity: .6,
        relocate: function() {
            arraied = $('ol.sortable').nestedSortable('toArray', {startDepthCount: 0});
            $.post( '{{ url_for('admin.ajax_folders') }}', {'data': JSON.stringify(arraied)} );
        }
    });



    $('[data-toggle="confirmation"]').confirmation({
        onConfirm: function(e){
            e.preventDefault();
            var id = $(this)[0].id;
            $('#folder_'+id).remove();
            arraied = $('ol.sortable').nestedSortable('toArray', {startDepthCount: 0});
            $.post( '{{ url_for('admin.ajax_folders') }}', {'data': JSON.stringify(arraied)} );
        },
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