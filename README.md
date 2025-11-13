# Sistema de Adaptación de Contenido con LLM

Sistema interactivo que adapta contenido original a múltiples redes sociales usando OpenAI GPT-3.5 Turbo. Genera versiones optimizadas para Facebook, Instagram, LinkedIn, TikTok y WhatsApp con características específicas por plataforma.

##  Características

- **Interfaz Interactiva**: Entrada amigable de título, contenido y selección de redes
- **Adaptación Inteligente**: Tono, longitud y estilo específicos por red social
- **Campos Especializados**: 
  - Instagram: `suggested_image_prompt` para imágenes
  - TikTok: `suggested_video_prompt` para videos
- **Validación Automática**: Límites de caracteres y formato JSON
- **Sistema de Pruebas**: Casos unificados para testing

##  Requisitos

- Python 3.8+
- Clave API de OpenAI
- Conexión a internet

##  Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd proy2
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
# Editar .env y agregar tu OPENAI_API_KEY
```

## Uso

### Sistema Principal

```bash
python src/services/llm_adapter.py

# Flujo:
# 1. Ingresa título
# 2. Ingresa contenido (Enter doble para terminar)  
# 3. Selecciona redes (números, nombres, o 'a' para todas)
# 4. Ve resultados
# 5. Opcionalmente guarda en JSON
```

### Sistema de Pruebas

```bash
# Ver casos disponibles
python tests/test_all_cases.py --list

# Ejecutar caso específico
python tests/test_all_cases.py --caso corporativo

# Ejecutar todos los casos
python tests/test_all_cases.py --all

# Modo interactivo
python tests/test_all_cases.py --interactive
```

### Uso Programático

```python
from src.services.llm_adapter import process_content

input_data = {
    "titulo": "Título del contenido",
    "contenido": "Contenido completo...",
    "target_networks": ["facebook", "instagram", "tiktok"]
}

results = process_content(input_data)
```

### Sistema de Pruebas Unificado

El sistema incluye 3 casos de prueba integrados:

```bash
# Ver casos disponibles
python tests/test_all_cases.py --list

# Ejecutar caso específico
python tests/test_all_cases.py --caso corporativo
python tests/test_all_cases.py --caso producto
python tests/test_all_cases.py --caso evento

# Ejecutar todos los casos
python tests/test_all_cases.py --all

# Modo interactivo de pruebas
python tests/test_all_cases.py --interactive
```

##  Formato de Entrada

```json
{
  "titulo": "Título del contenido",
  "contenido": "Contenido original completo...",
  "target_networks": ["facebook", "instagram", "linkedin", "tiktok", "whatsapp"]
}
```

##  Formato de Salida

```json
{
  "facebook": {
    "text": "🎉 Gran noticia para nuestra comunidad...",
    "hashtags": ["#Innovación", "#Tecnología"],
    "character_count": 245,
    "tone": "casual"
  },
  "instagram": {
    "text": "✨ Nueva función increíble...",
    "hashtags": ["#Tech", "#Innovation"],
    "character_count": 180,
    "tone": "inspirational",
    "suggested_image_prompt": "Modern tech interface with vibrant colors..."
  },
  "tiktok": {
    "text": "🔥 Esto va a cambiar todo...",
    "hashtags": ["#TechTok", "#Innovation"],
    "character_count": 120,
    "tone": "energetic",
    "suggested_video_prompt": "Dynamic video showing app features with trending music..."
  }
}
```

##  Configuración por Red Social

| Red Social | Tono | Límite | Hashtags | Temp | Campo Especial |
|------------|------|--------|----------|------|----------------|
| **Facebook** | Casual-profesional | 63,206 | 3-5 | 0.7 | - |
| **Instagram** | Visual-inspiracional | 2,200 | 5-10 | 0.8 | `suggested_image_prompt` |
| **LinkedIn** | Profesional | 3,000 | 3-5 | 0.5 | - |
| **TikTok** | Dinámico-viral | 4,000 | 3-8 | 0.9 | `suggested_video_prompt` |
| **WhatsApp** | Personal-directo | 4,000 | 1-2 | 0.6 | - |

##  Estructura del Proyecto

```
proy2/
├── src/services/
│   ├── llm_adapter.py        # Sistema principal
│   └── __init__.py
├── tests/
│   └── test_all_cases.py     # Sistema de pruebas unificado
├── docs/
│   ├── prompts.md
│   └── clase-02-desarrollo.md
├── requirements.txt
├── .env.example
└── README.md
```

##  Casos de Prueba

El sistema incluye 3 casos predefinidos en `test_all_cases.py`:

- **corporativo**: Milestone empresarial (10K clientes)
- **producto**: Lanzamiento SmartApp 2.0 con IA  
- **evento**: Conferencia TechFuture 2025

**Funcionalidades del sistema de pruebas**:
- Validación automática de campos específicos por plataforma
- Análisis de elementos clave por tipo de contenido
- Resumen detallado por red social
- Guardado automático de resultados con timestamp

##  Configuración Avanzada

### Variables de Entorno

```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo  # Opcional, por defecto gpt-3.5-turbo
LOG_LEVEL=INFO              # Opcional, por defecto INFO
```

### Personalización de Prompts

Los prompts se pueden personalizar editando el método `get_system_prompt()` en `src/services/llm_adapter.py`.

##  Desarrollo

### Agregar Nueva Red Social

1. Actualizar `CHARACTER_LIMITS` y `TEMPERATURE_CONFIG`
2. Crear prompt en `get_system_prompt()`
3. Si requiere campo especial, agregarlo en `get_user_prompt()`

### Ejecutar Tests

```bash
# Casos disponibles
python tests/test_all_cases.py --list

# Caso específico
python tests/test_all_cases.py --caso corporativo

# Todos los casos
python tests/test_all_cases.py --all

# Modo interactivo
python tests/test_all_cases.py --interactive
```

## Métricas y Logging

El sistema incluye logging detallado:

- Procesamiento por red social
- Tiempo de respuesta del LLM
- Errores y advertencias
- Validaciones de límites

##  Troubleshooting

### Error: "OPENAI_API_KEY not found"
```bash
export OPENAI_API_KEY=sk-your-key-here
# o agregar a .env
```

### Error: "Rate limit exceeded"
- Verificar límites de tu plan OpenAI
- Implementar retry con backoff exponencial

### Error: "JSON parsing failed"
- El LLM devolvió formato incorrecto
- Revisar prompts o aumentar max_tokens
