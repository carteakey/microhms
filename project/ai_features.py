"""
AI-powered features for MicroHMS
"""
import os
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional


class SmartPricingEngine:
    """AI-powered dynamic pricing for hotel rooms."""
    
    def __init__(self):
        self.base_rate = 100.0  # Base room rate
        
    def calculate_dynamic_price(self, 
                              check_in_date: datetime,
                              check_out_date: datetime,
                              room_type: str = "standard",
                              current_occupancy: float = 0.5) -> Dict:
        """
        Calculate dynamic pricing based on various factors.
        
        Args:
            check_in_date: Guest check-in date
            check_out_date: Guest check-out date  
            room_type: Type of room (standard, deluxe, suite)
            current_occupancy: Current hotel occupancy rate (0.0-1.0)
            
        Returns:
            Dict with recommended price and reasoning
        """
        base_price = self.base_rate
        
        # Room type multiplier
        room_multipliers = {
            "standard": 1.0,
            "deluxe": 1.5,
            "suite": 2.0
        }
        
        # Occupancy-based pricing
        if current_occupancy > 0.8:
            occupancy_multiplier = 1.3  # High demand
        elif current_occupancy > 0.6:
            occupancy_multiplier = 1.1  # Medium demand
        else:
            occupancy_multiplier = 0.9  # Low demand, discount
            
        # Seasonal/day-of-week adjustments
        day_of_week = check_in_date.weekday()
        if day_of_week >= 5:  # Weekend (Fri, Sat)
            day_multiplier = 1.2
        else:
            day_multiplier = 1.0
            
        # Advance booking discount
        days_in_advance = (check_in_date - datetime.now()).days
        if days_in_advance > 30:
            advance_multiplier = 0.95  # Early bird discount
        elif days_in_advance < 7:
            advance_multiplier = 1.1  # Last minute premium
        else:
            advance_multiplier = 1.0
            
        # Calculate final price
        final_price = (base_price * 
                      room_multipliers.get(room_type, 1.0) * 
                      occupancy_multiplier * 
                      day_multiplier * 
                      advance_multiplier)
        
        return {
            "recommended_price": round(final_price, 2),
            "base_price": base_price,
            "factors": {
                "room_type_multiplier": room_multipliers.get(room_type, 1.0),
                "occupancy_multiplier": occupancy_multiplier,
                "day_multiplier": day_multiplier,
                "advance_booking_multiplier": advance_multiplier
            },
            "reasoning": self._generate_pricing_explanation(
                occupancy_multiplier, day_multiplier, advance_multiplier
            )
        }
    
    def _generate_pricing_explanation(self, occ_mult: float, day_mult: float, adv_mult: float) -> str:
        """Generate human-readable explanation for pricing."""
        explanations = []
        
        if occ_mult > 1.1:
            explanations.append("High demand period")
        elif occ_mult < 0.95:
            explanations.append("Low occupancy discount applied")
            
        if day_mult > 1.0:
            explanations.append("Weekend premium")
            
        if adv_mult < 1.0:
            explanations.append("Early booking discount")
        elif adv_mult > 1.0:
            explanations.append("Last-minute booking premium")
            
        if not explanations:
            explanations.append("Standard pricing")
            
        return "; ".join(explanations)


class BookingChatbot:
    """Simple AI chatbot for booking assistance."""
    
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! How can I help you with your booking today?",
                "Welcome! I'm here to assist you with your hotel reservation.",
                "Hi there! What can I help you with regarding your stay?"
            ],
            "pricing": [
                "Our rooms start at $100 per night. Prices vary based on room type and dates.",
                "I'd be happy to help you find the best rate for your stay. When are you planning to visit?",
                "Room rates depend on your travel dates and room preference. Let me help you find options."
            ],
            "availability": [
                "I can check availability for you. What dates are you considering?",
                "Let me help you find available rooms for your preferred dates.",
                "I'll be happy to check room availability. Please provide your check-in and check-out dates."
            ],
            "amenities": [
                "Our hotel offers WiFi, parking, room service, and more. What specific amenities are you interested in?",
                "We have great facilities including a gym, restaurant, and business center. What would you like to know more about?",
                "Our amenities include complimentary breakfast, WiFi, and 24/7 front desk service."
            ],
            "cancellation": [
                "Our cancellation policy allows free cancellation up to 24 hours before check-in.",
                "You can cancel your booking without charge up to one day before arrival.",
                "Cancellations are free until 24 hours before your scheduled arrival."
            ],
            "default": [
                "I'm here to help with your booking. You can ask about pricing, availability, amenities, or policies.",
                "I can assist with room reservations, pricing information, and hotel amenities. How may I help?",
                "Please let me know what you'd like to know about your hotel stay."
            ]
        }
    
    def get_response(self, user_message: str) -> str:
        """
        Generate chatbot response based on user message.
        
        Args:
            user_message: User's input message
            
        Returns:
            Appropriate response string
        """
        message_lower = user_message.lower()
        
        # Simple keyword matching
        if any(word in message_lower for word in ["hello", "hi", "hey", "good morning", "good evening"]):
            return self.responses["greeting"][0]
        elif any(word in message_lower for word in ["price", "cost", "rate", "money", "expensive"]):
            return self.responses["pricing"][0]
        elif any(word in message_lower for word in ["available", "availability", "free", "book", "reserve"]):
            return self.responses["availability"][0]
        elif any(word in message_lower for word in ["amenities", "facilities", "wifi", "parking", "breakfast"]):
            return self.responses["amenities"][0]
        elif any(word in message_lower for word in ["cancel", "cancellation", "refund", "policy"]):
            return self.responses["cancellation"][0]
        else:
            return self.responses["default"][0]


class OccupancyPredictor:
    """Simple occupancy prediction model."""
    
    def predict_occupancy(self, date: datetime, historical_data: Optional[List] = None) -> Dict:
        """
        Predict hotel occupancy for a given date.
        
        Args:
            date: Target date for prediction
            historical_data: Optional historical occupancy data
            
        Returns:
            Dict with predicted occupancy and confidence
        """
        # Simple rule-based prediction (in real implementation, would use ML model)
        day_of_week = date.weekday()
        month = date.month
        
        # Base occupancy by day of week
        weekday_occupancy = {
            0: 0.65,  # Monday
            1: 0.70,  # Tuesday
            2: 0.75,  # Wednesday
            3: 0.80,  # Thursday
            4: 0.85,  # Friday
            5: 0.90,  # Saturday
            6: 0.75   # Sunday
        }
        
        # Seasonal adjustments
        seasonal_multiplier = {
            12: 1.2, 1: 1.1, 2: 0.9,  # Winter
            3: 1.0, 4: 1.1, 5: 1.2,   # Spring
            6: 1.3, 7: 1.4, 8: 1.3,   # Summer
            9: 1.1, 10: 1.0, 11: 0.9  # Fall
        }
        
        base_occupancy = weekday_occupancy[day_of_week]
        seasonal_adj = seasonal_multiplier[month]
        predicted_occupancy = min(0.95, base_occupancy * seasonal_adj)
        
        return {
            "predicted_occupancy": round(predicted_occupancy, 2),
            "confidence": 0.75,  # Mock confidence score
            "factors": {
                "day_of_week_effect": weekday_occupancy[day_of_week],
                "seasonal_effect": seasonal_adj,
                "day_name": date.strftime("%A")
            }
        }