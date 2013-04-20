import os
import web
import jucs
import secret

db = web.database(dbn='mysql', user='root', pw=secret.pw, db='juxif')

render = web.template.render('templates/', base='layout')

course_render = web.template.render('templates/course/', base='../layout')
#article_render = web.template.render('templates/article/', base='../layout')

algorithm_render = web.template.render('templates/algorithm/', base='../layout')
problem_render = web.template.render('templates/problem/', base='../layout')
contest_render = web.template.render('templates/contest/', base='../layout')

#accounts_render = web.template.render('templates/accounts/', base='../layout')

urls = (
    '/?',                       'home',
#   '/admin',                   'admin',
#   '/news/?',                  'news',
#   '/news/(\d+)',              'news',

    '/course/?',                'course',
    '/course/(.+)',             'course',

#   '/article/?',               'article',
#   '/article/(\d*)',           'article',

    '/algorithm/?',             'algorithm',
    '/algorithm/(\d+)',         'algorithm',
    '/algorithm/status/?',      'status',
    '/algorithm/status/(\d+)',  'status',
    '/algorithm/shoot',         'shoot',

    '/problem/?'   ,            'problem',
    '/problem/(\d+)',           'problem',
    '/problem/status/?',        'status',
    '/problem/status/(\d+)',    'status',
    '/problem/shoot',           'shoot',

    '/contest/?',               'contest',
    '/contest/(\d+)',           'contest',
    '/contest/status/?',        'status',
    '/contest/status/(\d+)',    'status',
#   '/contest/board/(\d+)',     'board',    # http://icpc.sharif.ir/acmicpc12/scoreboard/
    '/contest/shoot',           'shoot',

#   '/accounts/?',              'accounts',
#   '/accounts/register',       'register',
#   '/accounts/logout',         'logout',
#   '/accounts/login',          'login',

#   '/five-oh-oh',              'err500',
    '/four-oh-four',            'err404'

)

class home:
    def GET(self):
        return render.home()

class course:
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return course_render.home(section)

class algorithm:
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return algorithm_render.home(section)

class problem:
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return problem_render.home(section)

class contest:
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return contest_render.home(section)

class status:
    def GET(self, id = None):
        section = web.url().split('/')[1]

        if id is None:
            where = 'true'

        if section == "algorithm":
            if id:
                where = 'subid=%s' % (id)
            query = db.select('shots', what='subid,uid,pid,cid,addr,lang,created', where=where)
            return contest_render.status(query)

        elif section == "problem":
            if id:
                where = 'pid=%s' % (id)
            query = db.select('shots', what='subid,uid,pid,cid,addr,lang,created', where=where)
            return contest_render.status(query)

        elif section == "contest":
            if id:
                where = 'cid=%s' % (id)
            query = db.select('shots', what='subid,uid,pid,cid,addr,lang,created', where=where)
            return contest_render.status(query)

        return render.err404()

class shoot:
    def GET(self):
        return algorithm_render.shoot()

    def POST(self):
        section = web.url().split('/')[1]

        i = web.input(code={})

        uid = int(i.uid) 
        pid = int(i.pid) 
        cid = int(i.cid)

        addr = '%s/source/%s' % (os.getcwd(), i.code.filename)
        code = file(addr, 'w')
        code.write(i.code.value)
        code.close()
    
        lang = i.lang

        subid = db.insert('shots', 
            # subid has AUTO_INCREMENT, 
            uid = uid, 
            pid = pid, 
            cid = cid, 
            addr = addr, 
            lang = lang,
            mode = 0 # mode[i.cid]  #FIXME
            # created is set to CURRENT_TIMESTAMP,
            # access is updated by judge
            # modify is updated by judge)
            )
        jucs.submit(subid, uid, pid, lang, addr)

        raise web.seeother('/algorithm/status/%s' % (subid))

class err404:
    def GET(self):
        return render.err404()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
