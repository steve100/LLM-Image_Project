import os
import requests
import base64
import csv

from dotenv import load_dotenv
load_dotenv() ;

# === Configuration ===
#API_URL = "https://api.openai.com/v1/chat/completions"
API_URL = os.environ.get("API_URL_OPENAI")
API_KEY = os.environ.get("OPENAI_API_KEY")

#chose a model
MODEL_NAME = "gpt-4o"
IMAGE_FOLDER = "./images"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

TEXT_LOG = "captions_log.txt"
CSV_FILE = "captions_output.csv"

# === Encode image as base64 ===
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# === Create payload for OpenAI Vision model ===
def create_payload(encoded_image):
    return {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.7
    }

# === Main process ===
def process_images():
    results = []

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    with open(TEXT_LOG, "w", encoding="utf-8") as txt_log:
        txt_log.write("Image Caption Log\n==================\n\n")

        for filename in os.listdir(IMAGE_FOLDER):
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                image_path = os.path.join(IMAGE_FOLDER, filename)
                print(f"\n📷 Processing: {filename}")
                try:
                    encoded = encode_image(image_path)
                    payload = create_payload(encoded)
                    response = requests.post(API_URL, headers=headers, json=payload)

                    if response.status_code == 200:
                        caption = response.json()["choices"][0]["message"]["content"]
                        print(f"🧠 Caption: {caption}")
                        txt_log.write(f"{filename}:\n{caption}\n\n")
                        results.append((filename, caption))
                    else:
                        error_msg = f"API error ({response.status_code}): {response.text}"
                        print(f"❌ {error_msg}")
                        txt_log.write(f"{filename}:\nERROR: {error_msg}\n\n")
                        results.append((filename, f"ERROR: {error_msg}"))
                except Exception as e:
                    print(f"❌ Failed: {e}")
                    txt_log.write(f"{filename}:\nERROR: {e}\n\n")
                    results.append((filename, f"ERROR: {e}"))

    # Save to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Image Filename", "Caption"])
        for row in results:
            writer.writerow(row)

    print(f"\n✅ Captions saved to:\n- {TEXT_LOG}\n- {CSV_FILE}")

# === Run it ===
if __name__ == "__main__":
    process_images()
