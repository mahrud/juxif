import web
import secret
import hmac
import hashlib
from Crypto.Cipher import XOR

db = web.database(dbn = 'mysql', user = 'root', pw = secret.pw, db = 'juxif')

renderer = web.template.render('templates/accounts/',  base = '../layout')

urls = (
    '/?',  'accounts',
    '/register',    'register',
    '/logout',      'logout',
    '/login',       'login'
    )

class accounts:
    def GET(self):
        return renderer.home('')

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
            XOR(sha1(salt | password), (hex(fullname) : hex(username) : hex(email) : hex(password)))
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
            code += uname.encode('hex') + ':'
            code += email.encode('hex') + ':'
            code += passwd.encode('hex')

            """
            Settin' up some cryptographic functions:
                hash(P) -> sha1(P)
                enc_K(P) -> XOR(P, K)
            And based on those, we have:
                key = sha1(salt | password)
                nonce = XOR(key, code)
            """
            hash = hashlib.sha1()
            hash.update(secret.salt)
            hash.update(passwd)
            key = hash.digest()
            enc = XOR.new(key)
            nonce = enc.encrypt(code)

            """
            Now we set up one more function:
                mac_K(P) -> hmac_K(P)
            Now:
                digest = hmac_K(nonce)
            """
            mac = hmac.new(secret.salt)
            mac.update(passwd)
            mac.update(nonce)
            digest = mac.digest()

            """
            What we send back to the user:
                hex( nonce : digest)
            """
            return renderer.confirm(nonce.encode('hex') + ':' + digest.encode('hex'))
        else:
            """
            What we get from the user: the nonce, its digest, and password
            Then we set up some cryptographic functions:
                hash(P) -> sha1(P)
                enc_K(P) -> XOR(P, K)
             Based on those, we have:
                key = sha1(salt | password)
                nonce = XOR(key, code)
            """
            hash = hashlib.sha1()
            hash.update(secret.salt)
            hash.update(passwd)
            key = hash.digest()
            dec = XOR.new(key)

            """
            Now we set up one more function:
                mac_K(P) -> hmac_K(P)
            Now:
                digest = hmac_K(nonce)
            """
            mac = hmac.new(secret.salt)
            mac.update(passwd)
            mac.update(nonce.split(':')[0].decode('hex'))
            digest = mac.digest()

            """
            To ensure that the nonce is correct, 
            we check it by comparing it to its digest 
            """
            if nonce.split(':')[1].decode('hex') != digest:
                return renderer.confirm(nonce, 1)

            """
            Aaaaan finally we can decrypt the nonce to get our code, 
            and then split that to get the original data:
            """
            code = dec.decrypt(nonce.split(':')[0].decode('hex'))
            fname, uname, email, passwd = code.split(':')

            uid = db.insert('users',
                gid      = -1, # FIXME
                email    = email.decode('hex'),
                username = uname.decode('hex'),
                realname = fname.decode('hex'),
                password = passwd.decode('hex')
                )

            raise web.seeother('/accounts/%d' % (uid))

class logout:
    def GET(self):
        return renderer.logout()

class login:
    def GET(self):
        return renderer.login()

accounts_app = web.application(urls, globals())
if __name__ == "__main__":
    accounts_app.run()
