import requests
import certifi

from config import Config


class AIServiceError(Exception):
    pass


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY

    def _get_system_instruction(self):
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis):
        if not self.api_key:
            return "Demo modu: Groq API anahtarı bulunamadı."

        messages = [
            {
                "role": "system",
                "content": self._get_system_instruction()
            }
        ]

        messages.extend(gecmis)

        messages.append({
            "role": "user",
            "content": mesaj
        })

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": messages
                },
                verify=certifi.where()
            )

            if response.status_code != 200:
                raise AIServiceError(
                       f"AI servisi cevap vermedi. Durum: {response.status_code}, Detay: {response.text}"
    )

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            raise AIServiceError(f"AI servisi hatası: {e}")


ai_service = AIService()