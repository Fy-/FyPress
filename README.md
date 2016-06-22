FyPress (Still in development)
--------
[![irc #fy](https://img.shields.io/badge/IRC-fy-green.svg)](http://webchat.freenode.net/?channels=%23fy)

FyPress is a mini CMS in Python based on Flask and Jinja2, aimed to easily deploy content-managed websites through organized articles and pages, using simply HTML.

[![FyPress](https://raw.githubusercontent.com/Fy-/FyPress/91858685ca95d5a884d6735a67e9aad343bfde8b/static/admin/images/fakeplayer.png)](https://www.youtube.com/watch?v=5ejW8wblJps)

### Install FyPress
    git clone --recursive https://github.com/Fy-/FyPress.git
    cd FyPress
    pip install -r requirements.txt

Edit your configuration file (config.py)

    python manager.py init_db
    python manager.py init_fypress --login=yourLogin --email=your@email.tld --passwd=yourPassword

    python run.py

Build your website http://127.0.0.1:5000 & http://127.0.0.1:5000/admin/

## License
This project is licensed under the [MIT license](http://opensource.org/licenses/MIT), see `LICENSE` for more details.
