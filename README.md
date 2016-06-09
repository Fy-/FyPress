FyPress (Still in development)
--------
FyPress is a mini CMS in Python based on Flask and Jinja2, aimed to easily deploy content-managed websites through organized articles and pages, using simply HTML.

[![FyPress](https://fy.to//files/2016/6/fakeplayer.png)](https://www.youtube.com/watch?v=5ejW8wblJps)

### Install FyPress
    git clone --recursive https://github.com/Fy-/FyPress.git
    cd FyPress
    pip install -r requirements.txt

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
