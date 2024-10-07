from flask import Blueprint, jsonify, request
from models import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt ,current_user, get_jwt_identity

auth_bprint = Blueprint('auth', __name__)

@auth_bprint.post('/user/signup')
def register_user():
    data = request.get_json()
    f_name = data.get("f_name").lower()
    l_name = data.get("l_name").lower()
    email = data.get("email").lower()
    password = data.get("password")
    role = data.get("role").lower()
    user = User.query.filter_by(email=data.get("email")).first()
    if user is None:
        if f_name is None:
            return jsonify({"message": "f_name is required"}), 400
        if l_name is None:
            return jsonify({"message": "l_name is required"}), 400
        if email is None:
            return jsonify({"message": "email is required"}), 400
        if password is None:
            return jsonify({"message": "password is required"}), 400
        if role is None:
            return jsonify({"message": "role is required"}), 400
        if email in [i.email for i in User.query.all()]:
            return jsonify({"message": "email already taken, Try Again"}), 409 #Nantar Vichar Karne
        
        if data.get("role") == "user":
            new_user = User(
                f_name=f_name,
                l_name=l_name,
                email=email,
                role=role
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User_created"}), 201
        else:
            return jsonify({"message": "Unauthorized"}), 401

    else:
        return jsonify({"message": "User already exists, Try Again"}), 409
    
@auth_bprint.post('/user/login')
def login_user():
    data = request.get_json()
    email = data.get("email").lower()
    role = data.get("role").lower()
    if email not in [usr.email for usr in User.query.all()]:
        return jsonify({"message": "User does not exist"}), 404
    role_db = User.query.filter_by(email=email).first().role
    password = data.get("pass")
    ac_token = create_access_token(identity=email)
    ref_token  = create_refresh_token(identity=email)
    if email is None:
        return jsonify({"message": "email is required"}), 400
    if role is None:
        return jsonify({"message": "role is required"}), 400
    if password is None:
        return jsonify({"message": "password is required"}), 400
    if role != role_db:
        return jsonify({"message": "Unauthorized role"}), 403
    user = User.query.filter_by(email=email).first()
    if user and user.check_passw(password):
        return jsonify({"message": "Logged In Successfully",
                        "identity" : email,
                        "tokens": {
                            "ac_token": ac_token,
                            "ref_token": ref_token
                        }}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
@auth_bprint.post('/lib/login')
def login_lib():
    data = request.get_json()
    email = data.get("email").lower()
    role = data.get("role").lower()
    role_db = User.query.filter_by(email=email).first().role
    password = data.get("pass")
    ac_token = create_access_token(identity=email)
    ref_token  = create_refresh_token(identity=email)
    if email is None:
        return jsonify({"message": "email is required"}), 400
    if role is None:
        return jsonify({"message": "role is required"}), 400
    if password is None:
        return jsonify({"message": "password is required"}), 400
    if role != role_db:
        return jsonify({"message": "Unauthorized role"}), 403
    user = User.query.filter_by(email=email).first()
    if user and user.check_passw(password):
        return jsonify({"message": "Logged In Successfully", 
                        "tokens": {
                            "ac_token": ac_token,
                            "ref_token": ref_token,
                            "identity" : email
                        }}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bprint.get('/myinfo')
@jwt_required()
def my_info():
    exp_time = get_jwt()["exp"]
    return jsonify({"message": "Success", "user_details": {"usr_id":current_user.usr_id ,"email":current_user.email, "f_name":current_user.f_name, "l_name":current_user.l_name, "role":current_user.role, "exp":exp_time}}), 200

@auth_bprint.get('/refresh_access')
@jwt_required(refresh=True)
def refresh():
    cur_usr = get_jwt_identity()
    new_ac_token = create_access_token(identity=cur_usr)
    return jsonify({"email":cur_usr, "ac_token" : new_ac_token}), 200

@auth_bprint.get('/logout')
@jwt_required(verify_type=False)
def logout_usr():
    jwt = get_jwt()
    jti = jwt["jti"]
    tkn_type = jwt["type"]
    tkn = TknBlockList(jti=jti)
    db.session.add(tkn)
    db.session.commit()
    return jsonify({"message": f"{tkn_type} token revoked successfully"}), 200

@auth_bprint.route('/updtusr', methods=['GET','POST'])
@jwt_required()
def updt_usr():
    data = request.get_json()
    if current_user.check_passw(data['pass']):
      current_user.f_name = data['fname']
      current_user.l_name = data['lname']
      db.session.commit()
      return jsonify({'message': 'User updated'}), 200
    else:
      return jsonify({'message': 'Wrong password'}), 401
      
