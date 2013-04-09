import web
import MySQLdb

conn = MySQLdb.connection (host='127.0.0.1', user='hellicode', passwd='', db='hellicode')

render = web.template.render('templates/', base='layout')
urls = (
  '/',                              'home'

#  '/hellicode',                    'dash'

#  '/hellicode/problemset/(.*)',    'pset'
#  '/hellicode/problem/(.*)',       'prob'
#  '/hellicode/contest/(.*)',       'contest'

  '/hellicode/submit',              'submit'

#  '/hellicode/ranking',            'rank'
#  '/hellicode/scoreboard/(.*)',    'board'
  '/hellicode/status/(.*)',         'stat'

#  '/hellicode/admin',              'admin'
#  '/hellicode/login',              'login'
#  '/hellicode/user/(.*)',          'user'
#  '/hellicode/users',              'users'
#  '/hellicode/logout',             'logout'
#  '/hellicode/register',           'register'

#  '/hellicode/news/(.*)',          'news'
)

class home:
    def GET(self):
        return render.home()

class submit:
    def GET(self):
        return "hellow"

class stat:
    def GET(self, content):
        conn.query("SELECT id, username, problem_id, lang, status, time, memory, date FROM `submitions` where `id`=%s" % (content))
        res = conn.store_result()
        return render.home(res.fetch_row())

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

conn.close()
