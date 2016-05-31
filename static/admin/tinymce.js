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
    visualblocks_default_state: true,
    document_base_url : "http://127.0.0.1:5000",
    plugins: [
        "autoresize advlist autolink link  lists charmap  hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code nonbreaking",
        "table contextmenu textcolor paste  textcolor colorpicker textpattern codesample"
    ],
    contextmenu: "link insertlink",
    toolbar1: "styleselect formatselect fontselect fontsizeselect |  searchreplace removeformat visualchars visualblocks code ",
    toolbar2: "bold italic underline strikethrough | bullist numlist | hr blockquote codesample nonbreaking pagebreak charmap | link unlink anchor | forecolor backcolor | outdent indent | alignleft aligncenter alignright alignjustify",
    schema: "html5",
    menubar: false,
    toolbar_items_size: 'small',
    convert_fonts_to_spans : true,
    valid_children : "+a[div], +div[*]",
    extended_valid_elements : "div[*]",
    content_css: [ 'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.6/css/bootstrap.min.css', '/static/admin/rte.css'],
    body_class: "tinymce-editor-body",
    theme: "modern",
    skin: "lightgray",  
    style_formats: [{
        "title": "Typography",
        "items": [{
            "title": "Lead Text",
            "block": "p",
            "classes": "lead"
        }, {
            "title": "Small",
            "inline": "small"
        }, {
            "title": "Highlight",
            "inline": "mark"
        }, {
            "title": "Insert",
            "inline": "ins"
        }, {
            "title": "Abbreviation",
            "inline": "abbr"
        }, {
            "title": "Initialism",
            "inline": "abbr",
            "classes": "initialism"
        }, {
            "title": "Cite",
            "inline": "cite"
        }, {
            "title": "User Input",
            "inline": "kbd"
        }, {
            "title": "Variable",
            "inline": "var"
        }, {
            "title": "Sample Output",
            "inline": "samp"
        }, {
            "title": "Address",
            "format": "address",
            "wrapper": true
        }, {
            "title": "Code Block",
            "format": "pre",
            "wrapper": true
        }]
    }, {
        "title": "Colors",
        "items": [{
            "title": "Muted",
            "inline": "span",
            "classes": "text-muted"
        }, {
            "title": "Primary",
            "inline": "span",
            "classes": "text-primary"
        }, {
            "title": "Success",
            "inline": "span",
            "classes": "text-success"
        }, {
            "title": "Info",
            "inline": "span",
            "classes": "text-info"
        }, {
            "title": "Warning",
            "inline": "span",
            "classes": "text-warning"
        }, {
            "title": "Danger",
            "inline": "span",
            "classes": "text-danger"
        }, {
            "title": "Background Primary",
            "block": "div",
            "classes": "bg-primary",
            "wrapper": true
        }, {
            "title": "Background Success",
            "block": "div",
            "classes": "bg-success",
            "wrapper": true
        }, {
            "title": "Background Info",
            "block": "div",
            "classes": "bg-info",
            "wrapper": true
        }, {
            "title": "Background Warning",
            "block": "div",
            "classes": "bg-warning",
            "wrapper": true
        }, {
            "title": "Background Danger",
            "block": "div",
            "classes": "bg-danger",
            "wrapper": true
        }]
    }, {
        "title": "Utilities",
        "items": [{
            "title": "Caret",
            "block": "div",
            "classes": "caret"
        }, {
            "title": "Pull Left",
            "block": "div",
            "classes": "pull-left"
        }, {
            "title": "Pull Right",
            "block": "div",
            "classes": "pull-right"
        }, {
            "title": "Clearfix",
            "block": "div",
            "classes": "clearfix"
        }, {
            "title": "Center Block",
            "block": "div",
            "classes": "center-block"
        }, {
            "title": "Show",
            "inline": "span",
            "classes": "show"
        }, {
            "title": "Hidden",
            "inline": "span",
            "classes": "hidden"
        }, {
            "title": "Invisible",
            "inline": "span",
            "classes": "invisible"
        }, {
            "title": "Hide Text",
            "inline": "span",
            "classes": "hide-text"
        }]
    }, {
        "title": "Lists",
        "items": [{
            "title": "Unstyled List",
            "selector": "ul,ol",
            "classes": "list-unstyled"
        }, {
            "title": "Inline List",
            "selector": "ul,ol",
            "classes": "list-inline"
        }]
    }, {
        "title": "Buttons",
        "items": [{
            "title": "Default",
            "inline": "a",
            "classes": "btn btn-default"
        }, {
            "title": "Primary",
            "inline": "a",
            "classes": "btn btn-primary"
        }, {
            "title": "Success",
            "inline": "a",
            "classes": "btn btn-success"
        }, {
            "title": "Info",
            "inline": "a",
            "classes": "btn btn-info"
        }, {
            "title": "Warning",
            "inline": "a",
            "classes": "btn btn-warning"
        }, {
            "title": "Danger",
            "inline": "a",
            "classes": "btn btn-danger"
        }, {
            "title": "Link",
            "inline": "a",
            "classes": "btn btn-link"
        }, {
            "title": "Large",
            "selector": "a,button,input",
            "classes": "btn-lg"
        }, {
            "title": "Small",
            "selector": "a,button,input",
            "classes": "btn-sm"
        }, {
            "title": "Extra Small",
            "selector": "a,button,input",
            "classes": "btn-xs"
        }, {
            "title": "Block",
            "selector": "a,button,input",
            "classes": "btn-block"
        }, {
            "title": "Disabled",
            "selector": "a,button,input",
            "attributes": {
                "disabled": "disabled"
            }
        }]
    }, {
        "title": "Labels",
        "items": [{
            "title": "Default",
            "inline": "span",
            "classes": "label label-default"
        }, {
            "title": "Primary",
            "inline": "span",
            "classes": "label label-primary"
        }, {
            "title": "Success",
            "inline": "span",
            "classes": "label label-success"
        }, {
            "title": "Info",
            "inline": "span",
            "classes": "label label-info"
        }, {
            "title": "Warning",
            "inline": "span",
            "classes": "label label-warning"
        }, {
            "title": "Danger",
            "inline": "span",
            "classes": "label label-danger"
        }]
    }, {
        "title": "Alerts",
        "items": [{
            "title": "Default",
            "block": "div",
            "classes": "alert alert-default",
            "wrapper": true
        }, {
            "title": "Primary",
            "block": "div",
            "classes": "alert alert-primary",
            "wrapper": true
        }, {
            "title": "Success",
            "block": "div",
            "classes": "alert alert-success",
            "wrapper": true
        }, {
            "title": "Info",
            "block": "div",
            "classes": "alert alert-info",
            "wrapper": true
        }, {
            "title": "Warning",
            "block": "div",
            "classes": "alert alert-warning",
            "wrapper": true
        }, {
            "title": "Danger",
            "block": "div",
            "classes": "alert alert-danger",
            "wrapper": true
        }]
    }, {
        "title": "Other",
        "items": [{
            "title": "Reverse Blockquote",
            "selector": "blockquote",
            "classes": "blockquote-reverse"
        }, {
            "title": "Centered Blockquote",
            "selector": "blockquote",
            "classes": "text-center"
        }, {
            "title": "Blockquote Footer",
            "block": "footer"
        }, {
            "title": "Well",
            "block": "div",
            "classes": "well",
            "wrapper": true
        }, {
            "title": "Large Well",
            "block": "div",
            "classes": "well well-lg",
            "wrapper": true
        }, {
            "title": "Small Well",
            "block": "div",
            "classes": "well well-sm",
            "wrapper": true
        }, {
            "title": "Badge",
            "inline": "span",
            "classes": "badge"
        }, {
            "title": "Rounded Image",
            "selector": "img",
            "classes": "img-rounded"
        }, {
            "title": "Circle Image",
            "selector": "img",
            "classes": "img-circle"
        }, {
            "title": "Thumbnail Image",
            "selector": "img",
            "classes": "img-thumbnail"
        }]
    }],
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
