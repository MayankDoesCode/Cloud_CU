from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# ---------------------------
# Translator API
# ---------------------------

translator_key = "Your Key"
translator_endpoint = ""
translator_region = ""

# ---------------------------
# Text Analytics API
# ---------------------------

language_key = "Your Key"
language_endpoint = "Your Endpoint"

@app.route("/", methods=["GET", "POST"])
def index():

    translated_text = ""
    sentiment = ""
    key_phrases = []
    detected_language = ""

    if request.method == "POST":

        text = request.form["text"]
        target_language = request.form["language"]

        # ---------------------------
        # TRANSLATION
        # ---------------------------

        translate_url = translator_endpoint + "/translate?api-version=3.0"

        params = {
            "to": target_language
        }

        headers = {
            "Ocp-Apim-Subscription-Key": translator_key,
            "Ocp-Apim-Subscription-Region": translator_region,
            "Content-type": "application/json"
        }

        body = [{
            "text": text
        }]

        response = requests.post(
            translate_url,
            params=params,
            headers=headers,
            json=body
        )

        translated_text = response.json()[0]["translations"][0]["text"]

        # ---------------------------
        # TEXT ANALYTICS
        # ---------------------------

        analytics_url = language_endpoint + "/language/:analyze-text?api-version=2023-04-01"

        headers = {
            "Ocp-Apim-Subscription-Key": language_key,
            "Content-Type": "application/json"
        }

        body = {
            "kind": "SentimentAnalysis",
            "analysisInput": {
                "documents": [
                    {
                        "id": "1",
                        "language": "en",
                        "text": text
                    }
                ]
            }
        }

        response = requests.post(
            analytics_url,
            headers=headers,
            json=body
        )

        result = response.json()

        sentiment = result["results"]["documents"][0]["sentiment"]

        # ---------------------------
        # KEY PHRASES
        # ---------------------------

        keyphrase_url = language_endpoint + "/language/:analyze-text?api-version=2023-04-01"

        body = {
            "kind": "KeyPhraseExtraction",
            "analysisInput": {
                "documents": [
                    {
                        "id": "1",
                        "language": "en",
                        "text": text
                    }
                ]
            }
        }

        response = requests.post(
            keyphrase_url,
            headers=headers,
            json=body
        )

        key_result = response.json()

        key_phrases = key_result["results"]["documents"][0]["keyPhrases"]

    return render_template(
        "index.html",
        translated_text=translated_text,
        sentiment=sentiment,
        key_phrases=key_phrases
    )

if __name__ == "__main__":
    app.run(debug=True)
