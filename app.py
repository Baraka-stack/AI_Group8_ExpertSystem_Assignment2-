from flask import Flask, render_template, request, jsonify
from scholarship_advisor import ScholarshipExpertSystem
import os

app = Flask(__name__, 
    static_folder='static',    # Explicitly set static folder
    static_url_path='/static'  # Explicitly set static URL path
)

expert_system = ScholarshipExpertSystem()

# Debug configurations
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

# Print paths for debugging
print("Static folder:", app.static_folder)
print("Template folder:", app.template_folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.form
        expert_system.facts = {
            'gpa': float(data['gpa']),
            'family_income': float(data['family_income']),
            'extracurricular_activities': data.get('extracurricular') == 'true',
            'sports_achievement': data.get('sports') == 'true',
            'leadership_role': data.get('leadership') == 'true',
            'community_service': float(data['community_hours'])
        }
        
        conclusions, rules_fired = expert_system.infer()
        return jsonify({
            'conclusions': conclusions,
            'rules_fired': rules_fired,
            'facts': expert_system.facts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
