from openai import OpenAI
import os
from datetime import datetime
import pandas as pd

class AIElfAnalyzer:
    def __init__(self):
        """Initialize the AI analyzer with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OpenAI API key not found in environment variables")

    def analyze_communications(self, messages, elf_name):
        """Analyze elf communications using OpenAI to detect suspicious patterns"""
        
        # Prepare the messages for analysis
        message_text = "\n".join(messages)
        
        # Create the prompt for OpenAI
        prompt = f"""Analyze these elf workshop communications for suspicious activity. 
        Consider signs of sabotage, conspiracy, or deviation from normal workshop operations.
        Communications to analyze:
        {message_text}
        
        Provide a JSON-structured analysis with these fields:
        - risk_level (0-10)
        - suspicious_patterns (list)
        - recommended_actions (list)
        - psychological_assessment (brief)"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a North Pole security analyst specializing in elf behavior analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                'analysis': response.choices[0].message.content,
                'timestamp': datetime.now().isoformat(),
                'elf_name': elf_name
            }
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return None

    def enhance_risk_assessment(self, basic_metrics, communications_analysis):
        """Combine traditional metrics with AI insights for enhanced risk assessment"""
        try:
            # Extract numerical risk score from AI analysis (assuming it's in the response)
            ai_risk_score = float(communications_analysis.get('risk_score', 5)) / 10
            
            # Weighted combination of traditional and AI risk metrics
            enhanced_risk = {
                'combined_risk_score': (
                    basic_metrics['average_suspicious_score'] * 0.4 +
                    ai_risk_score * 0.6
                ),
                'ai_insights': communications_analysis.get('suspicious_patterns', []),
                'recommended_actions': communications_analysis.get('recommended_actions', [])
            }
            
            # Determine final risk level
            if enhanced_risk['combined_risk_score'] > 0.7:
                enhanced_risk['risk_level'] = 'CRITICAL'
            elif enhanced_risk['combined_risk_score'] > 0.5:
                enhanced_risk['risk_level'] = 'HIGH'
            elif enhanced_risk['combined_risk_score'] > 0.3:
                enhanced_risk['risk_level'] = 'MEDIUM'
            else:
                enhanced_risk['risk_level'] = 'LOW'
                
            return enhanced_risk
            
        except Exception as e:
            print(f"Error in risk enhancement: {e}")
            return None

    def predict_future_behavior(self, elf_name, historical_data, recent_communications):
        """Use AI to predict potential future actions based on patterns"""
        
        # Prepare historical context
        historical_summary = (
            f"Tasks Completed: {historical_data.get('tasks_completed')}\n"
            f"Attendance Rate: {historical_data.get('attendance_rate')}\n"
            f"Recent Communications: {recent_communications[-3:]}"
        )
        
        prompt = f"""Based on this elf's historical behavior and recent communications,
        predict potential future actions and risk of sabotage.
        
        Historical Context:
        {historical_summary}
        
        Provide predictions for:
        1. Likely next actions
        2. Risk of sabotage in next 24 hours
        3. Recommended preventive measures
        
        Format as JSON with these fields:
        - predicted_actions (list)
        - sabotage_risk_24h (0-10)
        - preventive_measures (list)"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a predictive behavior analyst for North Pole Security."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                'prediction': response.choices[0].message.content,
                'timestamp': datetime.now().isoformat(),
                'elf_name': elf_name
            }
        except Exception as e:
            print(f"Error in behavior prediction: {e}")
            return None