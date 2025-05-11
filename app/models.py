from datetime import datetime
from app import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates

class BaseModel:
    """Base model class that includes common fields and methods"""
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save the model instance to the database"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the model instance from the database"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        """Get a model instance by its ID"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all instances of the model"""
        return cls.query.all()

class JournalEntry(db.Model, BaseModel):
    """Journal Entry model with enhanced features"""
    
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50))  # Optional field for tracking mood
    tags = db.Column(db.String(200))  # Optional field for tags (comma-separated)
    
    @validates('title')
    def validate_title(self, key, title):
        """Validate the title field"""
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title cannot be longer than 200 characters")
        return title
    
    @validates('content')
    def validate_content(self, key, content):
        """Validate the content field"""
        if not content:
            raise ValueError("Content cannot be empty")
        return content
    
    def __repr__(self):
        return f'<JournalEntry {self.title}>'
    
    def to_dict(self):
        """Convert the model instance to a dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'mood': self.mood,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def search_by_title(cls, search_term):
        """Search entries by title"""
        return cls.query.filter(cls.title.ilike(f'%{search_term}%')).all()
    
    @classmethod
    def get_by_mood(cls, mood):
        """Get entries by mood"""
        return cls.query.filter_by(mood=mood).all()
    
    @classmethod
    def get_by_tag(cls, tag):
        """Get entries by tag"""
        return cls.query.filter(cls.tags.ilike(f'%{tag}%')).all()
    
    def add_tag(self, tag):
        """Add a tag to the entry"""
        current_tags = set(self.tags.split(',')) if self.tags else set()
        current_tags.add(tag)
        self.tags = ','.join(current_tags)
        return self.save()
    
    def remove_tag(self, tag):
        """Remove a tag from the entry"""
        if self.tags:
            current_tags = set(self.tags.split(','))
            current_tags.discard(tag)
            self.tags = ','.join(current_tags) if current_tags else None
            return self.save()
        return self 