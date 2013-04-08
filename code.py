import web

render = web.template.render('templates/')
urls = (
  '/',                     'homepage'

#  '/hellicode',            'hc_home'
#  '/hellicode/dashboard',  'hc_dash'

#  '/hellicode/problemset', 'hc_pset'
#  '/hellicode/problem',    'hc_prob'
#  '/hellicode/contest',    'hc_contest'

#  '/hellicode/submit',     'hc_submit'

#  '/hellicode/ranking',    'hc_rank'
#  '/hellicode/scoreboard', 'hc_board'
#  '/hellicode/status',     'hc_stat'

#  '/hellicode/admin',      'hc_admin'
#  '/hellicode/login',      'hc_login'
#  '/hellicode/user',       'hc_user'
#  '/hellicode/users',      'hc_users'
#  '/hellicode/logout',     'hc_logout'
#  '/hellicode/register',   'hc_register'

#  '/hellicode/news',       'hc_news'
)

class homepage:
    def GET(self):
        return render.index()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
