from flask import request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from models.product import ProductModel
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from models.db import db
import json
import math

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

product_fields = {
    'sno': fields.Integer,
    'name': fields.String,
    'desc': fields.String,
    'is_available': fields.Boolean
}

product_put_args = reqparse.RequestParser()
product_put_args.add_argument("name", type=str, help="Name of the product is required", required=True)
product_put_args.add_argument("desc", type=str, help="Description of the product")
product_put_args.add_argument("is_available", type=bool, help="Product's availability status is required", required=True)

product_update_args = reqparse.RequestParser()
product_update_args.add_argument("name", type=str, help="Name of the product")
product_update_args.add_argument("desc", type=str, help="Description of the product")
product_update_args.add_argument("is_available", type=bool, help="Product's availability status")


class AllProducts(Resource):
    @jwt_required()
    @marshal_with(product_fields)
    def get(self):
        try:
            products = ProductModel.query.all()
        except:
            abort(500, message="Internal server error")

        last = math.ceil(len(products)/int(params['no_of_products']))
        page = request.args.get('page')
        if(not str(page).isnumeric()):
            page = 1
        page= int(page)
        products = products[(page-1)*int(params['no_of_products']): (page-1)*int(params['no_of_products'])+ int(params['no_of_products'])]
        #Pagination Logic
        #First
        if (page==1):
            prev = "#"
            next = "/?page="+ str(page+1)
        elif(page==last):
            prev = "/?page=" + str(page - 1)
            next = "#"
        else:
            prev = "/?page=" + str(page - 1)
            next = "/?page=" + str(page + 1)

        return products, 200
        
    @jwt_required()
    @marshal_with(product_fields)
    def post(self):
        args = product_put_args.parse_args()
        try:
            product = ProductModel(name=args['name'], desc=args['desc'], is_available=args['is_available'])
        except:
            abort(500, message="Internal server error")
        db.session.add(product)
        db.session.commit()
        return product, 201
        

class Product(Resource):
    @jwt_required()
    @marshal_with(product_fields)
    def get(self, p_id):
        try:
            result = ProductModel.query.filter_by(sno=p_id).first()
        except:
            abort(500, message="Internal server error")
        if not result:
            abort(404, message="Could not find product with that id")
        return result, 200
        
    @jwt_required()
    @marshal_with(product_fields)
    def put(self, p_id):
        args = product_update_args.parse_args()
        try:
            result = ProductModel.query.filter_by(sno=p_id).first()
        except:
            abort(500, message="Internal server error")
        if not result:
            abort(404, message="Product doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['desc']:
            result.desc = args['desc']
        if str(args['is_available']):
            result.is_available = args['is_available']

        db.session.commit()

        return result
        
class Search(Resource):
    @marshal_with(product_fields)
    def get(self):
        q = request.args.get('q')
        try:
            results = ProductModel.query.filter(or_(ProductModel.name.like('%'+q+'%'), ProductModel.desc.like('%'+q+'%'))).all()
        except:
            abort(500, message="Internal server error")
        return results
        