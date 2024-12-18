# Neptune
Neptune is a simple project that was originally intended as a simple HTTP server based on the TCP protocol with Python sockets, but has evolved into a Django-like framework.

*Note:*  The project is still running on a simple HTTP server! Maybe I will make a new project with a fully integrated HTTP protocol that is up to date.


## Table of Contents
- [Description](#description)
- [Preparation](#preparation)
- [Example View](#example_view)
- [Contact](#contact)

1. Clone this repository:

   ```bash
   git clone https://github.com/phbruemmer/HTTP-Server.git


## Description
This project is a good start for anyone who wants to learn more about how the Internet, or more specifically the protocols on which much of the Internet is based, works.
It includes a simple HTTP server based on the TCP protocol, functions that break HTTP requests into logically meaningful parts and parse them into a hashmap (Python dictionary), 
Functions that create appropriate HTTP responses, and if you are familiar with the Django framework, views, URL routing, database operations (still working on ORM) and apps for more modularity.
## Preparation
- After cloning this repository you can try the following commands, to test if this project is working:
  ```bash
  python manage.py runserver [ip:port]   # to run the server
  python manage.py add app [name]        # to add an app
  python manage.py update statics        # to update the static files

Follow these steps to create your first working view:
- Create an app *'python manage.py add app [name]'*
- go into views.py
- import render from backend
- create a view function with request as parameter
- return *'render.render(request, HTML path, arguments)'*
  - *'render.render()'* returns an HTTP response with all the information needed to display the HTML file.
  - the view returns this value to the HTTP server, which sends the encrypted (not secure) response to the browser via the TCP protocol

## Important
For example, if you are trying to render a specific HTML file, always use the path from the root directory.
(The default content directory is set to the file you are running, usually manage.py in the root directory).


## Example View
    from backend import render

    def main(request):
      args = {
          'var_3': 'Welcome!',
          'info': ''
      }
      return render.render(request, 'HTML_files/index.html', args)
  - Will add more description to this example later.
