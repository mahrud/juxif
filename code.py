import web
import secret

db = web.database(dbn='mysql', user='root', pw=secret.pw, db='test')

render = web.template.render('templates/', base='layout')

urls = (
    '/',                'home',
#    '/contest/(.*)',    'contest',
#    '/problem/(.+)',    'pset',
    '/shoot',           'shoot',
    '/status/(.*)',     'status'
#    '/board/(.*)',      'board', #   http://icpc.sharif.ir/acmicpc12/scoreboard/
)

class home:
    def GET(self):
        return render.home()

class shoot:
    def GET(self):
        return render.shoot()
    def POST(self):
        i = web.input()
        n = db.insert('test', a=int(i.b)*10, b=int(i.b))
        raise web.seeother('/status/%s' % (i.b))

class status:
    def GET(self, subid):
        q = db.select('test', what='a,b', where='b=%s' % (subid))
        return render.status(q[0].a)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
