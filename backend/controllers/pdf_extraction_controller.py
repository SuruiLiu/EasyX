from flask import Blueprint, request, jsonify

from services.pdf_extraction_service import PdfExtractionService

from services.save_meta import save_meta, extract_and_save, save_meta_with_extras

import os
import uuid
import io

pdf_extraction_bp = Blueprint('pdf_extraction', __name__, url_prefix='/api')
pdf_extraction_service = PdfExtractionService()

@pdf_extraction_bp.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    """Handle PDF file upload and text extraction for preview"""
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No pdf_file part in the request"}), 400
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if pdf_file and pdf_file.filename.lower().endswith('.pdf'):
        try:
            # Read the file into memory
            pdf_content = pdf_file.read()
            pdf_stream = io.BytesIO(pdf_content)
            
            # Extract data from PDF
            extracted_data = pdf_extraction_service.extract_timesheet_data(pdf_stream)
            if "error" in extracted_data:
                return jsonify({"error": extracted_data["error"]}), 500
            
            # Get PDF text for preview
            pdf_stream.seek(0)  # Reset stream position
            pdf_text = pdf_extraction_service.get_pdf_text(pdf_stream)
            
            return jsonify({
                "success": True,
                "data": extracted_data,
                "pdf_text": pdf_text
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

@pdf_extraction_bp.route('/extract-meta', methods=['POST'])
def extract_meta():
    """Handle PDF file upload and extract structured metadata"""
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No pdf_file part in the request"}), 400
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if pdf_file and pdf_file.filename.lower().endswith('.pdf'):
        try:
            # Read the file into memory
            pdf_content = pdf_file.read()
            pdf_stream = io.BytesIO(pdf_content)
            
            # Extract meta data from PDF
            meta_data = pdf_extraction_service.extractMeta(pdf_stream)
            if "error" in meta_data:
                return jsonify({"error": meta_data["error"]}), 500
            
            return jsonify({
                "success": True,
                "meta_data": meta_data
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

@pdf_extraction_bp.route('/extract-meta-save', methods=['POST'])
def extract_meta_and_save():
    """Upload PDF, extract metadata, and save JSON into PostgreSQL in one step"""
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No pdf_file part in the request"}), 400
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if pdf_file and pdf_file.filename.lower().endswith('.pdf'):
        try:
            # Read PDF content into memory stream
            pdf_content = pdf_file.read()
            pdf_stream = io.BytesIO(pdf_content)
            
            # Get optional form parameters
            status = request.form.get('status', 'done')
            notes = request.form.get('notes')
            
            # Extract metadata first for response
            meta_data = pdf_extraction_service.extractMeta(pdf_stream)
            if "error" in meta_data:
                return jsonify({"error": meta_data["error"]}), 500
            
            # Get PDF text for response
            pdf_stream.seek(0)  # Reset stream position
            pdf_text = pdf_extraction_service.get_pdf_text(pdf_stream)
            
            # Save to PostgreSQL with extracted data and optional extras
            pdf_stream.seek(0)  # Reset stream position again
            tid = extract_and_save(
                pdf_stream,
                status=status,
                keep_pdf_text=True,
                filename=pdf_file.filename,
                notes=notes,
            )
            
            # Return comprehensive response with all extracted data
            return jsonify({
                "success": True,
                "tid": tid,
                "filename": pdf_file.filename,
                "status": status,
                "meta_data": meta_data,
                "pdf_text": pdf_text
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Error processing or saving PDF: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

@pdf_extraction_bp.route('/save-meta-json', methods=['POST'])
def save_meta_json():
    """Accept extracted metadata JSON from frontend and save to PostgreSQL."""
    try:
        payload = request.get_json(silent=True) or {}
        meta = payload.get('meta_data') or payload.get('meta')
        
        if not isinstance(meta, dict):
            return jsonify({"error": "meta_data must be an object"}), 400
        
        status = str(payload.get('status') or 'done')
        # Save "pure metadata" as JSONB to meet the requirement of directly storing extracted JSON
        tid = save_meta(meta, status=status)
        
        return jsonify({"success": True, "tid": tid}), 200
    except Exception as e:
        return jsonify({"error": f"Error saving meta JSON: {e}"}), 500
