import web
import time
import secret

from Crypto import Random
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES

urls = (
    '/?',               'accounts',
    '/(\d+)',           'accounts',
    '/register',        'register',
    '/logout',          'logout',
    '/login',           'login'
    )

accounts_app = web.application(
    urls, 
    globals()
    )

db = web.database(
    dbn = 'mysql', 
    user = 'root', 
    pw = secret.pw, 
    db = 'juxif'
    )

if web.config.get('_session') is None: # the fishiest thing ever ... something ain't right here!
    session = web.session.Session(
        accounts_app, 
        web.session.DiskStore('sessions'),
        initializer = {
            'auth': False,
            'time': time.time(),
    
            'uid': None,
            'email': None,
            'uname': None
            }
        )
    web.config._session = session
else:
    session = web.config._session

renderer = web.template.render(
    'templates/accounts/', 
    base = '../layout',
    globals = {
        'session': session,
        }
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
        return renderer.login()
    def POST(self):
        section = web.url().split('/')[1]
        i = web.input(
            identity = None, 
            passwd = None
            )

        identity = i.identity
        passwd = i.passwd

        what = 'uid, email, username, password'
        where = "(email='%s' OR username='%s')" % (identity, identity)

        query = db.select('users', None, 
            what, where)

        row = query[0]

        hash = SHA256.new()
        hash.update(secret.salt)
        hash.update(row.email)
        hash.update(passwd)
        shadow = hash.digest()

        # TODO: implement HTTP Digest Authentication :-fsck yeah! https://github.com/mahrud/webpy_http-digest-auth
        if shadow.encode('hex') == row.password:
#           session.start()
            session.auth = True
            session.time = time.time()
            session.uid  = row.uid
            session.email = row.email
            session.uname = row.username

            return web.seeother("/")
        else:
            return renderer.login(1, identity)

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

        token = i.token
        fname = i.fname
        uname = i.uname
        email = i.email
        passwd = i.passwd

        ctime = time.time()

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

            nonce = str(ctime).encode('hex') # FIXME: should we make it more complex?

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
            content = '<a href="%s">%s</a>' % (token, token)
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
            between ctime and ttime, if it is more than 24 hours, we 
            ignore the token and ask the user to register again.
            """
            ttime = float(nonce.decode('hex'))
            if ctime - ttime > 24 * 60 * 60:
                return renderer.register(1)

            """
            Now we have to store a shadow of the password in db.
            First we set up the hash function:
                hash(P) -> SHA256(P)
            Based on that, we have:
                shadow = SHA256(salt | email | passwd)
            """
            hash = SHA256.new()
            hash.update(secret.salt)
            hash.update(email.decode('hex'))
            hash.update(passwd.decode('hex'))
            shadow = hash.digest()

            uid = db.insert('users',
                gid      = -1, # FIXME
                email    = email.decode('hex'),
                username = uname.decode('hex'),
                realname = fname.decode('hex'),
                password = shadow.encode('hex')
                )

            raise web.seeother('/%d' % (uid))

if __name__ == "__main__":
    accounts_app.run()
