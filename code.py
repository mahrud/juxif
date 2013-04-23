import os
import web
import jucs
import shutil

import config
import secret

import accounts
#import course
#import problem
#import contest
#import algorithm

db = web.database(dbn = 'mysql', user = 'root', pw = secret.pw, db = 'juxif')

renderer = {
    'kernel':   web.template.render('templates/',           base = 'layout'),
    'course':   web.template.render('templates/course/',    base = '../layout'),
   #'article':  web.template.render('templates/article/',   base = '../layout'),
    'problem':  web.template.render('templates/problem/',   base = '../layout'),
    'contest':  web.template.render('templates/contest/',   base = '../layout'),
    'accounts': web.template.render('templates/accounts/',  base = '../layout'),
    'algorithm': web.template.render('templates/algorithm/', base = '../layout')
    }

urls = (
    '/?',                       'home',
#   '/admin',                   accounts.accounts_app,

    '/accounts/status/(\d+)',   'status',
    '/accounts',                accounts.accounts_app,

    '/news/?',                  'news',
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
    '/contest/shoot',           'shoot',
#   '/contest/board/(\d+)',     'board',
#   http://icpc.sharif.ir/acmicpc12/scoreboard/

#   '/five-oh-oh',              'err500',
    '/four-oh-four',            'err404'
    )

class home:
    """
    Description for home? Seriously?
    """
    def GET(self):
        return renderer['kernel'].home()

class news:
    """
    For now, shows the RSS feed of out git repo.
    """
    def GET(self):
        return renderer['kernel'].news()

class course:
    """
    A Data Structure and Algorithm Design course similar to:
    http://cerberus.delos.com:790/usacogate
    """
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return renderer[section].home(section)

class algorithm:
    """
    A Data Structure and Algorithm database/wiki similar to:
    http://www.cs.sunysb.edu/~algorith/
    Plus an efficient implementation competition.
    """
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return renderer[section].home(section)

class problem:
    """
    Collection of theory/programming problems with references to 
    related algorithms and courses.
    """
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return renderer[section].home(section)

class contest:
    """
    A Programming Competition website similar to many!
    """
    def GET(self, id = None):
        section = web.url().split('/')[1]
        return renderer[section].home(section)

class status:
    """
    Shows the status of one or more shots (submissions)
    """
    def GET(self, id = None):
        section = web.url().split('/')[1]
        i = web.input(page = 1)

        order = {'algorithm': 'subid DESC',
                 'problem': 'pid', 
                 'contest': 'cid DESC',
                 'accounts': 'uid'
                 }  # FIXME
        group = {'algorithm': 'subid',
                 'problem': 'pid', 
                 'contest': 'cid',
                 'accounts': 'uid'
                 }  # FIXME

        what = 'subid, uid, pid, addr, lang, created, stat, time, mmem'
        where = str((id == None) or ('%s = %s' % (group[section], str(id))))

        page = int(i.page)
        limit = 19  # Perfect size for my beloved X61 Thinkpad screen!
        offset = (page - 1) * limit

        query = db.select('shots', None, 
            what, where, 
            'subid DESC', None, #order[section], group[section], FIXME
            limit, offset)

        return renderer[section].status(query)

class shoot:
    """
    A place to shoot (submit) codes to the judge
    """
    def GET(self):
        section = web.url().split('/')[1]
        return renderer[section].shoot()

    def POST(self):
        section = web.url().split('/')[1]
        i = web.input(code={})

        uid = int(i.uid)
        pid = int(i.pid)
        cid = int(i.cid)
        orig = '%s/sources/%s' % (os.getcwd(), i.code.filename)
        code = file(orig, 'w')
        code.write(i.code.value)
        code.close()
        lang = i.lang

        subid = db.insert('shots', 
            # subid has AUTO_INCREMENT, 
            uid = uid, 
            pid = pid, 
            cid = cid, 
            addr = orig, 
            lang = lang,
            mode = 0 # mode[i.cid]  #FIXME
            # created is set to CURRENT_TIMESTAMP,
            # TODO: update `access` by judge
            # TODO: update `modify` by judge
            )

        addr = '%s/sources/%d-%s' % (os.getcwd(), subid, i.code.filename)
        shutil.move(orig, addr)

        db.update('shots', 
            where = "subid=%d" % subid, 
            addr = addr
            )

        jucs.submit(subid, uid, pid, lang, addr)
        raise web.seeother('/algorithm/status/%s' % (subid))

class err404:
    """
    Sorry, description not found!!
    """
    def GET(self):
        return renderer['kernel'].err404()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
