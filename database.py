import web

db = web.database(dbn = 'sqlite', db = 'sqlite.db')

db.query("""
CREATE TABLE sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text);""")

db.query("""
CREATE TABLE `users` (
    `uid` INTEGER NOT NULL PRIMARY KEY,
    `gid` INTEGER NOT NULL,
    `email` char(128) NOT NULL,
    `username` char(32) NOT NULL,
    `realname` char(32) NOT NULL,
    `password` char(128) NOT NULL,
    `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `access` datetime NOT NULL);
""")


