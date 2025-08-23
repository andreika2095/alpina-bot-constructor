import openai
from django.conf import settings
import json

class GPTService:
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        openai.api_key = self.api_key
    
    def generate_response(self, prompt, context=None, max_tokens=150):
        try:
            full_prompt = self._build_prompt(prompt, context)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты полезный ассистент для бизнес-обучения."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error in GPT API: {e}")
            return "Извините, произошла ошибка при обработке запроса."
    
    def _build_prompt(self, prompt, context):
        if context:
            context_str = json.dumps(context, ensure_ascii=False)
            return f"Контекст: {context_str}\n\nЗапрос: {prompt}"
        return prompt

gpt_service = GPTService()