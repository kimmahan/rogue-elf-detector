# test_app.py
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Template folder: {app.template_folder}")
    print(f"Looking for template in: {os.path.join(app.template_folder, 'index.html')}")
    
    try:
        return render_template('index.html')
    except Exception as e:
        return f"""
        <pre>
        Debug Info:
        Current directory: {os.getcwd()}
        Template folder: {app.template_folder}
        Template exists: {os.path.exists(os.path.join(app.template_folder, 'index.html'))}
        Error: {str(e)}
        </pre>
        """

if __name__ == '__main__':
    app.run(debug=True)
    