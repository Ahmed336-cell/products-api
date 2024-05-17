from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    is_boycott = db.Column(db.Boolean, nullable=False, default=False)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'description': self.description,
            'image_url': self.image_url,
            'isBoycott': self.is_boycott

        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
