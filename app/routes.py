from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from app import app, db
from app.model import Users, SleepSession, SleepScore, SleepSnore
from app.utils import calculate_sleep_time, save_audio_file, calculate_sleep_noise
from datetime import datetime
import shortuuid

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Add your login logic here
    user = Users.query.filter_by(email=email).first()
    
    # Verify user credentials (dummy example)
    if email == user.email and password == user.password:
        additional_claims = {
            "username": user.username,
            "email": user.email,
            "user_id": user.user_id,
        }
        access_token =create_access_token(identity=email, additional_claims=additional_claims)
        return jsonify({'token': access_token, 'message': 'login success!'}), 200
    else:
        return jsonify({'message': 'invalid email or password'}), 401

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Add your registration logic here

    current_timestamp = datetime.now().isoformat()
    
    # Store user in the database
    new_user = Users(
        user_id=shortuuid.uuid(),  # Generate a unique user ID
        username=username,
        email=email,
        password=password,
        created_at=current_timestamp,  # Set the current timestamp
        created_by='SYSTEM',  # Set the user ID of the creator
        updated_by='SYSTEM',  # Set the user ID of the updater
        updated_at=current_timestamp  # Set the current timestamp
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful'}), 201


@app.route('/sleep/quality', methods=['GET'])
@jwt_required()
def get_sleep_quality():
    date = request.args.get('date')

    # Add your logic to retrieve sleep quality based on the provided date
    
    sleep_time =  10 # Dummy sleep time
    sleep_noise = 2  # Dummy sleep noise
    sleep_score = 9  # Dummy sleep score
    snore_count = 5  # Dummy snore count
    
    return jsonify({
        "sleepTime": sleep_time,
        "sleepNoise": sleep_noise,
        "sleepScore": sleep_score,
        "snoreCount": snore_count,
    }), 200


@app.route('/sleep/session', methods=['POST'])
@jwt_required()
def save_sleep_session():
    # Assuming the request contains an audio file and other form data
    audio_recording = request.files['audioRecording']
    from_time = request.form.get('fromTime')
    to_time = request.form.get('toTime')

    claims = get_jwt()
    
    # Add your logic to save the sleep session
    audio_file_path = save_audio_file(audio_recording)
    current_timestamp = datetime.now().isoformat()

    new_session = SleepSession(
        session_id= shortuuid.uuid(),  # Generate a unique session ID
        user_id=claims['user_id'],  # Get the current user ID from the JWT
        from_time=from_time,
        to_time=to_time,
        sleep_time=calculate_sleep_time(from_time, to_time),  # Call your sleep time calculation function
        url_recording=audio_file_path,
        noise=10,  # Call your sleep noise calculation function
        # noise=calculate_sleep_noise(audio_file_path),  # Call your sleep noise calculation function
        created_at=current_timestamp,  # Set the current timestamp
        created_by=claims['user_id'],  # Set the user ID of the creator
        updated_by=claims['user_id'],  # Set the user ID of the updater
        updated_at=current_timestamp  # Set the current timestamp
    )
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify({"message": "Sleep session saved successfully"}), 201


@app.route('/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    claims = get_jwt()
    email = claims['email']
    
    # Assuming you have a logged-in user and retrieve their profile information
    user = Users.query.filter_by(email=email).first()
    
    return jsonify({
        "username": user.username,
        "email": user.email
    }), 200


if __name__ == '__main__':
    app.run()
