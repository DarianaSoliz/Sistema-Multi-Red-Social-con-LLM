import openai
import json
import logging
import re
import os
import sys
from typing import Dict, List

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMAdapter:
    """Adaptador principal para generar contenido específico por red social"""

    # Límites de caracteres por red social
    CHARACTER_LIMITS = {
        "facebook": 63206,
        "instagram": 2200,
        "linkedin": 3000,
        "tiktok": 4000,
        "whatsapp": 4000,
    }

    # Configuraciones de temperatura por red social
    TEMPERATURE_CONFIG = {
        "facebook": 0.7,
        "instagram": 0.8,
        "linkedin": 0.5,
        "tiktok": 0.9,
        "whatsapp": 0.6,
    }

    def __init__(self, api_key: str):
        """Inicializa el adaptador LLM"""
        self.client = openai.OpenAI(api_key=api_key)
        logger.info("LLMAdapter inicializado correctamente")

    def get_system_prompt(self, network: str) -> str:
        """Obtiene el prompt del sistema específico para cada red social"""
        prompts = {
            "facebook": """
Eres un experto en contenido para Facebook. Tu tarea es adaptar contenido para esta red social con estas características:
- Tono: Casual y amigable, pero profesional
- Longitud: Máximo 500 caracteres recomendados
- Emojis: Usar con moderación (1-3 por post)
- Hashtags: Máximo 5, relevantes y populares
- Enfoque: Generar engagement y conversación
- Formato: Texto claro con saltos de línea para legibilidad
""",
            "instagram": """
Eres un experto en contenido para Instagram. Tu tarea es adaptar contenido con estas características:
- Tono: Visual, inspiracional y moderno
- Longitud: Máximo 2200 caracteres
- Emojis: Usar generosamente para impacto visual
- Hashtags: Entre 5-10, incluye trending y nicho
- Enfoque: Storytelling visual y engagement
- Formato: Párrafos cortos, fácil de leer en móvil
- Imagen: Incluir suggested_image_prompt con descripción detallada para foto/gráfico atractivo
- Considerar: Estética visual, colores, composición, elementos que generen engagement
""",
            "linkedin": """
Eres un experto en contenido para LinkedIn. Tu tarea es adaptar contenido con estas características:
- Tono: Profesional, informativo y de valor
- Longitud: Máximo 3000 caracteres
- Emojis: Usar mínimamente, solo para énfasis
- Hashtags: Máximo 3-5, enfocados en industria/profesión
- Enfoque: Insights profesionales, networking, valor empresarial
- Formato: Estructura clara con bullet points si es necesario
""",
            "tiktok": """
Eres un experto en contenido para TikTok. Tu tarea es adaptar contenido con estas características:
- Tono: Divertido, dinámico y trending
- Longitud: Máximo 4000 caracteres
- Emojis: Usar abundantemente para expresión
- Hashtags: Entre 3-8, incluir trending y challenges
- Enfoque: Entretenimiento, trends, viralidad
- Formato: Energético, call-to-action claros
- Video: Incluir suggested_video_prompt con descripción detallada para crear video viral
- Considerar: Transiciones, efectos, música trending, hooks visuales
""",
            "whatsapp": """
Eres un experto en contenido para WhatsApp. Tu tarea es adaptar contenido con estas características:
- Tono: Personal, directo y conversacional
- Longitud: Máximo 4000 caracteres, pero preferible conciso
- Emojis: Usar naturalmente como en conversación
- Hashtags: Evitar o usar muy pocos (1-2 máximo)
- Enfoque: Comunicación directa, información útil
- Formato: Como mensaje personal, fácil de reenviar
""",
        }
        return prompts.get(network, prompts["facebook"])

    def get_user_prompt(self, title: str, content: str, network: str) -> str:
        """Crea el prompt del usuario específico para la adaptación"""
        # Crear estructura JSON base
        json_structure = {
            "text": "texto adaptado aquí",
            "hashtags": ["#hashtag1", "#hashtag2"],
            "character_count": "número_de_caracteres",
            "tone": "descripción_del_tono",
        }

        # Agregar campos específicos por plataforma
        if network == "instagram":
            json_structure["suggested_image_prompt"] = (
                "descripción para imagen sugerida"
            )
        elif network == "tiktok":
            json_structure["suggested_video_prompt"] = "descripción para video sugerido"

        # Convertir a string JSON para mostrar en el prompt
        json_example = json.dumps(json_structure, indent=4, ensure_ascii=False)

        return f"""
Adapta el siguiente contenido para {network}:

TÍTULO: {title}
CONTENIDO: {content}

Genera SOLO un objeto JSON con esta estructura exacta:
{json_example}

IMPORTANTE:
- El texto debe ser específico para {network}
- Respeta el límite de {self.CHARACTER_LIMITS[network]} caracteres
- El character_count debe ser exacto (número entero)
- NO agregues explicaciones adicionales, solo el JSON
- Responde únicamente con el JSON válido
"""

    def adapt_content(self, title: str, content: str, network: str) -> Dict:
        """Adapta contenido para una red social específica"""
        try:
            logger.info(f"Adaptando contenido para {network}")

            system_prompt = self.get_system_prompt(network)
            user_prompt = self.get_user_prompt(title, content, network)
            temperature = self.TEMPERATURE_CONFIG.get(network, 0.7)

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=1000,
            )

            # Extraer y limpiar respuesta JSON
            response_text = response.choices[0].message.content.strip()

            # Limpiar markdown si existe
            if "```json" in response_text:
                start_idx = response_text.find("```json") + 7
                end_idx = response_text.find("```", start_idx)
                response_text = response_text[
                    start_idx : end_idx if end_idx != -1 else len(response_text)
                ].strip()
            elif "```" in response_text:
                start_idx = response_text.find("```") + 3
                end_idx = response_text.find("```", start_idx)
                response_text = response_text[
                    start_idx : end_idx if end_idx != -1 else len(response_text)
                ].strip()

            # Buscar JSON válido
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)

            adapted_content = json.loads(response_text)

            # Validar y corregir conteo de caracteres
            actual_char_count = len(adapted_content["text"])
            adapted_content["character_count"] = actual_char_count

            # Validar límite de caracteres
            if adapted_content["character_count"] > self.CHARACTER_LIMITS[network]:
                logger.warning(
                    f"Contenido excede límite para {network}: {adapted_content['character_count']}"
                )

            logger.info(f"Contenido adaptado exitosamente para {network}")
            return adapted_content

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response for {network}: {e}")
            raise Exception(f"Error parsing LLM response for {network}")

        except Exception as e:
            logger.error(f"Error adaptando contenido para {network}: {e}")
            raise Exception(f"Error en adaptación para {network}: {str(e)}")

    def adapt_to_multiple_networks(
        self, title: str, content: str, target_networks: List[str]
    ) -> Dict:
        """Adapta contenido para múltiples redes sociales"""
        results = {}
        errors = {}

        logger.info(f"Iniciando adaptación para {len(target_networks)} redes")

        for network in target_networks:
            if network not in self.CHARACTER_LIMITS:
                logger.warning(f"Red social no soportada: {network}")
                errors[network] = f"Red social '{network}' no está soportada"
                continue

            try:
                results[network] = self.adapt_content(title, content, network)
            except Exception as e:
                logger.error(f"Error adaptando para {network}: {e}")
                errors[network] = str(e)

        # Solo agregar errores si los hay, sin otros metadatos
        if errors:
            logger.error(f"Errores en adaptación: {errors}")

        successful_adaptations = len(
            [n for n in target_networks if n in results and not n.startswith("_")]
        )
        logger.info(
            f"Adaptación completada. Éxito: {successful_adaptations}, Errores: {len(errors)}"
        )
        return results


def validate_input(data: Dict) -> bool:
    """Valida que el input tenga la estructura correcta"""
    required_fields = ["titulo", "contenido", "target_networks"]

    for field in required_fields:
        if field not in data:
            logger.error(f"Campo requerido faltante: {field}")
            return False

    if not isinstance(data["target_networks"], list):
        logger.error("target_networks debe ser una lista")
        return False

    if len(data["target_networks"]) == 0:
        logger.error("target_networks no puede estar vacía")
        return False

    return True


def process_content(input_data: Dict) -> Dict:
    # Validar entrada
    if not validate_input(input_data):
        raise ValueError("Formato de entrada inválido")

    # Obtener clave API
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Se requiere OPENAI_API_KEY como variable de entorno")

    logger.info(f"Procesando contenido: '{input_data['titulo'][:50]}...'")

    # Inicializar adaptador
    adapter = LLMAdapter(api_key)

    # Procesar adaptación
    results = adapter.adapt_to_multiple_networks(
        title=input_data["titulo"],
        content=input_data["contenido"],
        target_networks=input_data["target_networks"],
    )

    return results


def interactive_input():
    """Permite entrada interactiva de datos"""
    print("=" * 60)
    print("📝 SISTEMA DE ADAPTACIÓN DE CONTENIDO - ENTRADA INTERACTIVA")
    print("=" * 60)

    # Solicitar título
    titulo = input("\n📌 Ingresa el título del contenido:\n> ").strip()

    # Solicitar contenido
    print("\n📄 Ingresa el contenido (presiona Enter dos veces para terminar):")
    contenido_lines = []
    print("> ", end="")
    while True:
        try:
            line = input()
            if line == "" and contenido_lines and contenido_lines[-1] == "":
                break
            contenido_lines.append(line)
            if line != "":
                print("> ", end="")
        except (EOFError, KeyboardInterrupt):
            break

    # Remover líneas vacías del final
    while contenido_lines and contenido_lines[-1] == "":
        contenido_lines.pop()

    contenido = "\n".join(contenido_lines).strip()

    # Solicitar redes sociales
    redes_validas = ["facebook", "instagram", "linkedin", "tiktok", "whatsapp"]
    print("\n🌐 SELECCIÓN DE REDES SOCIALES")
    print("-" * 40)
    print("Redes disponibles:")
    for i, red in enumerate(redes_validas, 1):
        print(f"  {i}. {red.capitalize()}")

    print("\nOpciones de selección:")
    print("  • Ingresa números separados por comas (ej: 1,3,5)")
    print("  • Ingresa nombres separados por comas (ej: facebook,instagram)")
    print("  • Presiona 'a' o Enter para seleccionar TODAS")
    print("  • Presiona 'q' para salir")

    while True:
        seleccion = input("\n> ").strip().lower()

        if seleccion in ["q", "quit", "salir"]:
            print("👋 Operación cancelada")
            sys.exit(0)

        if seleccion in ["a", "all", "todas", ""]:
            target_networks = redes_validas.copy()
            print(
                f"✅ Seleccionadas TODAS las redes: {', '.join([r.capitalize() for r in target_networks])}"
            )
            break

        # Intentar parsear como números
        if "," in seleccion or seleccion.isdigit():
            try:
                numeros = [int(num.strip()) for num in seleccion.split(",")]
                target_networks = []
                for num in numeros:
                    if 1 <= num <= len(redes_validas):
                        target_networks.append(redes_validas[num - 1])
                    else:
                        print(
                            f"❌ Número {num} no válido (debe ser entre 1 y {len(redes_validas)})"
                        )
                        target_networks = []
                        break

                if target_networks:
                    target_networks = list(set(target_networks))  # Eliminar duplicados
                    print(
                        f"✅ Seleccionadas: {', '.join([r.capitalize() for r in target_networks])}"
                    )
                    break
                else:
                    print("🔄 Intenta de nuevo...")
                    continue

            except ValueError:
                # Intentar parsear como nombres
                pass

        # Intentar parsear como nombres de redes
        nombres = [nombre.strip().lower() for nombre in seleccion.split(",")]
        target_networks = []
        nombres_invalidos = []

        for nombre in nombres:
            if nombre in redes_validas:
                target_networks.append(nombre)
            else:
                nombres_invalidos.append(nombre)

        if nombres_invalidos:
            print(f"❌ Redes no válidas: {', '.join(nombres_invalidos)}")
            print(f"   Redes válidas: {', '.join(redes_validas)}")
            continue

        if target_networks:
            target_networks = list(set(target_networks))  # Eliminar duplicados
            print(
                f"✅ Seleccionadas: {', '.join([r.capitalize() for r in target_networks])}"
            )
            break
        else:
            print("❌ No se seleccionaron redes válidas. Intenta de nuevo.")
            print("   Ejemplo: facebook,instagram o 1,2,3 o 'a' para todas")

    return {
        "titulo": titulo,
        "contenido": contenido,
        "target_networks": target_networks,
    }


def main():
    try:
        # Entrada interactiva de datos
        input_data = interactive_input()

        # Procesar contenido
        results = process_content(input_data)

        # Mostrar resultados
        print("\n" + "=" * 60)
        print("✅ RESULTADOS GENERADOS")
        print("=" * 60)
        print(json.dumps(results, indent=2, ensure_ascii=False))

        # Preguntar si desea guardar
        print("\n💾 ¿Deseas guardar los resultados en un archivo? (s/N)")
        guardar = input("> ").strip().lower()

        if guardar in ["s", "si", "sí", "yes", "y"]:
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resultados_adaptacion_{timestamp}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"✅ Resultados guardados en: {filename}")
        else:
            print("📋 Resultados mostrados únicamente en pantalla")

    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error en ejecución: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
