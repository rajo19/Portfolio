from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests
import uuid
from datetime import datetime
from bson import ObjectId
from config import Config
from models import RESUME_CONTEXT
from database import chat_sessions_collection

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat/sessions', methods=['POST'])
def create_chat_session():
    """Create a new chat session"""
    data = request.get_json()
    metadata = data.get('metadata', {})
    
    session_data = {
        'messages': [],
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow(),
        'metadata': metadata
    }
    
    result = chat_sessions_collection.insert_one(session_data)
    session_data['_id'] = str(result.inserted_id)
    
    return jsonify(session_data), 201

@ai_bp.route('/chat/sessions/<session_id>', methods=['GET'])
def get_chat_session(session_id):
    """Get chat session by ID"""
    try:
        session = chat_sessions_collection.find_one({'_id': ObjectId(session_id)})
        if not session:
            return jsonify({'message': 'Session not found'}), 404
        
        session['_id'] = str(session['_id'])
        return jsonify(session)
    except Exception as e:
        return jsonify({'message': 'Invalid session ID'}), 400

@ai_bp.route('/chat/message', methods=['POST'])
def add_message_to_session():
    """Add a message to a chat session. Creates new session if conversation_id not provided."""
    try:
        data = request.get_json()
        question = data.get('question', '')
        conversation_id = data.get('conversation_id')
        
        if not question:
            return jsonify({'message': 'Question is required'}), 400
        
        session = None
        session_id = None
        
        # If conversation_id is provided, verify and retrieve existing session
        if conversation_id:
            try:
                session = chat_sessions_collection.find_one({'_id': ObjectId(conversation_id)})
                if not session:
                    return jsonify({'message': 'Conversation not found'}), 404
                session_id = conversation_id
            except Exception:
                return jsonify({'message': 'Invalid conversation_id format'}), 400
        else:
            # Create new session if conversation_id not provided
            session_data = {
                'messages': [],
                'createdAt': datetime.utcnow(),
                'updatedAt': datetime.utcnow(),
                'metadata': {
                    'page': 'chat',
                    'type': 'conversation'
                }
            }
            
            result = chat_sessions_collection.insert_one(session_data)
            session_id = str(result.inserted_id)
            session = session_data
            session['_id'] = ObjectId(session_id)
        
        # Now process the AI request with the session (either existing or newly created)
        groq_api_key = Config.GROQ_API_KEY
        if not groq_api_key:
            return jsonify({'message': 'AI service not configured'}), 500
        
        # Build conversation context from existing messages
        messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant acting as a professional yet witty 'wingman' for Rajorshi Tah. "
                            "Your job is to answer questions about Rajorshi based only on his resume and professional background. "
                            "When the question is within context, respond factually, clearly, and in a professional tone. "
                    "If the question is out of context or not answerable from the resume, respond humorously while still making Rajorshi look good. "
                    "For example, say things like: "
                    "'I don’t have that info, but given his track record of leading teams, he’d probably ace it,' "
                    "or 'That’s not in the resume, but with his IIT background, I wouldn’t be surprised if he secretly built it over a weekend.' "
                    "Always aim to make Rajorshi sound skilled, resourceful, and likable. "
                    f"Here is the resume and professional background information:\n\n{RESUME_CONTEXT}"
                )
            }
        ]
        
        # Add previous messages for context (last 10 to avoid token limits)
        for msg in session.get('messages', [])[-10:]:
            messages.append({
                'role': 'user' if msg['sender'] == 'user' else 'assistant',
                'content': msg['content']
            })
        
        # Add current question
        messages.append({
            'role': 'user',
            'content': question
        })
        
        headers = {
            'Authorization': f'Bearer {groq_api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'groq/compound',
            'messages': messages,
            'max_tokens': 1024,
            'temperature': 0.7,
            'top_p': 0.9,
            'stop': ['<|eot_id|>', '<|end_of_text|>', 'Human:', 'AI:'],
            'stream': False
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Groq API Response Status: {response.status_code}")
        print(f"Groq API Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            
            # Create new messages
            current_time = datetime.utcnow()
            user_message = {
                'sender': 'user',
                'content': question,
                'timestamp': current_time.isoformat() + 'Z'
            }
            
            bot_message = {
                'sender': 'bot',
                'content': answer,
                'timestamp': current_time.isoformat() + 'Z'
            }
            
            # Update session with new messages
            chat_sessions_collection.update_one(
                {'_id': ObjectId(session_id)},
                {
                    '$push': {
                        'messages': {
                            '$each': [user_message, bot_message]
                        }
                    },
                    '$set': {
                        'updatedAt': current_time
                    }
                }
            )
            
            return jsonify({
                'answer': answer,
                'conversation_id': session_id,
                'user_message': user_message,
                'bot_message': bot_message
            })
        else:
            return jsonify({
                'message': 'AI service error',
                'status_code': response.status_code,
                'error_details': response.text
            }), 500
            
    except Exception as e:
        return jsonify({'message': f'AI service error: {str(e)}'}), 500

@ai_bp.route('/chat/sessions/<session_id>/messages', methods=['POST'])
def add_message_to_existing_session(session_id):
    """Add a message to existing chat session and get AI response (legacy endpoint)"""
    # Use the new unified endpoint with conversation_id
    data = request.get_json()
    data['conversation_id'] = session_id
    
    # Call the unified function
    return add_message_to_session()

@ai_bp.route('/chat/sessions', methods=['GET'])
@jwt_required()
def get_all_chat_sessions():
    """Get all chat sessions (admin only)"""
    sessions = list(chat_sessions_collection.find().sort('updatedAt', -1))
    for session in sessions:
        session['_id'] = str(session['_id'])
    return jsonify(sessions)

@ai_bp.route('/chat/sessions/<session_id>', methods=['DELETE'])
def delete_chat_session(session_id):
    """Delete a chat session"""
    try:
        result = chat_sessions_collection.delete_one({'_id': ObjectId(session_id)})
        if result.deleted_count:
            return jsonify({'message': 'Session deleted'})
        return jsonify({'message': 'Session not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Invalid session ID'}), 400

# Legacy endpoint for backward compatibility
@ai_bp.route('/ask', methods=['POST'])
def ai_ask():
    """Legacy ask endpoint - creates new session for each question"""
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'message': 'Question is required'}), 400
    
    # Create new session
    session_data = {
        'messages': [],
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow(),
        'metadata': {
            'page': 'legacy',
            'type': 'single_question'
        }
    }
    
    result = chat_sessions_collection.insert_one(session_data)
    session_id = str(result.inserted_id)
    
    # Use the session message endpoint
    return add_message_to_session(session_id)
