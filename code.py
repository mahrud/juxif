import os
import web
import secret

db = web.database(dbn='mysql', user='root', pw=secret.pw, db='juxif')

render = web.template.render('templates/', base='layout')

urls = (
    '/',                'home',
#    '/contest/(.*)',    'contest',
#    '/problem/(.+)',    'pset',
    '/shoot',           'shoot',
    '/status/(.*)',     'status'
#    '/board/(.*)',      'board', # http://icpc.sharif.ir/acmicpc12/scoreboard/
)

class home:
    def GET(self):
        return render.home()

class shoot:
    def GET(self):
        return render.shoot()

    def POST(self):
        i = web.input(code={})

        addr = '%s/source/%s' % (os.getcwd(), i.code.filename)
        code = file(addr, 'w')
        code.write(i.code.value)
        code.close()

        subid = db.insert('shots', 
            # subid has AUTO_INCREMENT, 
            uid = int(i.uid), 
            pid = int(i.pid), 
            cid = int(i.cid), 
            addr = addr, 
            lang = i.lang,
            mode = 0 # mode[i.cid]  #FIXME
            # created is set to CURRENT_TIMESTAMP,
            # access is updated by judge
            # modify is updated by judge)
            )

        raise web.seeother('/status/%s' % (subid))

class status:
    def GET(self, subid):
        if subid:
            where = 'subid=%s' % (subid)
        else:
            where = 'true'

        query = db.select('shots', what='subid,uid,pid,cid,addr,lang,created', where=where)
        return render.status(query)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
