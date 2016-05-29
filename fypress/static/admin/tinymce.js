tinymce.init({
    selector: '#fp_content',
    autoresize_min_height: 350,
    relative_urls: false,
    remove_script_host: false,
    convert_urls: false,
    browser_spellcheck: true,
    fix_list_elements: true,
    entity_encoding: "raw",
    keep_styles: false,
    end_container_on_empty_block: true,
    document_base_url : "/",
    setup: function(editor) {
        editor.addButton('fpmedias', {
            text: 'Media',
            icon: 'icon-media',
            onclick: function() {
                editor.insertContent('[media]');
            }
        });
    },

    plugins: [
        "autoresize advlist autolink link image lists charmap  hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime nonbreaking",
        "table contextmenu directionality emoticons template textcolor paste fullpage textcolor colorpicker textpattern media imagetools"
    ],
    contextmenu: "link insertlink inserttable | cell row column deletetable",
    toolbar1: "styleselect formatselect fontselect fontsizeselect |  searchreplace | table | hr removeformat | charmap emoticons | visualchars visualblocks nonbreaking pagebreak | code",
    toolbar2: "bold italic underline strikethrough | bullist numlist | outdent indent blockquote | link unlink anchor | forecolor backcolor | alignleft aligncenter alignright alignjustify",
    schema: "html5",
    menubar: false,
    toolbar_items_size: 'small',
    formats: {
        alignleft: [{
            selector: "p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li",
            styles: {
                textAlign: "left"
            }
        }, {
            selector: "img,table,dl.wp-caption",
            classes: "alignleft"
        }],
        aligncenter: [{
            selector: "p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li",
            styles: {
                textAlign: "center"
            }
        }, {
            selector: "img,table,dl.wp-caption",
            classes: "aligncenter"
        }],
        alignright: [{
            selector: "p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li",
            styles: {
                textAlign: "right"
            }
        }, {
            selector: "img,table,dl.wp-caption",
            classes: "alignright"
        }],
        strikethrough: {
            inline: "del"
        }
    },
    images_upload_handler: function(blobInfo, success, failure) {
        var xhr, formData;

        xhr = new XMLHttpRequest();
        xhr.withCredentials = false;
        xhr.open('POST', 'postAcceptor.php');

        xhr.onload = function() {
            var json;

            if (xhr.status != 200) {
                failure('HTTP Error: ' + xhr.status);
                return;
            }

            json = JSON.parse(xhr.responseText);

            if (!json || typeof json.location != 'string') {
                failure('Invalid JSON: ' + xhr.responseText);
                return;
            }

            success(json.location);
        };

        formData = new FormData();
        formData.append('file', blobInfo.blob(), blobInfo.filename());

        xhr.send(formData);
    },
    content_css: [ 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.6/css/bootstrap.min.css' ]
});