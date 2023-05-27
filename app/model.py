from app import db


class Users(db.Model):
    user_id = db.Column(db.String(50), primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)
    deleted_by = db.Column(db.String(50))
    deleted_at = db.Column(db.TIMESTAMP)


class SleepSession(db.Model):
    session_id = db.Column(db.String(50), primary_key=True, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id'), nullable=False)
    from_time = db.Column(db.TIMESTAMP, nullable=False)
    to_time = db.Column(db.TIMESTAMP, nullable=False)
    sleep_time = db.Column(db.Integer, nullable=False)
    url_recording = db.Column(db.String(255), nullable=False)
    noise = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)
    deleted_by = db.Column(db.String(50))
    deleted_at = db.Column(db.TIMESTAMP)


class SleepScore(db.Model):
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id'), nullable=False, primary_key=True)
    sleep_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)
    deleted_by = db.Column(db.String(50))
    deleted_at = db.Column(db.TIMESTAMP)


class SleepSnore(db.Model):
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'), nullable=False, primary_key=True)
    snore_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)
    deleted_by = db.Column(db.String(50))
    deleted_at = db.Column(db.TIMESTAMP)


if __name__ == '__main__':
    db.create_all()
