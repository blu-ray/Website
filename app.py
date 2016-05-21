from flask import *
from db import *
from captcha import make_captcha
import random
import time

app = Flask(__name__)
app.secret_key = 'problemscomplicated'


last_checked_user = [""]
liked_or_dis = []
last_captcha = [-1,-1,-1]

def get_captcha():
    x=[0,0,0]
    for i in range(3):
        rand = random.randint(1,36)
        if rand<11 :
            x[i] = chr(rand+47)
        else:
            x[i] = chr(rand+86)
    make_captcha(x[0],x[1],x[2])
    last_captcha[0] = x[0]
    last_captcha[1] = x[1]
    last_captcha[2] = x[2]

@app.route('/')
def index():
    if 'guest' not in session:
        session['guest'] = 'myg'
    return render_template("index.html")

@app.route('/comments/<postid>' , methods=['POST','GET'])
def comment_view(postid):
    if request.method=='POST':
        insert_new_comment(last_checked_user[0],postid,request.form['commm'])
    comments = get_comments(last_checked_user[0],postid)
    #print comments
    return render_template('comment.html',comments = comments,postid = postid)


@app.route('/replies/<commentid>' , methods=['POST','GET'])
def reply_view(commentid):
    if request.method=='POST':
        insert_new_reply(last_checked_user[0],commentid,request.form['commm'])
    replies = get_replies(last_checked_user[0],commentid)
    #print comments
    return render_template('reply.html',replies = replies,commentid = commentid)

@app.route('/like',methods=['POST','GET'])
def likeit():
    if request.method=='POST':
        already_liked = False
        for tupind in range(len(liked_or_dis)):
            if liked_or_dis[tupind][0]== last_checked_user[0] and liked_or_dis[tupind][1] == int(request.form['id']) :
                already_liked = liked_or_dis[tupind][2]
                break
        if request.form['like'] == 'up' and not already_liked:
            like(last_checked_user[0],int(request.form['id']),"up")
            liked_or_dis.append((last_checked_user[0],int(request.form['id']),"l"))
        elif not already_liked:
            dislike(last_checked_user[0],int(request.form['id']),"up")
            liked_or_dis.append((last_checked_user[0],int(request.form['id']),"d"))
        elif request.form['like'] == 'up' and already_liked=="d" :
            dislike(last_checked_user[0],int(request.form['id']),"down")
            like(last_checked_user[0],int(request.form['id']),"up")
            del(liked_or_dis[tupind])
            liked_or_dis.append((last_checked_user[0],int(request.form['id']),"l"))
        elif request.form['like'] == 'down' and already_liked=="l":
            like(last_checked_user[0],int(request.form['id']),"down")
            dislike(last_checked_user[0],int(request.form['id']),"up")
            del(liked_or_dis[tupind])
            liked_or_dis.append((last_checked_user[0],int(request.form['id']),"d"))
    address = 'blog.html#'+ str(request.form['id'])
    return render_template('blog.html',username=last_checked_user[0],posts_list=get_posts(last_checked_user[0]),scroll=request.form['id'])

@app.route('/blogs')
def show_blogs_list():
    if 'guest' not in session:
        session['guest'] = 'myg'
    return render_template('bloglist.html',username_list = get_usernames())

@app.route('/delete', methods=['POST','GET'])
def delete():
    if request.method=='POST':
        delete_post(session['username'],request.form['delete'])
    return redirect(url_for('manage'))

@app.route('/edit', methods=['POST','GET'])
def edit():
    if request.method=='POST':
        username = session['username']
        if 'edited' in request.form :

            edit_post(username,request.form['edited'],request.form['title'],request.form['post_text'])
            return redirect(url_for('manage'))


        else :

            post_id = request.form['edit']
            pos_list = get_posts(username)
            for i in pos_list :

                if int(i[0]) == int(post_id) :
                    post_tup = i

                    break

            return render_template('manager.html',posts= get_posts(username),thispost=post_tup)

@app.route('/blogs/<username>')
def show_blog(username):
    if 'guest' not in session:
        session['guest'] = 'myg'
    last_checked_user[0]=username
    return render_template('blog.html',username=username,posts_list= get_posts(username))
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/manage',methods=['POST','GET'])
def manage():
    if 'username' not in session:
        return render_template('errorshower.html',error='You must login first!')
    username = session['username']
    if request.method== 'POST':
        title = request.form['title']
        post_text = request.form['post_text']
        insert_new_post(username,title,post_text)

    return render_template('manager.html',posts=get_posts(username))

@app.route('/login',methods = ['POST', 'GET'])
def login(message = "" , mcolor = None):

    if 'username' in session:
        return render_template('errorshower.html',error='You are already logged in!')
    #return "hiiii"
    if request.method == 'POST':
        user = request.form['un']
        password = request.form['pass']
        captcha = (request.form['captch']).lower()
        captcha_con = False
        if captcha[0] == last_captcha[0] and captcha[1] == last_captcha[1] and captcha[2] == last_captcha[2] :
            captcha_con = True
        if validate_user(user,password) and captcha_con:
            message = "You succsesfully loged in"
            mcolor = "green"
            session['username'] = user
            make_needed_tables("username")
        elif captcha_con:
            message = "Username or Password is Wrong ... Please try again"
            mcolor = "red"
        else:
            message = "Wrong Captcha"
            mcolor = "red"
        get_captcha()
        return render_template("login.html",message=message,mcolor=mcolor,src = url_for('static' , filename = 'Captcha.jpg')+"?"+str(time.time()) )
    else:
        #return "h"
        get_captcha()
        return render_template("login.html",message = message, mcolor = mcolor,src = url_for('static' , filename = 'Captcha.jpg')+"?"+str(time.time()))
        return "hi"
    #return render_template("login.html",message = message, mcolor = mcolor)


@app.route('/Singup',methods=['POST','GET'])
def singup():
    if 'username' in session:
        return render_template('errorshower.html',error='You are already logged in!')
    message= ""
    mcolor = None
    if request.method == 'POST':
        user = request.form['un']
        password = request.form['pass']
        make_users_table()

        captcha = (request.form['captch']).lower()
        captcha_con = False
        if captcha[0] == last_captcha[0] and captcha[1] == last_captcha[1] and captcha[2] == last_captcha[2] :
            captcha_con = True

        if insert_user(user,password) and captcha_con :
            make_needed_tables(user)
            message= "You singup Succsesfully!"
            mcolor = "green"
        elif captcha_con:
            message= "This Username is already taken"
            mcolor = "red"
        else:
            message = "Wrong Captcha"
            mcolor = "red"
        #return redirect(url_for('login',message = message , mcolor = mcolor))
        get_captcha()
        return render_template("login.html",message = message, mcolor = mcolor,src = url_for('static' , filename = 'Captcha.jpg')+"?"+str(time.time()))
    else:
        get_captcha()
        return render_template("login.html",message = message, mcolor = mcolor,src = url_for('static' , filename = 'Captcha.jpg')+"?"+str(time.time()))
    #return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template('errorshower.html', error="You Successfully loged out!")

if __name__ == '__main__':
    tt=[]
    app.run(debug = True)
    #get_captcha()
    #make_captcha("s","g","f")