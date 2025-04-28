import logging
from flask import Flask, request, jsonify, Response, render_template
from requests.exceptions import RequestException
from ollama_client import OllamaClient

app = Flask(__name__)

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Ollama Client globally or per request (global is fine for this case)
ollama_client = OllamaClient()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/generate", methods=["GET", "POST"])
def generate():
    error_message = None
    code = None
    title = None
    submitted_prompt = None

    if request.method == "POST":
        submitted_prompt = request.form.get("prompt", "").strip()
        if not submitted_prompt:
            error_message = "Lütfen bir prompt girin."
            app.logger.warning("Generate called with empty prompt.") # Log warning
        else:
            try:
                app.logger.info(f"Calling Ollama client for prompt: {submitted_prompt[:50]}...")
                code, title = ollama_client.generate_code_and_summary(submitted_prompt)

                if not code and not title:
                   error_message = "Modelden geçerli bir kod veya başlık alınamadı. Lütfen promptunuzu kontrol edin veya tekrar deneyin."

            except RequestException as e:
                # Error is logged within the client now, just set the user message
                error_message = "Kod üretici servisine bağlanırken bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            except Exception as e:
                # Error is logged within the client now, just set the user message
                error_message = "Beklenmedik bir hata oluştu. Lütfen sistem yöneticisi ile iletişime geçin."

    return render_template(
        "index.html",
        code=code,
        title=title,
        error=error_message,
        submitted_prompt=submitted_prompt # Pass prompt back to template
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)

