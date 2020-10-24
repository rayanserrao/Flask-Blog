from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pylint_flask
import pylint_flask_sqlalchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'   #confirguring databse with relative path(///)
                                                         #if i give 4 slahesit will be absolute path

db = SQLAlchemy(app)  #creating databse


class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self) :   #this method gonna printout wenever we create a new Posts
        return "Blog Post " +str(self.id)
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
    if request.method=='POST':
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        new_post=Posts(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/post')
    else:
        all_post=Posts.query.order_by(Posts.date).all()
        return render_template('post.html',all_post=all_post)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)