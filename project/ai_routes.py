"""
AI-powered routes for MicroHMS
"""
from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timedelta
from .ai_features import SmartPricingEngine, BookingChatbot, OccupancyPredictor
from .models import Bookings, Hotels

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

# Initialize AI components
pricing_engine = SmartPricingEngine()
chatbot = BookingChatbot()
occupancy_predictor = OccupancyPredictor()


@ai_bp.route('/chatbot')
def chatbot_page():
    """Render the AI chatbot page."""
    return render_template('ai/chatbot.html')


@ai_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot conversations."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
            
        response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/pricing/recommend', methods=['POST'])
def recommend_pricing():
    """Get AI-powered pricing recommendations."""
    try:
        data = request.get_json()
        
        # Parse input data
        check_in = datetime.fromisoformat(data.get('check_in'))
        check_out = datetime.fromisoformat(data.get('check_out'))
        room_type = data.get('room_type', 'standard')
        
        # Get current occupancy (simplified - in real app would calculate from bookings)
        current_occupancy = data.get('current_occupancy', 0.6)
        
        # Get pricing recommendation
        recommendation = pricing_engine.calculate_dynamic_price(
            check_in, check_out, room_type, current_occupancy
        )
        
        return jsonify(recommendation)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/occupancy/predict', methods=['POST'])
def predict_occupancy():
    """Predict hotel occupancy for given dates."""
    try:
        data = request.get_json()
        target_date = datetime.fromisoformat(data.get('date'))
        
        prediction = occupancy_predictor.predict_occupancy(target_date)
        
        return jsonify(prediction)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/analytics/dashboard')
def analytics_dashboard():
    """Render AI analytics dashboard."""
    return render_template('ai/analytics.html')


@ai_bp.route('/analytics/data')
def analytics_data():
    """Provide analytics data for dashboard."""
    try:
        # Get recent bookings for analytics
        recent_bookings = Bookings.query.limit(100).all()
        
        # Calculate basic metrics
        total_bookings = len(recent_bookings)
        avg_tariff = sum(b.tariff for b in recent_bookings) / total_bookings if total_bookings > 0 else 0
        
        # Predict next week's occupancy
        predictions = []
        for i in range(7):
            future_date = datetime.now() + timedelta(days=i)
            prediction = occupancy_predictor.predict_occupancy(future_date)
            predictions.append({
                'date': future_date.isoformat(),
                'predicted_occupancy': prediction['predicted_occupancy']
            })
        
        return jsonify({
            'metrics': {
                'total_bookings': total_bookings,
                'average_tariff': round(avg_tariff, 2),
                'occupancy_predictions': predictions
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500