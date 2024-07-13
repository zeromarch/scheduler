from flask import Flask
from models import db, Availability
from routes import availability_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

app.register_blueprint(availability_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
