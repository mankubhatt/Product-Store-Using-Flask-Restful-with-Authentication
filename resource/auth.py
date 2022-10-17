from flask import jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from models.user import UserModel
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from models.db import db

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String
}

user_register_args = reqparse.RequestParser()
user_register_args.add_argument("username", type=str, help="username is required", required=True)
user_register_args.add_argument("password", type=str, help="password is required", required=True)



class Register(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_register_args.parse_args()
        try:
            result = UserModel.query.filter_by(username=args['username']).first()
        except:
            abort(500, message="Internal server error")
        if result:
            abort(403, message="user already exists")
        user = UserModel(username=args["username"])
        user.hash_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
class Login(Resource):
    def post(self):
        args = user_register_args.parse_args()
        try:
            result = UserModel.query.filter_by(username=args['username']).first()
        except:
            abort(500, message="Internal server error")
        if not result:
            abort(400, message="No User Exists with given username")
        if not result.check_password(args['password']):
            abort(401, message="wrong username or password")
        access_token = create_access_token(identity=args["username"], fresh=True)
        refresh_token = create_refresh_token(identity="example_user")
        return jsonify(access_token=access_token, refresh_token=refresh_token)
        


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return jsonify(access_token=access_token)
