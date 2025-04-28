import requests
import os
import re
import logging # Import logging

# Configure basic logging for this module if needed, or rely on Flask's
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OllamaClient:
    DEFAULT_API_URL = "http://localhost:11434/api/generate"
    DEFAULT_MODEL = "llama3"
    SYSTEM_PROMPT = (
        "Sen uzman bir Python geliştiricisisin. "
        "Kullanıcının verdiği isteğe uygun bir Python kodu üret. "
        "Önce kodu ÜÇ TIRNAK (```python\n...\n```) içinde ver. "
        "Sonra kısa bir başlık iki yıldız (**) içinde ver. "
        "Başlık en fazla 5 kelime olsun."
    )

    def __init__(self, api_url: str = None, model: str = None):
        self.api_url = api_url or os.getenv("OLLAMA_API_URL", self.DEFAULT_API_URL)
        self.model = model or self.DEFAULT_MODEL
        logger.info(f"OllamaClient initialized with API URL: {self.api_url} and Model: {self.model}")

    def _parse_response(self, response_text: str) -> tuple[str, str]:
        """Parses the raw response text from Ollama to extract code and title."""
        try:
            # Using re.DOTALL for code block to span multiple lines
            code_match = re.search(r"```python\n(.*?)\n```", response_text, re.DOTALL | re.IGNORECASE)
            # Searching for title enclosed in double asterisks
            title_match = re.search(r"\*\*(.*?)\*\*", response_text)

            code = code_match.group(1).strip() if code_match else ""
            title = title_match.group(1).strip() if title_match else ""

            if not code and not title:
                 logger.warning(f"Could not parse code or title from response: {response_text[:200]}...") # Log first 200 chars
            elif not code:
                 logger.warning(f"Could not parse code from response: {response_text[:200]}...")
            elif not title:
                 logger.warning(f"Could not parse title from response: {response_text[:200]}...")


            return code, title
        except Exception as e:
            logger.error(f"Error parsing Ollama response: {e}", exc_info=True)
            return "", "" # Return empty strings on parsing error


    def generate_code_and_summary(self, prompt: str, temperature: float = 0.2) -> tuple[str, str]:
        """Generates Python code and a title based on the user prompt."""
        full_prompt = self.SYSTEM_PROMPT + "\n\nKullanıcı İsteği:\n" + prompt

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "temperature": temperature,
            "stream": False
        }

        logger.info(f"Sending request to Ollama for prompt: {prompt[:50]}...")
        try:
            response = requests.post(self.api_url, json=payload, timeout=60) # Added timeout
            response.raise_for_status()

            data = response.json()
            raw_response = data.get("response", "")

            logger.info("Received successful response from Ollama.")
            code, title = self._parse_response(raw_response)
            return code, title

        except requests.exceptions.Timeout:
            logger.error(f"Request to Ollama timed out ({self.api_url})")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with Ollama API ({self.api_url}): {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during Ollama interaction: {e}", exc_info=True)
            raise

