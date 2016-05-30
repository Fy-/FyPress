tinymce.init({
    selector: '#fp_content',
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
    image_caption: true,
    visualblocks_default_state: true,
    document_base_url : "http://127.0.0.1:5000",
    plugins: [
        "autoresize advlist autolink link image lists charmap  hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime nonbreaking",
        "table contextmenu directionality emoticons textcolor paste fullpage textcolor colorpicker textpattern media"
    ],
    contextmenu: "imageinsert | media image | link insertlink inserttable | cell row column deletetable",
    toolbar1: "image styleselect formatselect fontselect fontsizeselect |  searchreplace | table | hr removeformat | charmap emoticons | visualchars visualblocks nonbreaking pagebreak | code",
    toolbar2: "bold italic underline strikethrough | bullist numlist | outdent indent blockquote | link unlink anchor | forecolor backcolor | alignleft aligncenter alignright alignjustify",
    schema: "html5",
    menubar: false,
    toolbar_items_size: 'small',
    convert_fonts_to_spans : true,
    valid_children : "+a[div], +div[*]"
    extended_valid_elements : "div[*]",
    content_css: [ '/static/admin/rte.css', 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.6/css/bootstrap.min.css' ]
});