"""
Python2.7 code by @faustinoaq
This is a app that use Web.py micro framework
install dependences:
pip install -r requirements.txt
and run with:
python main.py
"""

import web  # Web.py Framework
import time  # Date timestamp
import socket  # Server ip
from hashlib import sha1  # Pass check

from db import db  # Database ORM

# URL's and classes
urls = (
    '/','Index',
    '/user', 'User',
    '/delete', 'Delete',
    '/update', 'Update',
    '/abort', 'Abort',
    '/count', 'Counter',
    '/login', 'Login',
    '/logout', 'Logout',
)

# Web.py variable for app
app = web.application(urls, globals())

# Web.py variable for template folder
# and setting base.html
render = web.template.render('templates', base='base', globals={})

# Admin access key is "123"
Key="40bd001563085fc35165329ea1ff5c5ecbdbbeef"

class Login:
    """
    Login for admin cases
    """
    def GET(self):
        return render.login()

    def POST(self):
        i = web.input().key
        key = unicode(i).encode('UTF-8')
        key = key + "h&g/8"  # key salt
        if sha1(key).hexdigest() == Key:
            web.setcookie('key', Key, 3600)
            web.setcookie('user', 'admin', 3600)
            raise web.seeother('/')
        else:
            raise web.seeother('/login')

class Logout:
    """
    Logout the user
    """
    def GET(self):
        web.setcookie('key', '', 3600)
        web.setcookie('user', '', 3600)
        raise web.seeother('/user')


# Function for check if admin is active
def logged(function):
    def GET(*args, **kwargs):
        # try:
        key = web.cookies().key
        print(key)
        if key == Key:
            print("Admin is verified - OK")
            return function(*args, **kwargs)
        print("Admin is not verified - FAIL")
        raise web.seeother('/login')
    return GET


class Index:
    """
    Index class:
    - Check if username exist
    - Return all data
    - Insert data in database
    """

    def __init__(self):
        try:
            self.user = web.cookies().user
            if not self.user:
                raise web.seeother('/user')
        except:
            raise web.seeother('/user')

    def GET(self):
        data = db.select('data', order="id DESC")
        if data:
            send = []
            for dat in data:
                chat = '<div class="chat">'
                chat += '<span class="info">{0} - '.format(dat.user)
                chat += '{0}</span>'.format(dat.timestamp)
                chat += '<pre><code>{0}</code></pre>'.format(unicode(dat.content).encode('UTF-8'))
                chat += '</div>'
                send.append(chat)
            del send[-1]
            return render.home(self.user, ''.join(send))
        return render.home(self.user, "")

    def POST(self):
        i = web.input()
        data = unicode(i.data).encode('UTF-8')  # Allow No ASCCI characters
        date = time.strftime("%Y-%m-%d %I:%M:%S %p")  # Current timestamp
        db.insert('data', content=i.data, user=self.user, timestamp=date)


class User:
    """
    User class:
    - Render username form
    - Check if username is admin
    - Set username
    """

    def GET(self):
        return render.user()

    def POST(self):
        i = web.input()
        user = unicode(i.user).encode('UTF-8')
        if user == "admin":
            raise web.seeother('/login')
        else:
            web.setcookie('user', user, 3600)
        raise web.seeother('/')


class Delete:
    """
    Delete class:
    - Delete all messages of database
    """

    @logged
    def GET(self):
        db.delete('data', where="id>0")

class Counter:
    """
    Counter class:
    - Get a count of database entries
      This is used for Ajax functions
    """

    def GET(self):
        return db.select('data', what='count(*) as count')[0].count


class Update:
    """
    Update class:
    - Get the last entry
      This is used for update the entries via Ajax
    """

    def GET(self):
        try:
            data = db.select('data', order="id DESC")[0]
        except:
            return ""
        send = []
        chat = '<div class="chat">'
        chat += '<span class="info">{0} - '.format(data.user)
        chat += '{0}</span>'.format(data.timestamp)
        chat += '<pre><code>{0}</code></pre>'.format(unicode(data.content).encode('UTF-8'))
        chat += '</div>'
        send.append(chat)
        return send[0]

# Execute app
if __name__ == '__main__':
    # Get local ip and set the port
    # Run with a light WSGI server
    ip = socket.gethostbyname(socket.gethostname())
    port = 8080
    web.httpserver.runsimple(app.wsgifunc(), (ip, port))
