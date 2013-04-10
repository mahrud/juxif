import web
import secret

db = web.database(dbn='mysql', user='root', pw=secret.pw, db='test')

render = web.template.render('templates/', base='layout')

urls = (
    '/',                    'home',

#    '/problemset/(.*)',    'pset',
#    '/problem/(.*)',       'prob',
#    '/contest/(.*)',       'contest',

    '/submit',              'submit',

#    '/ranking',            'rank',
#    '/scoreboard/(.*)',    'board',  #   http://icpc.sharif.ir/acmicpc12/scoreboard/
    '/status/(.+)',         'status'

#    '/admin',              'admin',
#    '/login',              'login',
#    '/user/(.*)',          'user',
#    '/users',              'users',
#    '/logout',             'logout',
#    '/register',           'register',

#    '/news/(.*)',          'news',
)

class home:
    def GET(self):
        return render.home()

class submit:
    def GET(self):
        return render.submit()

class status:
    def GET(self, subid):
        q = db.select('test', what='a,b', where='b=%s' % (subid))
        return render.status(q[0].a)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
