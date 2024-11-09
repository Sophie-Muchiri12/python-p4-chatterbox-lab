from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message  # Make sure to import db and the Message model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# Enable CORS to allow the frontend (React) to communicate with the backend
CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()  # Fetch all messages ordered by created_at
    return jsonify([message.to_dict() for message in messages])  # Convert each message to a dictionary and return as JSON

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()  # Parse incoming JSON data
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)  # Add new message to the database session
    db.session.commit()  # Commit the transaction to save the message in the database
    return jsonify(new_message.to_dict()), 201  # Return the created message as JSON

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()  # Get the updated data from the request
    message = Message.query.get_or_404(id)  # Fetch message by ID or return 404 if not found
    message.body = data['body']  # Update the message body
    db.session.commit()  # Commit the changes to the database
    return jsonify(message.to_dict())  # Return the updated message as JSON

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)  # Fetch the message by ID or return 404 if not found
    db.session.delete(message)  # Mark the message for deletion
    db.session.commit()  # Commit the changes to delete the message from the database
    return '', 204  # Return no content response (status code 204)

if __name__ == '__main__':
    app.run(port=5000)  # Run the Flask app on port 5000
