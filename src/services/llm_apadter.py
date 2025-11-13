import openai
import json
from typing import List,Dict,Optional
from dataclasses import dataclass
import os
from datetime import datetime

@dataclass
class SocialNetworkPost:
    text: str
    hashtags: List[str]
    character :int 
    tone :str
    suggested_image_prompt: Optional[str] = None

class LLMAdapter:
    character_limit = {
        "facebook": 63206,
        "instagram": 2200,
        "linkedin": 3000,
        "tikTok": 2200,
        "whatsapp": 65536
    }
    
    temperature_config = {
        "facebook": 0.7,
        "instagram": 0.8,
        "linkedin": 0.6,
        "tikTok": 0.9,
        "whatsapp": 0.5
    }

    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)

    def get_system_prompt(self, network: str) -> str:
       prompts = {
            "facebook": """" Eres un experto en contenido para facebook.tu tarea es adaptar contenido para esta red social con estas caracteristicas
            -tono: amigable, conversacional, y atractivo.
            -longitud: maximo 500 caracteres.
            -emojis: usa entre 2 y 5 emojis por post
            -hashtags: usa entre 2 y 5 hashtags relevantes al contenido.
            -enfoque: fomenta la interacción 
            -formato: usa texto claro y salto de lineas para mejorar la legibilidad""",
            "instagram": """ Eres un experto en contenido para instagram.tu tarea es adaptar contenido para esta red social con estas caracteristicas
            -tono: creativo, visual y atractivo.
            -longitud: maximo 500 caracteres.
            -emojis: usa entre 5 y 10 emojis por post
            -hashtags: usa entre 10 y 15 hashtags relevantes al contenido.
            -enfoque: fomenta la interacción y el engagement.
            -formato: usa texto claro y salto de lineas para mejorar la legibilidad""",
            "linkedin": """ Eres un experto en contenido para linkedin.tu tarea es adaptar contenido para esta red social con estas caracteristicas 
            -tono: profesional, informativo y respetuoso.
            -longitud: maximo 500 caracteres.
            -emojis: usa entre 1 y 3 emojis por post
            -hashtags: usa entre 3 y 7 hashtags relevantes al contenido.
            -enfoque: fomenta la interacción profesional y el networking.
            -formato: usa texto claro y salto de lineas para mejorar la legibilidad""",
            "tikTok": """ Eres un experto en contenido para tikTok.tu tarea es adaptar contenido para esta red social con estas caracteristicas 
            -tono: divertido, enérgico y atractivo.
            -longitud: maximo 300 caracteres.
            -emojis: usa entre 5 y 10 emojis por post
            -hashtags: usa entre 5 y 10 hashtags relevantes al contenido.
            -enfoque: fomenta la interacción y el engagement.
            -formato: usa texto claro y salto de lineas para mejorar la legibilidad""",
            "whatsapp": """ Eres un experto en contenido para whatsapp.tu tarea es adaptar contenido para esta red social con estas caracteristicas 
            -tono: casual, cercano y directo.
            -longitud: maximo 700 caracteres.
            -emojis: usa entre 2 y 5 emojis por post
            -hashtags: usa entre 1 y 3 hashtags relevantes al contenido.
            -enfoque: fomenta la interacción y la cercania.
            -formato: usa texto claro y salto de lineas para mejorar la legibilidad""",
        }
       
       return prompts.get(network,prompts["facebook"])

    def get_use_prompt(self,title:str,content:str,network:str) -> str:
        return f""" Adapta el siguiente contenido para una publicacion en {network}:
        Titulo: {title}
        Contenido: {content}
        Genera solo un objeto Json con esta estructura exacta:
        {{
            "text": "Texto adaptado para la publicacion",
            "hashtags": ["hashtag1", "hashtag2", "..."],
            "character": numero_de_caracteres,
            "tone": "descripcion_del_tono"
            {
              "," if network == "instagram" 
                else ""
            } 
            {
                "suggested_image_prompt": "opcional: sugerencia de prompt para imagen relacionada"
                if network == "instagram" else ""
            }
        }}

        importante: 
        -El texto debe ser especifico para {network}
        -El texto no debe exceder el limite de  { self.character_limit[network] } caracteres.
        -El character_count debe ser exacto.
        -No agregues explicaciones adicionales solo el Json.
        """
    
        def adapt_content(self, title: str, content: str, network: str) -> Dict:
            try:
                system_prompt = self.get_system_prompt(network)
                user_prompt = self.get_use_prompt(title, content, network)
                temperature = self.temperature_config.get(network, 0.7)
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=800,
                )
                response_content = response.choices[0].message.content.strip()
                if response_text.startswith("```json"):
                    response_text = response_text.replace("```json", "").replace("```", "").strip()
                adapted_content = json.loads(response_text)
                if adapted_content["character_count"] > self.character_limit[network]:
                    raise ValueError(f"Generated content exceeds character limit for {network}.")
                
                adapted_content["network"] = network

                adapted_content["adapted_at"] = datetime.utcnow().isoformat()
                return adapted_content
            except Exception as e:
                raise Exception(f"Error adaptando contenido para {network}")
           
        def adapt_to_multiple_networks(self, title:str,content:str,target_networks:List[str]) -> Dict:
            results = {}
            errors = {}
            for network in target_networks:
                if network not in self.character_limit:
                    errors[network] = f"Red Social'{network}'no soportada."
                    continue
                try:
                    results[network] = self.adapt_content(title,content,network)
                except Exception as e:
                    errors[network] = str(e)
            
            suceessfull_adaptations=len([n for n in target_networks if n in results and not n.startswith("_")])
            return results
        
        def validate_input(data:Dict)->bool:
            required_fields=["title","content","target_networks"]
            for field in required_fields:
                if field not in data:
                    return False
            if not isinstance(data["target_networks"],list) or len(data["target_networks"])==0:
                return False
            if len(data["target_networks"])==0:
                return False
            return True
        

        


       


       