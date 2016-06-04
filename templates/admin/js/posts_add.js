$(document).on('focusin', function(e) {
  if ($(e.target).closest(".mce-window").length) {
    e.stopImmediatePropagation();
  }
});
$(document).ready(function() {
    $('#fp_media_frame').height( $(window).height() - 170 );
    $('#fp_media_frame').css('display', 'none');
    $('#fp_slug').slugify('#fp_title');
});

var selected = null;
var selected_data = null;
var selected_id = 0;

$('#fp_media_frame').on('load', function(){
    $('#fp_media_frame').css('display', 'block')
    $('#fp_insert_btn').empty();
    $('#fp_media_selected').html('{{_('No media selected')}}');
    $('#fp_media_loader').empty();


    var $iframe = $(this).contents()
    
    $iframe.find('.nav a').click(function() {
        $iframe.find('.medias-box').html('<div style="text-align: center"><i class="fa fa-spinner spin-it fat-icon"></i></div>');
    });
    $iframe.find('nav a').click(function() {
        $iframe.find('.medias-box').html('<div style="text-align: center"><i class="fa fa-spinner spin-it fat-icon"></i></div>');
    });
    
    $iframe.find('.fp_media').click(function() {
        $('#fp_media_selected').empty();
        selected = null;
        $iframe.find('.fp_media').removeClass('media-selected');
        $(this).addClass('media-selected');
        var c_media = $(this).clone()
        selected_id = $(this).attr('id').replace('media_', '');
        $.get( '{{url_for('admin.ajax_get_media')}}?id='+$(this).attr('id'), function(data) {
            var html = '<pre>'+data.data.name+'</pre>'
            selected_data = data.data;
            if (data.data.var) {
                html += '<div class="form-group"><label for="fp_media_format">{{ _('Image size') }}</label><select class="form-control" id="fp_media_format">'
                html += '<option value="'+data.data.guid+'">Original file</option>'

                Object.keys(data.data.var).forEach(function(key) {
                    html += '<option value="'+data.data.var[key].guid+'">'+data.data.var[key].name+'</option>'
                });
                html += '</select></div>'

                selected = '<img class="img-thumbnail" src="{{flask_config['UPLOAD_DIRECTORY_URL']}}'+data.data.guid+'" alt="'+data.data.name+'" />'
            } else {
                selected = '<div class="media">'+data.data.html+'</div>'
            }
            $('#fp_media_selected').append(c_media)
            $('#fp_media_selected').append(html)

            $('#fp_media_format').change(function() {
                selected = '<img class="img-thumbnail" src="{{flask_config['UPLOAD_DIRECTORY_URL']}}'+$('#fp_media_format').val()+'" alt="'+data.data.name+'" />'
            });
        });
        console.log($(this).data('type'))
        if ( $(this).data('type') == 'image') {
            $('#fp_insert_btn').html('<a  href="javascript:insert_featured()" class="btn btn-success">{{_('Post Featured')}}</a> <a  href="javascript:insert_content()" class="btn btn-primary pull-right ">{{_('Insert')}}</a>');
        } else {
            $('#fp_insert_btn').html('<a  href="javascript:insert_content()" class="pull-right btn btn-primary">{{_('Insert')}}</a>');
        }
    });
});
var insert_featured = function() {
    $('#post_featured').attr('src', '{{flask_config['UPLOAD_DIRECTORY_URL']}}'+selected_data.var['thumbnail-lg'].guid)
    $('#post_image').val(selected_id)
    $('#fp_medias_modal').modal('hide')
};
var delete_cover = function() {
    $('#post_featured').attr('src', '/static/admin/images/empty-lg.png');
    $('#post_image').val(0);
}
var insert_content = function() {
    tinymce.get('tinymce').insertContent(selected);
    $('#fp_medias_modal').modal('hide')
};
$('#fp_medias_modal').on('shown.bs.modal', function (e) {
    if ($('#fp_media_frame').attr('src') == '') {
        $('#fp_media_loader').append('<i class="fa fa-spinner spin-it "></i>')
        $('#fp_media_frame').attr('src', '{{ url_for('admin.medias', parent=1)}}');    
        console.log('test');
    }
});
