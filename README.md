FyPress (Still in development)
--------
FlaskPress is a mini CMS based on Flask and Jinja2, aimed to easily deploy content-managed websites through organized articles and pages, using simply HTML.

### Install FyPress
    git clone --recursive https://github.com/Fy-/FyPress.git

Edit your configuration file (config.py)

    python manager.py init_db
    python manager.py init_fypress --login=yourLogin --email=your@email.tld --passwd=yourPassword

    python run.py

Build your website http://127.0.0.1:5000 & http://127.0.0.1:5000/admin/

### Dev 
* Comments
* Medias (Delete/Update)
* Improved template system
* Plugins
