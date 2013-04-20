import os
import web

render = web.template.render('templates/', base='layout')
urls = (
    '/(.+)/status',               'test',
    '/(.+)/status/?(\d*)',        'test',
)

class test:
    def GET(self, a, b=None):
        print web.url()
        if not b:
            b='12'
        if a == 'salam':
            return 'persian: %d %s' % (int(b), web.input(a='12').a)
        if a == 'hello':
            return 'english: %d %s' % (int(b), web.input(a='12').a)
        return 'oops: %s %d %s' % (a, int(b), web.input(a='12').a)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
