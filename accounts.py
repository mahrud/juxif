import web
import time
import secret

from Crypto import Random
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES

db = web.database(dbn = 'mysql', user = 'root', pw = secret.pw, db = 'juxif')
session = web.session.Session(accounts_app, web.session.DiskStore('sessions'))

renderer = web.template.render('templates/accounts/',  base = '../layout')

urls = (
    '/?',               'accounts',
    '/(\d+)',           'accounts',
    '/register',        'register',
    '/logout',          'logout',
    '/login',           'login'
    )

class accounts:
    def GET(self, uid = None):
        i = web.input(page = 1)

        page = int(i.page)

        what = 'uid, gid, realname, username, email, created'
        where = str((uid == None) or ('uid = %s' % (str(uid))))

        limit = 19  # Perfect size for my beloved X61 Thinkpad screen!
        offset = (page - 1) * limit

        query = db.select('users', None, 
            what, where, 
            None, None,
            limit, offset)

        return renderer.home(query)

class login:
    def GET(self):
        i = web.input()

        if i.login is None:
            renderer.login()

        email = i.email
        uname = i.uname
        passwd = i.passwd

        what = 'uid, email, uname, passwd'
        where = 'email = %s OR uname = %s' % (email, uname)

        query = db.select('users', None, 
            what, where)

        hash = SHA256.new()
        hash.update(secret.salt)
        hash.update(query.email)
        hash.update(passwd)
        passwd = hash.digest()

        # TODO: implement HTTP Digest Authentication :-fsck yeah! https://github.com/mahrud/webpy_http-digest-auth
        if passwd == query.passwd:
            session.start()
            session.auth = True
            session.time = time.time()

            session.uid = query.uid
            session.email = query.email
            session.uname = query.uname

            return web.seeother("/")
        else:
            return renderer.login(1)

class logout:
    def GET(self):
        session.kill()
        return renderer.logout("Bye!")

class register:
    def GET(self):
        return renderer.register()
    def POST(self):
        section = web.url().split('/')[1]
        i = web.input(
            fname = None, uname = None, 
            email = None, passwd = None, 
            token = None
            )

        fname = i.fname
        uname = i.uname
        email = i.email
        passwd = i.passwd
        token = i.token

        time = time.time()

        """
        Summary of what is about to happen:
        User to us:
            fullname, username, email, and password
        We to the user:
            AES(SHA256(salt | password), (hex(fullname) : hex(username) : hex(email) : hex(password) : hex(nonce)))
        Now, if the user successfully returened:
            token, password
        And the time of token was less than 24 hours ago, we register him!
        """
        if token is None:
            """
            What we get from the user: fullname, username, email, and password
            Then:
                code = hex(fullname) : hex(username) : hex(email) : hex(password)
            """
            code = fname.encode('hex') + ':'
            code += uname.encode('hex') + ':' # FIXME
            code += email.encode('hex') + ':'
            code += passwd.encode('hex')

            """
            Settin' up some cryptographic functions:
                hash(P) -> SHA256(P)
                cipher(K, P) -> AES(K, P)
            And based on those, we have:
                key = SHA256(salt | password)
                token = AES(key, code)
            """
            hash = SHA256.new()
            hash.update(secret.salt)
            hash.update(passwd)
            key = hash.digest()

            nonce = str(time).encode('hex') # FIXME: should we make it more complex?

            ctr = Counter.new(128)
            cipher = AES.new(key, AES.MODE_CTR, counter = ctr)
            token = cipher.encrypt(code + ':' + nonce)

            """
            Now we set up one more function:
                mac(P) -> HMAC(P)
            Now:
                digest = HMAC(salt | password | token)
            """
            mac = HMAC.new(secret.salt)
            mac.update(passwd)
            mac.update(token)
            digest = mac.digest()

            """
            What we email to the user:
                BASE64( token : digest)
            """
            token = token.encode('base64') + ':' + digest.encode('base64')

            # FIXME: create general email templates
            subject = ''
            content = '<a href="%s">%s</a>' % (confirm, confirm)
            # FIXME: We are supposed to email this!

            return renderer.confirm(token)
        else:
            """
            What we get from the user: the token, its digest, and password
            Then we set up some cryptographic functions:
                hash(P) -> SHA256(P)
                cipher(K, P) -> AES(K, P)
             Based on those, we have:
                key = SHA256(salt | password)
                token = AES(key, code)
            """
            hash = SHA256.new()
            hash.update(secret.salt)
            hash.update(passwd)
            key = hash.digest()

            """
            Now we set up one more function:
                mac(P) -> HMAC(P)
            Now:
                digest = HMAC(salt | password | token[0])
            """
            mac = HMAC.new(secret.salt)
            mac.update(passwd)
            mac.update(token.split(':')[0].decode('base64'))
            digest = mac.digest()

            """
            To ensure that the token is correct, 
            we check it by comparing it to its digest 
            """
            if token.split(':')[1].decode('base64') != digest:
                return renderer.confirm(token, 1)

            """
            Aaaaand finally we can decrypt the token to get our code, 
            and then split that to get the original data:
            """
            ctr = Counter.new(128)
            cipher = AES.new(key, AES.MODE_CTR, counter = ctr)
            code = cipher.decrypt(token.split(':')[0].decode('base64'))
            fname, uname, email, passwd, nonce = code.split(':')

            """
            To ensure that the token is current, we find difference 
            between time and ttime, if it is more than 24 hours, we 
            ignore the token and ask the user to register again.
            """
            ttime = float(nonce.decode('hex'))
            if time - ttime > 24 * 60 * 60:
                return renderer.register(1)

            uid = db.insert('users',
                gid      = -1, # FIXME
                email    = email.decode('hex'),
                username = uname.decode('hex'),
                realname = fname.decode('hex'),
                password = passwd.decode('hex')
                )

            raise web.seeother('/%d' % (uid))

accounts_app = web.application(urls, globals())
if __name__ == "__main__":
    accounts_app.run()
