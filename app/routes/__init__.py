from flask import Blueprint, request, jsonify
from app.services.document_service import DocumentService
from app.services.qa_service import QAService
from app.middleware.auth import jwt_required

api_bp = Blueprint('api', __name__)
doc_service = DocumentService()
qa_service = QAService()

@api_bp.route('/documents', methods=['POST'])
@jwt_required
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400
    
    success, message = doc_service.process_document(file)
    return jsonify({'success': success, 'message': message})

@api_bp.route('/query', methods=['POST'])
@jwt_required
def query():
    data = request.get_json()
    if 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    
    response, tokens = qa_service.process_query(data['question'])
    return jsonify({
        'response': response,
        'tokens_used': tokens
    })