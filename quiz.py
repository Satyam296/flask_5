from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# Initialize Flask app
app = Flask(__name__)

GOOGLE_API_KEY = "AIzaSyB7rmrMrhCUgVQjJly7fzYv9ZplZFEmrWI"
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/questions')
def questions():
    # Check if the file exists
    if not os.path.exists("output.txt"):
        return jsonify({"error": "File output.txt not found."}), 404

    # Read content from the transcript file
    try:
        with open("output.txt", "r") as f:
            content = f.read()
    except Exception as e:
        return jsonify({"error": f"Error reading the file: {str(e)}"}), 500
    
    # Create a prompt for generating questions
    relevance_prompt = f"Tell me 10 questions related to this transcript for the better conceptual clarity of the students in multiple choice format. The transcript is {content}"
    
    # Generate content using Gemini model
    model = genai.GenerativeModel("gemini-pro")
    try:
        response = model.generate_content(relevance_prompt)
        generated_questions = response.text  # Attempt to access 'text' attribute
    except Exception as e:
        return jsonify({"error": f"Error generating questions: {str(e)}"}), 500
    
    # Return the response as a JSON with questions
    return jsonify({"questions": generated_questions})

def answers():
    with open("output.txt", "r") as f:
            content = f.read()
            ques = questions()["questions"]
            relevance_prompt = f"Tell me the answers {content}"
            
            # Generate content using Gemini model
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(relevance_prompt)
            generated_answers = response.text
            print(generated_answers)

if __name__ == "__main__":
    app.run(debug=True)



     