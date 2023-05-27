from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import app, db
from app.model import Users

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Add your login logic here
    user = Users.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    # if not user or not check_password_hash(user.password, password):
    #     flash('Please check your login details and try again.')
    #     return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    
    # Verify user credentials (dummy example)
    if email == user.email and password == user.password:
        access_token =create_access_token(identity=email)
        return jsonify({'token': access_token, 'message': 'login success!'}), 200
    else:
        return jsonify({'message': 'invalid email or password'}), 401


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Add your registration logic here
    
    # Store user in the database
    new_user = Users(
        user_id='generate_user_id',  # Generate a unique user ID
        username=username,
        email=email,
        password=password,
        created_at='2023-05-29 00:00:00',  # Set the current timestamp
        created_by='user_id',  # Set the user ID of the creator
        updated_by='user_id',  # Set the user ID of the updater
        updated_at='2023-05-29 00:00:01'  # Set the current timestamp
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful'}), 201


@app.route('/sleep/quality', methods=['GET'])
@jwt_required()
def get_sleep_quality():
    date = request.args.get('date')
    
    # Add your logic to retrieve sleep quality based on the provided date
    
    sleep_time = 8  # Dummy sleep time
    sleep_noise = 2  # Dummy sleep noise
    sleep_score = 9  # Dummy sleep score
    snore_count = 5  # Dummy snore count
    
    return jsonify({
        "sleepTime": sleep_time,
        "sleepNoise": sleep_noise,
        "sleepScore": sleep_score,
        "snoreCount": snore_count
    }), 200


@app.route('/sleep/session', methods=['POST'])
@jwt_required()
def save_sleep_session():
    # Assuming the request contains an audio file and other form data
    audio_recording = request.files['audioRecording']
    from_time = request.form.get('fromTime')
    to_time = request.form.get('toTime')
    
    # Add your logic to save the sleep session
    url_recording = "path/to/save/audio/recording.wav"  # Modify this path
    
    new_session = SleepSession(
        session_id='generate_session_id',  # Generate a unique session ID
        user_id='current_user_id',  # Get the current user ID from the JWT
        from_time=from_time,
        to_time=to_time,
        sleep_time=calculate_sleep_time(from_time, to_time),  # Call your sleep time calculation function
        url_recording=url_recording,
        noise=calculate_sleep_noise_ratio(url_recording),  # Call your sleep noise calculation function
        created_at='current_timestamp',  # Set the current timestamp
        created_by='user_id',  # Set the user ID of the creator
        updated_by='user_id',  # Set the user ID of the updater
        updated_at='current_timestamp'  # Set the current timestamp
    )
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify({"message": "Sleep session saved successfully"}), 201


@app.route('/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    
    # Assuming you have a logged-in user and retrieve their profile information
    user = User.query.filter_by(email=current_user).first()
    
    return jsonify({
        "username": user.username,
        "email": user.email
    }), 200


if __name__ == '__main__':
    app.run()
