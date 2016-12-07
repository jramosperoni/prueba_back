import logging
import os
from flask import jsonify, g, request, Response, current_app
from . import api_bp
from .errors import unauthorized, bad_request, not_found
from ..models import Variedad
from ..models import Product
from ..models import Pallet
from ..models import ProductPackaging
from ..models import Color
from ..models import Calibre


@api_bp.route('/test_get/<int:id>')
def test_get(id):
    return jsonify({'status': 'OK', 'id': int(id)})


@api_bp.route('/test_post', methods=['POST'])
def test_post():
    if request.form is not None:
        name = request.form.get('name')
        return jsonify({'status': 'OK', 'name': str(name)})
    else:
        return bad_request('missing post param: name')


@api_bp.route('/variedades')
def getProducts():
    query = Variedad.query.order_by('id')
    variedades = [v.serialize() for v in query.all()]
    return jsonify({
        'status': 'OK',
        'result': variedades
    })


@api_bp.route('/products')
def getProductos():
    try:
        query = Product.query.order_by('id')
        productos = [p.serialize() for p in query.all()]
        return jsonify({
            'description': 'Success',
            'schema': productos
        })
    except Exception as e:
        return bad_request('Status 400')


@api_bp.route('/product/<int:productId>')
def getProductoById(productId):
    i = int(productId)
    try:
        ProductoId = Product.query.filter(Product.id == productId).first()
        return jsonify({
            'description': 'Success',
            'schema': ProductoId.serialize()
        })
    except AttributeError:
        return bad_request('Status 400')


@api_bp.route('/pallets/findByProducto', methods=['GET'])
def findPalletsByProducto():
    try:
        variedad = int(request.args.get('variedad'))
        status = int(request.args.get('status'))
        color = int(request.args.get('color'))
        calibre = int(request.args.get('calibre'))
        query = Pallet.query.join(
                ProductPackaging).join(
                Product).join(
                Variedad).join(
                Color).join(
                Calibre).filter(
                Variedad.id == variedad).filter(
                Pallet.status == status).filter(
                Color.id == color).filter(
                Calibre.id == calibre)
        pallets = [p.serialize() for p in query.all()]
    except Exception as e:
        return bad_request('Status 400')
    return jsonify({
        'description': 'Success',
        'schema': pallets
    })
