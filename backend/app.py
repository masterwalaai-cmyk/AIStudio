from flask import Flask, render_template, request
from duckduckgo_search import DDGS
import google.genai as genai
from dotenv import load_dotenv
import os
import time

app = Flask(
    __name__,
    template_folder="../templates"
)

load_dotenv()

genai_client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]
    chat_history.append("User: " + message) 

    if message.lower().startswith("search "):
        query = message[7:]
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        reply = ""
        for r in results:
            reply += f"• {r['title']}\n{r['href']}\n\n"

            return {
                "reply": reply
        }
        if message.lower().startswith("draw "):
            prompt = message[5:].strip().replace(" ", "%20")
            image_url = f"https://image.pollinations.ai/prompt/{prompt}?seed={int(time.time())}&width=1024&height=1024&nologo=true"

            print(image_url)

            return {
               "reply": image_url
            }

        prompt_context = "\n".join(chat_history) + "\nUser: " + message

        contents = f"""
    You are Taaha, a friendly AI assistant.

    Your identity:
    - Your name is Taaha.
    - You are an AI assistant application created by Taaha.

    If users ask about this application:
    - Who created this app?
    - Who built this app?
    - Who made this app?
    - Who developed this app?

    Answer:
    "This AI assistant application was created and developed by Taaha."

    If users ask about the underlying AI model or technology, be truthful and say you use Google's Gemini AI model.

    Keep answers short and natural.
    """ + "\n" + prompt_context

        try:
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash",
             contents=contents
            )

        return {
            "reply": response.text
        }

    except Exception as e:
        print(e)
        return {
            "reply": str(e)
        }


app.run(host="0.0.0.0", port=5000)
