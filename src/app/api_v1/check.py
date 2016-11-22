import logging
import os
from flask import jsonify, g, request, Response, current_app
from . import api_bp
from .errors import unauthorized, bad_request
from ..models import Variedad


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