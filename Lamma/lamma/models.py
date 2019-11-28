from lamma import loginManager, db, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



@loginManager.user_loader
def load_user(user_id):
 return User.query.get(int(user_id))


chat = db.Table('chat',
    db.Column('chat1', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat2', db.Integer, db.ForeignKey('user.id'))
)


liking =db.Table('liking',
    db.Column('liker_id', db.Integer , db.ForeignKey('user.id')),
    db.Column('post_liked_id', db.Integer , db.ForeignKey('post.id')),
    db.Column('rate_given' , db.Integer , default=0))


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


requests = db.Table('requests',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    #messages = db.relationship('Chats', backref='writer', lazy=True)
    stories = db.relationship('Story', backref='poster', lazy=True)    
    private = db.Column(db.Boolean)
    online = db.Column(db.Boolean , default=False)
    chatw =  db.relationship('User', 
                               secondary=chat, 
                               primaryjoin=(chat.c.chat1 == id), 
                               secondaryjoin=(chat.c.chat2 == id), 
                               backref=db.backref('chatter', lazy='dynamic'), 
                               lazy='dynamic')
    followed =  db.relationship('User', 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               backref=db.backref('followers', lazy='dynamic'), 
                               lazy='dynamic')
    requested_by =  db.relationship('User', 
                               secondary=requests, 
                               primaryjoin=(requests.c.follower_id == id), 
                               secondaryjoin=(requests.c.followed_id == id), 
                               backref=db.backref('requests', lazy='dynamic'), 
                               lazy='dynamic')
    liker =  db.relationship('Post', 
                               secondary=liking, 
                               backref=db.backref('likers', lazy='dynamic'), 
                               lazy='dynamic')

    def request(self,user):
        if not self.is_requesting(user):
            self.requested_by.append(user)
            return self

    def is_requesting(self , user):
        return self.requested_by.filter(requests.c.followed_id == user.id).count() > 0
    
    def unrequest(self, user):
        if self.is_requesting(user):
            self.requested_by.remove(user)
            return self

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def chatstart(self, user):
        if not self.is_chatting(user):
            self.chatw.append(user)
            return self

    def is_chatting(self, user):
        return self.chatw.filter(chat.c.chat2 == user.id).count() > 0            

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

def __repr__(self):
     return 'User(%s, %s, %s )' % ( self.username , self.email , self.image_file )




class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reciever_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20))
    like_percentage = db.Column(db.Integer , default=0)
    number_of_reactions = db.Column(db.Integer , default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def liked_by(self , user):
        if not self.is_liked_by(user):
            self.likers.append(user)
        return self
    
    def is_liked_by(self , user):
        return self.likers.filter(liking.c.liker_id == user.id).count() > 0             

    def unliked(self, user):
        if self.is_liked_by(user):
            self.likers.remove(user)
        return self    
        
def __repr__(self):
     return 'Post(%s , %s)' % ( self.title , self.date_posted, self.image )   



class Story(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    media = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)