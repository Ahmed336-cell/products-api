from flask import Flask, request, jsonify
from models import db, Product, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.json'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        category_id=data['category_id'],
        description=data.get('description'),
        image_url=data.get('image_url'),
        is_boycott = data.get('isBoycott', False)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get_or_404(product_id)
    product.name = data['name']
    product.category_id = data['category_id']
    product.description = data.get('description')
    product.image_url = data.get('image_url')
    product.is_boycott = data.get('isBoycott', product.is_boycott)

    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict())

@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    category = Category.query.get_or_404(category_id)
    category.name = data['name']
    db.session.commit()
    return jsonify(category.to_dict())

@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
