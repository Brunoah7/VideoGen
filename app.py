from flask import Flask, request, render_template, send_file
import subprocess
import os
from groq import Groq

app = Flask(__name__)

# Set a folder to store uploaded files temporarily
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = Groq(api_key="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")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

client = Groq(api_key="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")

def generate_ai_text(prompt):
    print(f"User Prompt: {prompt}")  # Debugging line
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "Generate the text of whatever the user requests, however, don't do anything else like talk like a chatbot or enclose their requested thing in quotations, simply follow their prompt and output that request ONLY. **NEW RESPONSE EVERY TIME**"
            },
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )
    result = completion.choices[0].message.content.strip()
    print(f"Generated Text: {result}")  # Debugging line
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image_url = request.form["pic_url"]
        user_prompt = request.form["user_prompt"]
        

        ai_generated_text = generate_ai_text(user_prompt)
        video_length = request.form["video_length"]
        fade_length = request.form["fade_length"]
        final_opacity = request.form["final_opacity"]
        

        # Get the uploaded audio file
        audio_file = request.files["audio_file"]
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(audio_path)

        # Call the video generation script and pass the URL and audio file path
        output_video_path="output.mp4"
        subprocess.run([
            "python", "auto_video.py",
            image_url,  # Directly pass pic_url
            audio_path,  # Directly pass audio_path
            ai_generated_text,  # Directly pass ai_generated_text
            video_length,
            fade_length,
            final_opacity
    ])

        # Clean up the uploaded audio file after generating the video
        os.remove(audio_path)

        return send_file("DeepVideo.mp4", as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

#Please provide a profound and thought-provoking quote that reflects on themes of resilience, personal growth, and the human experience. The quote should be in the format: 'When bro said, "[your quote here]