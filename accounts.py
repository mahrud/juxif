import web
import secret

from Crypto import Random
from Crypto.Util import Counter
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES

db = web.database(dbn = 'mysql', user = 'root', pw = secret.pw, db = 'juxif')

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

class register:
    def GET(self):
        return renderer.register()
    def POST(self):
        section = web.url().split('/')[1]
        i = web.input(
            fname = None, uname = None, 
            email = None, passwd = None, 
            nonce = None
            )

        fname = i.fname
        uname = i.uname
        email = i.email
        passwd = i.passwd
        nonce = i.nonce

        """
        Summary of what is about to happen:
        User to us:
            fullname, username, email, and password
        We to the user:
            AES(SHA256(salt | password), (hex(fullname) : hex(username) : hex(email) : hex(password)))
        Now, if the user successfully returened:
            nonce, password
        We register him!
        """
        if nonce is None:
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
                nonce = AES(key, code)
            """
            hash = SHA256.new()
            hash.update(secret.salt)
            hash.update(passwd)
            key = hash.digest()

            ctr = Counter.new(128)
            cipher = AES.new(key, AES.MODE_CTR, counter = ctr)
            nonce = cipher.encrypt(code)

            """
            Now we set up one more function:
                mac(P) -> HMAC(P)
            Now:
                digest = HMAC(salt | password | nonce)
            """
            mac = HMAC.new(secret.salt)
            mac.update(passwd)
            mac.update(nonce)
            digest = mac.digest()

            """
            What we send back to the user:
                BASE64( nonce : digest)
            """
            return renderer.confirm(nonce.encode('base64') + ':' + digest.encode('base64')) # FIXME: We are supposed to email this!
        else:
            """
            What we get from the user: the nonce, its digest, and password
            Then we set up some cryptographic functions:
                hash(P) -> SHA256(P)
                cipher(K, P) -> AES(K, P)
             Based on those, we have:
                key = SHA256(salt | password)
                nonce = AES(key, code)
            """
            hash = SHA256.new()
            hash.update(secret.salt)
            hash.update(passwd)
            key = hash.digest()

            """
            Now we set up one more function:
                mac(P) -> HMAC(P)
            Now:
                digest = HMAC(salt | password | nonce[0])
            """
            mac = HMAC.new(secret.salt)
            mac.update(passwd)
            mac.update(nonce.split(':')[0].decode('base64'))
            digest = mac.digest()

            """
            To ensure that the nonce is correct, 
            we check it by comparing it to its digest 
            """
            if nonce.split(':')[1].decode('base64') != digest:
                return renderer.confirm(nonce, 1)

            """
            Aaaaan finally we can decrypt the nonce to get our code, 
            and then split that to get the original data:
            """
            ctr = Counter.new(128)
            cipher = AES.new(key, AES.MODE_CTR, counter = ctr)
            code = cipher.decrypt(nonce.split(':')[0].decode('base64'))
            fname, uname, email, passwd = code.split(':')

            uid = db.insert('users',
                gid      = -1, # FIXME
                email    = email.decode('hex'),
                username = uname.decode('hex'),
                realname = fname.decode('hex'),
                password = passwd.decode('hex')
                )

            raise web.seeother('/%d' % (uid))

class logout:
    def GET(self):
        return renderer.logout()

class login:
    def GET(self):
        return renderer.login()

accounts_app = web.application(urls, globals())
if __name__ == "__main__":
    accounts_app.run()
