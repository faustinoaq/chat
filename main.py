import web
import socket

from db import db

urls = (
    '/','Index',
    '/user', 'User',
    '/delete', 'Delete',
    '/update', 'Update',
    '/abort', 'Abort'
)

app = web.application(urls, globals())

render = web.template.render('templates', base='base', globals={})


class Index:

    def __init__(self):
        try:
            self.user = web.cookies().user
            if not self.user:
                raise web.seeother('/user')
        except:
            raise web.seeother('/user')

    def GET(self):
        return render.home(self.user)

    def POST(self):
        i = web.input()
        data = unicode(i.data).encode('UTF-8')
        db.insert('data', content=i.data, user=self.user)

        
class User:

    def GET(self):
        return render.user()
        
    def POST(self):
        i = web.input()
        user = unicode(i.user).encode('UTF-8')
        web.setcookie('user', user, 3600)
        raise web.seeother('/')

        
class Delete:
    
    def GET(self):
        db.delete('data', where="id>0")
        raise web.seeother('/')


class Update:

    def GET(self):
        data = db.select('data')
        if data:
            send = []
            for dat in data:
                chat = '<li><b>{0}:</b> {1} - {2}</li>'.format(dat.user, unicode(dat.content).encode('UTF-8'), dat.timestamp)
                send.append(chat)
            return ''.join(send)
        return ''

class Abort:

    def GET(self):
        app.stop()
        

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    port = 8080
    web.httpserver.runsimple(app.wsgifunc(), (ip, port))
