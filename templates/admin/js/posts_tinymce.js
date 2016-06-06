tinymce.init({
    selector: '#tinymce',
    autoresize_min_height: 350,
    relative_urls: true,
    remove_script_host: false,
    convert_urls: false,
    browser_spellcheck: true,
    fix_list_elements: true,
    entity_encoding: "raw",
    keep_styles: false,
    end_container_on_empty_block: true,
    forced_root_block: '',
    force_p_newlines: true,
    visualblocks_default_state: true,
    document_base_url : "http://127.0.0.1:5000",
    plugins: [
        "autoresize advlist autolink link  lists charmap  hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code nonbreaking",
        "table contextmenu textcolor paste  textcolor colorpicker textpattern codesample"
    ],
    contextmenu: "link insertlink",
    toolbar1: " formatselect fontselect fontsizeselect |  searchreplace removeformat visualchars visualblocks code ",
    toolbar2: "bold italic underline strikethrough | bullist numlist | hr blockquote codesample nonbreaking pagebreak charmap | link unlink anchor | forecolor backcolor | outdent indent | alignleft aligncenter alignright alignjustify",
    schema: "html5",
    menubar: false,
    toolbar_items_size: 'small',
    convert_fonts_to_spans : true,
    valid_children : "+a[div], +div[*]",
    extended_valid_elements : "div[*]",
    content_css: [ 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.6/css/bootstrap.min.css', '/static/admin/css/rte.css'],
    body_class: "tinymce-editor-body",
    theme: "modern",
    skin: "lightgray",  
  
    formats: {
        alignleft: [{
            selector: "p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li",
            styles: {
                textAlign: "left"
            }
        }, {
            selector: "img,table,media,iframe",
            classes: "pull-left"
        }],
        aligncenter: [{
            selector: "p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li",
            styles: {
                textAlign: "center"
            }
        }, {
            selector: "img,table,media,iframe",
            classes: "centered"
        }],
        alignright: [{
            selector: "p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li",
            styles: {
                textAlign: "right"
            }
        }, {
            selector: "img,table,media,iframe",
            classes: "pull-right"
        }],
        strikethrough: {
            inline: "del"
        }
    }
});
