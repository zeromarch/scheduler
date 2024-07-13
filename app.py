from flask import Flask, render_template
from models import db, Availability
from routes import availability_bp
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

app.register_blueprint(availability_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
