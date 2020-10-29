from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pylint_flask
import pylint_flask_sqlalchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'   #confirguring databse with relative path(///)
                                                         #if i give 4 slahesit will be absolute path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///contacts.db'

db = SQLAlchemy(app)  #creating databse


class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self) :   #this method gonna printout wenever we create a new Posts
        return "Blog Post " +str(self.id)




class Contacts(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False)
    email = db.Column(db.String(20),  nullable=False)
    phone_num = db.Column(db.String(15),  nullable=False)
    message = db.Column(db.String(200), nullable=False)


    def __repr__(self) :  

        return "Contact " +str(self.id)

    

posts=[
    {'name':'rayan',
        'age':22,
        'salary':30000},
                                                     #dummpy databse to check
        {'name':'raksh','age':22,'salary':200000}
]

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/about')
def about():
    title="About python techie"
    return render_template('about.html',title=title,posts=posts)

@app.route('/post',methods=['POST','GET'])
def post():
    if request.method=='POST':                  # if your posting /putting some data to form
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        new_post=Posts(title=post_title,content=post_content,author=post_author)  #creating new post
        db.session.add(new_post)     #add into session the post created, it will be delted after this session
        db.session.commit()         #to save it permamnemtly u need to commit the changes
        return redirect('/post')    #which page u wnat to redirect to
    else:
        all_post=Posts.query.order_by(Posts.date).all()
        return render_template('post.html',all_post=all_post)

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':  
        contact_name=request.form['cname']
        contact_email=request.form['cemail']
        contact_phone=request.form['cphone']
        conact_message=request.form['cmsg']
        new_contact=Contacts(name=contact_name,email=contact_email,phone_num=contact_phone,message=conact_message)
        db.session.add(new_contact)
        db.session.commit()
        return redirect('/')

    else:
        # all_contacts=Contacts.query.order_by(Contacts.name).all()

        return render_template('contact.html')

@app.route('/contact/info',methods=['GET'])
def contactinfo():
    all_contacts=Contacts.query.order_by(Contacts.name).all()
    return render_template('contactinfo.html',all_contacts=all_contacts)

@app.route('/delete/<int:id>')
def delete(id):
    post=Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')

@app.route('/edit/<int:id>', methods=['GET','POST']) 
def edit(id):
    if request.method=='POST':

        post=Posts.query.get_or_404(id)
        post.title=request.form['title']
        post.content=request.form['content']
        post.author=request.form['author']
        db.session.commit()
        return redirect('/post')
    else:
        post=Posts.query.get_or_404(id)
        return render_template('edit.html', post=post)

@app.route('/post/newpost',methods=['GET','POST'])
def newpost():
    if request.method=='POST':

        
        post.title=request.form['title']
        post.content=request.form['content']
        post.author=request.form['author']
        new_post=Posts(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post) 
        db.session.commit()
        return redirect('/post')
    else:
        
        return render_template('new_post.html')




if __name__ == "__main__":
    app.run(debug=True)