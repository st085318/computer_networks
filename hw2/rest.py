from flask import Flask, jsonify, abort, request

app = Flask(__name__)
core = '/'
products = {
    1: {
        'id': 1,
        'title': u'Water',
        'description': u'Simple water'
    },
    2: {
        'id': 2,
        'title': u'Good water',
        'description': u'Tasty water'
    }
}

@app.route(core, methods=['GET'])
def get_all_products():
    return jsonify({'products': products})

@app.route(core + '<int:product_id>', methods=['GET'])
def get_product(product_id):
    if len(products) == 0:
        abort(404)
    
    if not(product_id in products):
        abort(404)

    return jsonify({product_id: products[product_id]})

@app.route(core, methods=['POST'])
def add_product():
    if not request.json['title']:
        abort(400)
    id = max(products.keys()) + 1
    product = {
        'id': id,
        'title': request.json['title'],
        'description': request.json.get('description', "")
    }
    products[id] = product
    return jsonify({'added product': products[id]}), 201

@app.route(core + '<int:product_id>', methods=['PUT'])
def put_product(product_id):
    if not request.json:
        abort(400)
    if 'title' not in request.json:
        abort(400)
    if not(product_id in products.keys()):
        abort(400)
    product = {
        'id': product_id,
        'title': request.json['title'],
        'description': request.json.get('description', "")
    }

    products[product_id] = product
    return jsonify({'putted product': products[product_id]})

@app.route(core + '<int:product_id>', methods=['DELETE'])
def del_product(product_id):
    products.pop(product_id)
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
