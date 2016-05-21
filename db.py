import MySQLdb

def connect():
    return MySQLdb.connect("soheil.mysql.pythonanywhere-services.com" , "soheil" , "akbar123456" , "soheil$users")

def make_users_table():
    con = connect()
    cur = con.cursor()
    #cur.execute('DROP TABLE users')
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY  ,username VARCHAR(255),password VARCHAR(255))')
    con.commit()
    con.close()


def make_posts_table(username):
    con = connect()
    cur = con.cursor()
    #cur.execute('DROP TABLE users')
    #cur.execute('CREATE TABLE IF NOT EXISTS %s(Post_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,Posts VARCHAR(255))',(username+"posts"))
    cur.execute('CREATE TABLE IF NOT EXISTS %s(Post_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,Titles VARCHAR(255),Posts VARCHAR(255) ,Likes INT DEFAULT 0, disLikes INT DEFAULT 0)' % (username + "posts"))
    con.commit()
    con.close()

def make_comments_table(username):
    con = connect()
    cur = con.cursor()
    #cur.execute('DROP TABLE users')
    cur.execute('CREATE TABLE IF NOT EXISTS %s(Comment_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Post_ID INT ,Comments VARCHAR(255),FOREIGN KEY (Post_ID) REFERENCES %s(Post_ID) ON DELETE CASCADE )'%((username+"comments"),(username+"posts")))
    con.commit()
    con.close()

def make_replies_table(username):
    con = connect()
    cur = con.cursor()
    #cur.execute('DROP TABLE users')
    cur.execute('CREATE TABLE IF NOT EXISTS %s(Reply_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,Comment_ID INT ,Replies VARCHAR(255),FOREIGN KEY (Comment_ID) REFERENCES %s(Comment_ID) ON DELETE CASCADE )'%((username+"replies"),(username+"comments")))
    con.commit()
    con.close()
def make_needed_tables(username):
    make_posts_table(username)
    make_comments_table(username)
    make_replies_table(username)

def insert_new_post(username,post_title,post_text):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO %s(Titles,Posts) VALUES('%s','%s')" % ((username+"posts"),post_title,post_text) )
    #cur.execute("INSERT INTO %s(Posts) VALUES(%s)" % ((username+"posts"),post_text) )         it raises error ... but WHY ? WHY inserting username is correct then ?
    con.commit()
    con.close()

def insert_new_comment(username,post_id,comment_text):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO %s(Post_ID , Comments) VALUES(%s,'%s')" % ((username+"comments"),post_id,comment_text) )
    con.commit()
    con.close()

def insert_new_reply(username,comment_id,reply_text):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO %s(Comment_ID , Replies) VALUES(%s,'%s')" % ((username+"replies"),comment_id,reply_text) )
    con.commit()
    con.close()

def insert_user(username , password):
    con = connect()
    cur = con.cursor()
    #cur.execute('INSERT INTO users (username , password) VALUES ("'+username+'","'+password+'")' )
    #cur.execute("INSERT INTO users(username , password) VALUES('sss','ssss')"  )
    cur.execute("SELECT * FROM users WHERE username='%s'" %(username))
    if cur.fetchall():
        #print "username is allready taken"
        con.close()
        return False
    cur.execute("INSERT INTO users(username , password) VALUES(%s,%s)" , (username,password) )
    con.commit()
    con.close()
    return True

def get_posts(username):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM %s " %(username+"posts"))
    result = cur.fetchall()
    con.close()
    return result
def get_comments(username,post_id):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM %s WHERE Post_ID=%s" %((username+"comments"),post_id))
    result = cur.fetchall()
    con.close()
    return result

def get_replies(username,comment_id):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM %s WHERE Comment_ID=%s" %((username+"replies"),comment_id))
    result = cur.fetchall()
    con.close()
    return result

def get_usernames():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    tup = cur.fetchall()
    return [x[1] for x in tup]
def delete_post(username,post_id):
    con = connect()
    cur = con.cursor()
    cur.execute("Delete FROM %s WHERE Post_ID=%s" %((username+"posts"),post_id))
    con.commit()
    con.close()
def edit_post(username,post_id,post_title,post_text):
    con = connect()
    cur = con.cursor()
    cur.execute("UPDATE %s SET Titles='%s',Posts='%s' WHERE Post_ID=%s "%((username+'posts'),post_title,post_text,post_id))
    con.commit()
    con.close()

def validate_user(username,password):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username='%s'" %(username))
    tup = cur.fetchall()
    if tup:
        if tup[0][2]== password :
            return True
    return False
def like(username,post_id,wtd):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM %s WHERE Post_ID=%s" %((username+'posts'),post_id))
    tup = cur.fetchall()
    if wtd == "up":
        likes = int(tup[0][3])+ 1
    elif wtd == "down":
        likes = int(tup[0][3])- 1
    cur.execute("UPDATE %s SET Likes=%s WHERE Post_ID=%s"%((username+'posts'),likes,post_id))
    con.commit()
    con.close()


def dislike(username,post_id,wtd):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM %s WHERE Post_ID=%s" %((username+'posts'),post_id))
    tup = cur.fetchall()
    if wtd == "up":
        likes = int(tup[0][4])+ 1
    elif wtd == "down":
        likes = int(tup[0][4])- 1
    cur.execute("UPDATE %s SET disLikes=%s WHERE Post_ID=%s"%((username+'posts'),likes,post_id))
    con.commit()
    con.close()

def test():
    con = connect()
    cur = con.cursor()
    cur.execute('DROP TABLE soheilreplies')
    con.commit()
    cur.execute('DROP TABLE soheilcomments')
    con.commit()
    cur.execute('DROP TABLE soheilposts')
    con.commit()
    con.close()

#make_users_table()
#make_needed_tables("soheil")
#insert_user("soheila","asghar")
#insert_user("mamad","akbar")
'''
insert_new_post("soheil","he","hi every one")
insert_new_post("soheil","he","good morning")
insert_new_post("soheil","he","how are you")
insert_new_comment("soheil","1","heloooo")
insert_new_comment("soheil","1","helowo")
insert_new_comment("soheil","1","helrroo")
insert_new_comment("soheil","2","good heloooo")

insert_new_reply("soheil","4","shut up ")
insert_new_reply("soheil","4","plz shut your mouth ")
'''

#test()
#print validate_user("mamad","d")