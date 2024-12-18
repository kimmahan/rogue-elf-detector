from flask import Flask, jsonify, render_template
import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the absolute path to the templates directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
print(f"Template directory: {template_dir}")
print(f"Template exists: {os.path.exists(template_dir)}")
print(f"index.html exists: {os.path.exists(os.path.join(template_dir, 'index.html'))}")

# Initialize Flask with template directory
app = Flask(__name__, template_folder=template_dir)

class RogueElfDetector:
    def __init__(self):
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = current_dir.parent / 'data'
        self.load_data()
    
    def load_data(self):
        """Load data from CSV files"""
        try:
            self.behavior_logs = pd.read_csv(self.data_dir / 'Elf_Behavior_Logs.csv')
            self.communication_logs = pd.read_csv(self.data_dir / 'Elf_Communication_Logs.csv')
            self.schedule = pd.read_csv(self.data_dir / 'Elf_Schedule.csv')
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def analyze_elf(self, elf_name):
        """Analyze an individual elf's behavior"""
        # Get elf's behavior data
        elf_behavior = self.behavior_logs[self.behavior_logs['Elf_Name'] == elf_name].copy()
        if elf_behavior.empty:
            return {"error": f"No behavior data found for elf: {elf_name}"}

        # Calculate risk metrics
        risk_metrics = {
            'average_suspicious_score': elf_behavior['Suspicious_Activity_Score'].mean(),
            'tasks_completed': elf_behavior['Tasks_Completed'].mean(),
            'attendance_rate': elf_behavior['Shift_Attendance'].mean(),
            'materials_accessed': elf_behavior['Materials_Accessed'].mean()
        }

        # Get recent communications
        elf_comms = self.communication_logs[
            self.communication_logs['Elf_Name'] == elf_name
        ].sort_values('Time_Sent', ascending=False).head(5)

        # Get schedule information
        elf_schedule = self.schedule[self.schedule['Elf_Name'] == elf_name]

        return {
            'elf_name': elf_name,
            'risk_metrics': risk_metrics,
            'risk_level': self._calculate_risk_level(risk_metrics),
            'recent_communications': elf_comms['Message'].tolist(),
            'current_assignment': {
                'production_line': elf_schedule['Assigned_Production_Line'].iloc[0] if not elf_schedule.empty else None,
                'days_off': elf_schedule['Days_Off'].iloc[0] if not elf_schedule.empty else None
            },
            'timestamp': datetime.now().isoformat()
        }

    def _calculate_risk_level(self, metrics):
        """Calculate risk level based on metrics"""
        risk_score = (
            metrics['average_suspicious_score'] * 0.4 +
            (10 - metrics['tasks_completed']) * 0.2 +
            (10 - metrics['attendance_rate']) * 0.2 +
            (metrics['materials_accessed'] / 10) * 0.2
        )
        
        if risk_score > 0.7:
            return 'HIGH'
        elif risk_score > 0.4:
            return 'MEDIUM'
        return 'LOW'

    def get_workshop_summary(self):
        """Get overall workshop status"""
        total_elves = len(self.behavior_logs['Elf_Name'].unique())
        high_risk_elves = sum(
            1 for elf in self.behavior_logs['Elf_Name'].unique()
            if self.analyze_elf(elf)['risk_level'] == 'HIGH'
        )
        
        return {
            'total_elves': total_elves,
            'high_risk_count': high_risk_elves,
            'average_suspicious_score': self.behavior_logs['Suspicious_Activity_Score'].mean(),
            'status': 'COMPROMISED' if high_risk_elves/total_elves > 0.1 else 'STABLE'
        }

@app.route('/api/data-summary')
def get_data_summary():
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    data_dir = current_dir.parent / 'data'
    
    summaries = {}
    
    for file in data_dir.glob('*.csv'):
        df = pd.read_csv(file)
        summaries[file.name] = {
            'columns': df.columns.tolist(),
            'row_count': len(df),
            'sample': df.head(2).to_dict('records')
        }
    
    return jsonify(summaries)

@app.route('/api/analyze-elf/<elf_name>')
def analyze_elf(elf_name):
    detector = RogueElfDetector()
    return jsonify(detector.analyze_elf(elf_name))

@app.route('/api/workshop-status')
def workshop_status():
    detector = RogueElfDetector()
    return jsonify(detector.get_workshop_summary())

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <h1>Debug Info:</h1>
        <p>Error: {str(e)}</p>
        <p>Template folder: {template_dir}</p>
        <p>Templates exist: {os.path.exists(template_dir)}</p>
        <p>index.html exists: {os.path.exists(os.path.join(template_dir, 'index.html'))}</p>
        """

if __name__ == '__main__':
    app.run(debug=True)