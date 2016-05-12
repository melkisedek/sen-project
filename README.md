

# sen_project

sen_project is a small library system . It is built with [Python][0] using the [Django Web Framework][1].

This project has the following basic apps:

* App1 (short desc)
* App2 (short desc)
* App3 (short desc)

## Installation
#### Cloning behind a proxy

To clone this repo from behind a proxy. You need to set the proxy on git. 
For example, if you are a NUST student on nust-staff wifi, run:

`$ git config --global http.proxy http://proxy.nust.na:3128`
you can run: `git config --get http.proxy` to view the set proxy. Then run:

`$ git clone http://github.com/melkisedek/sen_project.git` to clone it.
And optionally run 

`$ git config --global --unset http.proxy` to unset the proxy when you are not behind a proxy.

### Quick start

To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python3 -m venv sen_project`
    2. `$ . sen_project/bin/activate`

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

### Detailed instructions

Take a look at the docs for more information.

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
