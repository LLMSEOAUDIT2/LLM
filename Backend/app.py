from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
from utils import markdown_to_html  # Import the function from utils.py

app = Flask(__name__)

# Initialize Groq Client
api_key = "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"
client = Groq(api_key=api_key)

@app.route('/')
def index():
    # Serve the HTML file (for now, point to create-audit.html or your form file)
    return send_from_directory('./Frontend-master/audit', 'create-audit.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_metrics():
    # Get user input data
    data = request.json

    # Create the prompt for Groq
    prompt_lines = ["Explain the importance of the following SEO metrics and provide actionable recommendations for improvement:"]
    for metric, value in data.items():
        prompt_lines.append(f"{metric}: {value}")
    prompt = "\n".join(prompt_lines)

    try:
        # Send the prompt to the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an SEO expert assistant. Provide brief and actionable recommendations for each metric."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192",  
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False
        )

        # Get response from the model
        recommendation = chat_completion.choices[0].message.content.strip()

        # Format Markdown response to HTML using the imported function
        recommendation_html = markdown_to_html(recommendation)

        # Return the response as HTML to the frontend
        return jsonify({"recommendation": recommendation_html})

    except Exception as e:
        # Handle API errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
