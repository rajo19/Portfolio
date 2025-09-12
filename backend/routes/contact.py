from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message, Mail
from flask_jwt_extended import jwt_required
from bson import ObjectId
from datetime import datetime
from database import contact_collection

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    subject = data.get('subject', '')
    message = data.get('message', '')
    
    if not all([name, email, subject, message]):
        return jsonify({'message': 'All fields are required'}), 400
    
    # Save contact submission to database
    contact_data = {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
        'created_at': datetime.utcnow()
    }
    
    try:
        # Save to database
        result = contact_collection.insert_one(contact_data)
        
        # Check if email is configured
        mail_username = current_app.config.get('MAIL_USERNAME')
        mail_password = current_app.config.get('MAIL_PASSWORD')
        mail_default_sender = current_app.config.get('MAIL_DEFAULT_SENDER')
        
        if not mail_username or not mail_password or mail_password == 'your-gmail-app-password-here':
            print("Warning: Email not properly configured, skipping email notification")
            return jsonify({
                'message': 'Message saved successfully (email notification disabled - configure MAIL_PASSWORD in .env)',
                'id': str(result.inserted_id)
            })
        
        # Send email notification
        mail = current_app.extensions['mail']
        sender_email = mail_default_sender or mail_username
        
        msg = Message(
            subject=f'Portfolio Contact: {subject}',
            sender=sender_email,
            recipients=['rajorshitah9@gmail.com'],
            body=f'''
New contact form submission:


Name: {name}
Email: {email}
Subject: {subject}


Message:
{message}


Submission ID: {str(result.inserted_id)}
            '''
        )
        
        try:
            mail.send(msg)
            print(f"Email sent successfully to rajorshitah9@gmail.com")
            return jsonify({
                'message': 'Message sent successfully',
                'id': str(result.inserted_id)
            })
        except Exception as email_error:
            print(f"Email sending failed: {str(email_error)}")
            # Still return success since the message was saved to database
            return jsonify({
                'message': 'Message saved successfully (email notification failed)',
                'id': str(result.inserted_id),
                'email_error': str(email_error)
            })
        
    except Exception as e:
        print(f"Database error: {str(e)}")
        return jsonify({'message': f'Failed to save message: {str(e)}'}), 500

@contact_bp.route('', methods=['GET'])
@jwt_required()
def get_contacts():
    """Get all contact submissions (admin only)"""
    contacts = list(contact_collection.find().sort('created_at', -1))
    for contact in contacts:
        contact['_id'] = str(contact['_id'])
    return jsonify(contacts)

@contact_bp.route('/<contact_id>', methods=['PUT'])
@jwt_required()
def update_contact_status(contact_id):
    """Update contact submission status (admin only)"""
    data = request.get_json()
    status = data.get('status', 'unread')
    
    if status not in ['unread', 'read', 'replied']:
        return jsonify({'message': 'Invalid status'}), 400
    
    result = contact_collection.update_one(
        {'_id': ObjectId(contact_id)},
        {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
    )
    
    if result.modified_count:
        return jsonify({'message': 'Contact status updated'})
    return jsonify({'message': 'Contact not found'}), 404

@contact_bp.route('/<contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    """Delete contact submission (admin only)"""
    result = contact_collection.delete_one({'_id': ObjectId(contact_id)})
    
    if result.deleted_count:
        return jsonify({'message': 'Contact deleted'})
    return jsonify({'message': 'Contact not found'}), 404
