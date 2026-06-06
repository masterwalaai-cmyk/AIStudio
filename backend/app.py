from flask import Flask, render_template, request
from duckduckgo_search import DDGS
import google.genai as genai

app = app = Flask(
    __name__,
    template_folder="../templates"
)

genai_client = genai.Client(
    api_key=""
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]
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
        prompt = message[5:].replace(" ", "%20")
        image_url = "https://image.pollinations.ai/prompt/" + prompt

        return {
            "reply": image_url
        }

    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents="You are Taaha, a smart, friendly, and helpful AI assistant. User: " + message
    )

    return {
        "reply": response.text
    }


app.run(host="0.0.0.0", port=5000)
