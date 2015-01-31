"""
    Open Chat by @faustinoaq
    This app use Web.py micro web framework
    and SQLAlchemy ORM
"""

import web   # Web.py framework
import json  # Used for generate JSON documents
import time  # Used for generate timestamps
from db import db  # Get the database queries
from random import randrange  # Used for generate random numbers

web.config.debug = False

# Routes and classes
urls = (
    '/', 'Index',
    '/data/(.*)', 'Data',
    '/exit', 'Exit',
    '/reset', 'Reset'
)

app = web.application(urls, globals())

render = web.template.render('templates', base='base', globals={})
make = web.template.render('templates', globals={})


class Index:

    def __init__(self):
        self.maxUsers = 10  # LIMITED TO 30 USERS/COLORS
        clients = db.select('user', what='count(*) as count')[0]
        if clients.count >= self.maxUsers:
            raise web.seeother('/data/warning')
        try:
            cookie = web.cookies()
            if cookie.user == '' and cookie.color == '':
                Color = self.color()
                User = self.name()
                web.setcookie('color', Color, 604800)
                web.setcookie('user', User, 604800)
                timestamp = time.strftime("%Y-%m-%d %I:%M:%S %p")
                db.insert('user', user=User,
                                  color=Color,
                                  timestamp=timestamp)
            else:
                data = db.select('user', where='user="{0}"'.format(cookie.user))
                if not data:
                    x
        except BaseException as ex:
            print ex
            web.setcookie('user', '', 3600)
            web.setcookie('color', '', 3600)
            raise web.seeother('/')

    def color(self):
        stepRange = 50 # Max color = 255/stepRange * 6
        r = randrange(start=100, stop=255, step=stepRange)
        b = randrange(100, 255, stepRange)
        g = randrange(100, 255, stepRange)
        rgb = [
            [255, 0, b],
            [0, g, 255],
            [r, 0, 255],
            [r, 255, 0],
            [0, 255, b],
            [255, g, 0],
        ]
        existColor = True
        while existColor:
            rgb = rgb[randrange(0, 6, 1)]
            color = "rgb({0}, {1}, {2})".format(rgb[0], rgb[1], rgb[2])
            data = db.select('user', where='color="{0}"'.format(color))
            if data:
                existColor = True
            else:
                existColor = False
        return color

    def name(self):
        existUser = True
        while existUser:
            user = 'User' + str(randrange(1, self.maxUsers*5, 1))
            data = db.select('user', where='user="{0}"'.format(user))
            if data:
                existUser = True
            else:
                existUser = False
        return user

    def GET(self):
        cookie = web.cookies()
        if cookie.user and cookie.color:
            return render.home(cookie.user, cookie.color)
        raise web.seeother('/')

    def POST(self):
        i = web.input()
        cookie = web.cookies()
        timestamp = time.strftime("%Y-%m-%d %I:%M:%S %p")
        db.insert('data', timestamp=timestamp,
                          content=i.content,
                          user=cookie.user)

class Data:


    def hackIter(self, Iterbetter):
        list = []
        for Iter in Iterbetter:
            list.append(Iter)
        return list

    def GET(self, data):
        if data == "report":
            clients = db.select('user', what='count(*) as count')[0]
            messages = db.select('data', what='count(*) as count')[0]
            report = {'clients': clients.count, 'messages': messages.count}
            return "report = {0}".format(json.dumps(report, indent=4))
        if data == "users":
            users = self.hackIter(db.select('user'))
            return "users = {0}".format(json.dumps(users, indent=4))
        elif data == "last-message":
            data = self.hackIter(db.select('data', order="id DESC", limit=1))
            clients = self.hackIter(db.select('user'))
            return make.message(data, clients)
        elif data == "recent-messages":
            data = self.hackIter(db.select('data', order="id DESC", limit=100))
            clients = self.hackIter(db.select('user'))
            return make.message(data, clients)
        elif data == "all-messages":
            data = self.hackIter(db.select('data', order="id DESC"))
            clients = self.hackIter(db.select('user'))
            return make.message(data, clients)
        elif data == "warning":
            return render.warning()


class Exit:

    def GET(self):
        cookie = web.cookies()
        web.setcookie('user', '', 3600)
        web.setcookie('color', '', 3600)
        db.delete('user', where='user="{0}"'.format(cookie.user))
        db.delete('data', where='user="{0}"'.format(cookie.user))
        return render.bye()


class Reset:

    def GET(self):
        db.delete('user', where="id>0")
        db.delete('data', where="id>0")
        web.setcookie('user', '', 3600)
        web.setcookie('color', '', 3600)
        return render.bye()

if __name__ == '__main__':
    app.run()
