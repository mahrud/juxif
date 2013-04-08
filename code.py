import web

urls = (
  '/(.*)', 'index'
)

class index:
    def GET(self, name):
        return "Hello, world!\nurl=%s" % (name)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
