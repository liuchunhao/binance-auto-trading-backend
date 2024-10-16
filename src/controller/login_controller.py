from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from captcha.image import ImageCaptcha, ColorTuple
import redis


import random
import base64
import string
from io import BytesIO
import uuid
import logging
import os

ADMIN_LOGIN_PASSWORD = os.getenv('ADMIN_LOGIN_PASSWORD')

bp = Blueprint('login_controller', __name__)
r = redis.Redis(host='localhost', port=6379, db=0)  # Connect to your Redis instance



@bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    # get username, password, captcha, captcha_id from json request body
    payload = request.get_json()
    if not payload:
        return jsonify({'error': 'Please provide a valid JSON payload.'}), 400  # check if not exist, return 400
    
    username = payload['username']
    password = payload['password']
    captcha = payload['code']
    captcha_id = payload['uuid']
    
    # Get the CAPTCHA text from Redis
    captcha_text = r.get(captcha_id)

    if captcha_text is None:
        return jsonify({
                        'code': 401,
                        'msg': 'CAPTCHA code has expired.'
                        }), 401

    # Check if the CAPTCHA text entered by the user matches the one stored in Redis
    # Ignore case
    captcha_text = captcha_text.decode().upper()
    captcha = captcha.upper()
    if captcha != captcha_text:
        return jsonify({
                        'code': 401,
                        'msg': 'Invalid CAPTCHA code.'
                        }), 401

    if username == 'admin' and password == ADMIN_LOGIN_PASSWORD:
        return jsonify({
                        'code': 200,
                        'msg': 'Login successfully.',
                        #'token': 'O7F7iXmMKFhXLwwIPfhKBMxo9yOsD5GjmgafzYEkMoDvK4C13PbqF7ei2qCmGT1c'
                        'token': 'KFhXLwwIPfhKBMxo9yOsD5GjmgafzYEkMoDvK4C13PbqF7'
                        }), 200

    # return token 
    return jsonify({
                    'code': 200,
                    'msg': 'Please enter the CAPTCHA code in the login form.',
                    'token': ' '
                    })


@bp.route('/captcha')
@cross_origin()
def captcha():
    '''
    1. generate captcha
    2. save captcha value to redis
    3. return captcha image
    '''
    # Generate a random 5-character string
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    # Create a CAPTCHA image with noise
    image = ImageCaptcha(width=150, height=50, fonts=None, font_sizes=None)
    data = image.generate(captcha_text)

    # Convert the image data to base64
    base64_image = base64.b64encode(BytesIO(data.read()).getvalue()).decode()

    # Generate a UUID and store the CAPTCHA text in Redis
    captcha_id = str(uuid.uuid4())
    logging.info(f"captcha_id: {captcha_id}; captcha_text: {captcha_text}")

    r.set(captcha_id, captcha_text)
    # Set an expiration time on the key
    r.expire(captcha_id, 300)           

    # Return the CAPTCHA image and UUID
    return jsonify({
                    'code': 200,
                    'msg': 'Please enter the CAPTCHA code in the login form.',
                    'img': base64_image, 
                    'uuid': captcha_id,
                    'captchaEnabled': 'true'
                    })

