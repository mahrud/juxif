import web
from web import form

render = web.template.render('templates') # your templates

urls = ('/', 'register')

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
    form.Textbox("username", description="Username", placeholder="slaam"),
    form.Textbox("email", class_="salam", type="password", description="E-Mail"),
    form.Password("password", pattern="\S{5,10}", description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)

class register:
    def GET(self):
        # do $:f.render() in the template
        f = register_form()
        return render.test(f)

    def POST(self):
        f = register_form()
        if not f.validates():
            return render.test(f)
        else:
            print 12
            # do whatever is required for registration

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
