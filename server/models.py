from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import CheckConstraint

from config import db, bcrypt

class User(db.Model, SerializerMixin):

    __tablename__ = 'users'

    serialize_rules = ('-recipies.user',)
       
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', backref='user')

    @hybrid_property
    def password_hash(self):
        if self._password_hash:
            raise AttributeError('Password hashes may not be viewed.')
            
    @password_hash.setter
    def password_hash(self, password):
        
        password_hash = bcrypt.generate_password_hash( password.encode('utf-8'))
        
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    __table_args__ = (
        CheckConstraint('length(instructions) >= 50', name='check_instructions_length'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
            'minutes_to_complete': self.minutes_to_complete,
            'user_id': self.user_id
        }
