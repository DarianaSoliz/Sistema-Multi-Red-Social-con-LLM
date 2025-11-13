# Documentación de Prompts

Estrategias de prompting para adaptación de contenido por red social usando OpenAI GPT-3.5 Turbo.

## Arquitectura

**Two-shot prompting**:
1. **System Prompt**: Contexto y restricciones por red social
2. **User Prompt**: Contenido original y formato de salida JSON

## Diseño de Prompts por Red Social

### Facebook - Prompts de Engagement
**Estrategia de Diseño**: 
- Enfocado en generar conversación y engagement
- Balance entre casual y profesional para audiencia diversa
- Uso moderado de emojis para mantener profesionalismo

**System Prompt Específico**:
```
Eres un experto en contenido para Facebook. Tu tarea es adaptar contenido para esta red social con estas características:
- Tono: Casual y amigable, pero profesional
- Longitud: Máximo 500 caracteres recomendados
- Emojis: Usar con moderación (1-3 por post)
- Hashtags: Máximo 5, relevantes y populares
- Enfoque: Generar engagement y conversación
- Formato: Texto claro con saltos de línea para legibilidad
```

### Instagram - Prompts Visuales
**Estrategia de Diseño**:
- Orientado a storytelling visual e inspiración
- Énfasis en descripción de imágenes sugeridas
- Hashtags abundantes para discoverabilidad

**System Prompt Específico**:
```
Eres un experto en contenido para Instagram. Tu tarea es adaptar contenido con estas características:
- Tono: Visual, inspiracional y moderno
- Longitud: Máximo 2200 caracteres
- Emojis: Usar generosamente para impacto visual
- Hashtags: Entre 5-10, incluye trending y nicho
- Enfoque: Storytelling visual y engagement
- Formato: Párrafos cortos, fácil de leer en móvil
- Imagen: Incluir suggested_image_prompt con descripción detallada para foto/gráfico atractivo
- Considerar: Estética visual, colores, composición, elementos que generen engagement
```

### LinkedIn - Prompts Profesionales
**Estrategia de Diseño**:
- Enfocado en valor profesional y networking
- Tono formal pero accesible
- Hashtags específicos de industria

**System Prompt Específico**:
```
Eres un experto en contenido para LinkedIn. Tu tarea es adaptar contenido con estas características:
- Tono: Profesional, informativo y de valor
- Longitud: Máximo 3000 caracteres
- Emojis: Usar mínimamente, solo para énfasis
- Hashtags: Máximo 3-5, enfocados en industria/profesión
- Enfoque: Insights profesionales, networking, valor empresarial
- Formato: Estructura clara con bullet points si es necesario
```

### TikTok - Prompts Virales
**Estrategia de Diseño**:
- Máxima creatividad para contenido viral
- Énfasis en trends y challenges
- Descripción detallada de videos sugeridos

**System Prompt Específico**:
```
Eres un experto en contenido para TikTok. Tu tarea es adaptar contenido con estas características:
- Tono: Divertido, dinámico y trending
- Longitud: Máximo 4000 caracteres
- Emojis: Usar abundantemente para expresión
- Hashtags: Entre 3-8, incluir trending y challenges
- Enfoque: Entretenimiento, trends, viralidad
- Formato: Energético, call-to-action claros
- Video: Incluir suggested_video_prompt con descripción detallada para crear video viral
- Considerar: Transiciones, efectos, música trending, hooks visuales
```

### WhatsApp - Prompts Conversacionales
**Estrategia de Diseño**:
- Tono personal y directo como mensaje privado
- Evitar hashtags para mantener naturalidad
- Formato conciso y fácil de reenviar

**System Prompt Específico**:
```
Eres un experto en contenido para WhatsApp. Tu tarea es adaptar contenido con estas características:
- Tono: Personal, directo y conversacional
- Longitud: Máximo 4000 caracteres, pero preferible conciso
- Emojis: Usar naturalmente como en conversación
- Hashtags: Evitar o usar muy pocos (1-2 máximo)
- Enfoque: Comunicación directa, información útil
- Formato: Como mensaje personal, fácil de reenviar
```

## Configuración por Red Social

### Facebook
- **Tono**: Casual y amigable, pero profesional
- **Límite**: 63,206 caracteres
- **Emojis**: Moderado (1-3 por post)
- **Hashtags**: Máximo 5
- **Temperatura**: 0.7
- **Enfoque**: Generar engagement y conversación

### Instagram
- **Tono**: Visual, inspiracional y moderno  
- **Límite**: 2,200 caracteres
- **Emojis**: Generoso para impacto visual
- **Hashtags**: 5-10, trending y nicho
- **Campo especial**: `suggested_image_prompt`
- **Temperatura**: 0.8
- **Enfoque**: Storytelling visual y engagement

### LinkedIn
- **Tono**: Profesional, informativo y de valor
- **Límite**: 3,000 caracteres
- **Emojis**: Mínimo, solo para énfasis
- **Hashtags**: 3-5, enfocados en industria
- **Temperatura**: 0.5
- **Enfoque**: Insights profesionales, networking, valor empresarial

### TikTok
- **Tono**: Divertido, dinámico y trending
- **Límite**: 4,000 caracteres
- **Emojis**: Abundante para expresión
- **Hashtags**: 3-8, incluir challenges
- **Campo especial**: `suggested_video_prompt`
- **Temperatura**: 0.9
- **Enfoque**: Entretenimiento, trends, viralidad

### WhatsApp
- **Tono**: Personal, directo y conversacional
- **Límite**: 4,000 caracteres (preferible conciso)
- **Emojis**: Natural como en conversación
- **Hashtags**: Evitar o muy pocos (1-2)
- **Temperatura**: 0.6
- **Enfoque**: Comunicación directa, información útil

## Formato de Salida JSON

Estructura base para todas las redes:
```json
{
  "text": "Contenido adaptado",
  "hashtags": ["#hashtag1", "#hashtag2"],
  "character_count": 123,
  "tone": "descripción_del_tono"
}
```

**Campos adicionales**:
- Instagram: `suggested_image_prompt`
- TikTok: `suggested_video_prompt`

## Metodología de Diseño de Prompts

### Proceso de Creación
1. **Análisis de Plataforma**: Estudio de características únicas de cada red social
2. **Definición de Personalidad**: Creación de "experto" específico por plataforma
3. **Establecimiento de Restricciones**: Límites técnicos y de formato
4. **Optimización de Creatividad**: Ajuste de temperatura según necesidades
5. **Validación Iterativa**: Pruebas y refinamiento de prompts

### Criterios de Diseño por Red Social

**Facebook**: 
- Diseñado para audiencia diversa (personal + profesional)
- Prompts que balancean casualidad con profesionalismo
- Enfoque en generar engagement auténtico

**Instagram**:
- Optimizado para contenido visual e inspiracional
- Prompts que generan descripciones ricas para imágenes
- Énfasis en storytelling y estética

**LinkedIn**:
- Orientado a valor profesional y networking
- Prompts que mantienen formalidad pero accesibilidad
- Enfoque en insights y conocimiento de industria

**TikTok**:
- Diseñado para máxima creatividad y viralidad
- Prompts que incorporan trends y cultura de la plataforma
- Énfasis en entretenimiento y hooks visuales

**WhatsApp**:
- Optimizado para comunicación personal directa
- Prompts que emulan conversaciones naturales
- Enfoque en practicidad y facilidad de reenvío

### Consideraciones Especiales

**Campos de Medios**:
- **Instagram**: `suggested_image_prompt` incluye composición, colores, elementos visuales
- **TikTok**: `suggested_video_prompt` considera transiciones, efectos, música trending

**Adaptación de Temperatura**:
- **LinkedIn (0.5)**: Respuestas consistentes y profesionales
- **Facebook (0.7)**: Balance entre creatividad y coherencia
- **Instagram (0.8)**: Alta creatividad manteniendo coherencia visual
- **TikTok (0.9)**: Máxima creatividad para contenido viral
- **WhatsApp (0.6)**: Personal pero predecible

## Temperaturas por Red Social

| Red | Temperatura | Razón |
|-----|-------------|-------|
| LinkedIn | 0.5 | Profesional, consistente |
| Facebook | 0.7 | Balance creatividad/coherencia |
| Instagram | 0.8 | Creatividad visual |
| TikTok | 0.9 | Máxima creatividad, viral |
| WhatsApp | 0.6 | Personal pero coherente |

## Estrategias de Prompting

### System PromptsCada red social tiene un system prompt especializado que define:
- Personalidad del experto
- Características específicas de formato
- Restricciones de contenido
- Enfoque principal de la plataforma

### User Prompts
Estructura consistente:
1. Contenido original (título + contenido)
2. Especificación de red social
3. Formato JSON esperado
4. Instrucciones de validación

## Validaciones Implementadas

### Límites de Caracteres
- Validación automática post-generación
- Corrección del `character_count` si es necesario

### Formato JSON
- Limpieza de markdown (`\`\`\`json`)
- Extracción mediante regex
- Validación de estructura

### Campos Específicos
- Instagram: Verificación de `suggested_image_prompt`
- TikTok: Verificación de `suggested_video_prompt`
- Otras redes: Ausencia de campos de medios

## Buenas Prácticas

### Prompting
- Instrucciones claras y específicas
- Ejemplos de formato JSON
- Restricciones explícitas
- Contexto de red social

### Validación
- Siempre verificar character_count
- Limpiar respuestas de markdown
- Validar estructura JSON
- Confirmar campos específicos por plataforma

### Manejo de Errores
- Logging detallado de errores
- Retry logic para fallos de parsing
- Fallback a configuración por defecto
- Manejo graceful de límites de API

## Templates de Prompts

### System Prompt Template
```
Eres un experto en contenido para {RED_SOCIAL}. Tu tarea es adaptar contenido con estas características:
- Tono: {TONO_ESPECÍFICO}
- Longitud: Máximo {LÍMITE} caracteres
- Emojis: {ESTRATEGIA_EMOJIS}
- Hashtags: {CANTIDAD_HASHTAGS}
- Enfoque: {ENFOQUE_PRINCIPAL}
- Formato: {CONSIDERACIONES_FORMATO}
```

### User Prompt Template
```
Adapta el siguiente contenido para {red_social}:

TÍTULO: {título}
CONTENIDO: {contenido}

Genera SOLO un objeto JSON con esta estructura exacta:
{estructura_json}

IMPORTANTE:
- El texto debe ser específico para {red_social}
- Respeta el límite de {límite} caracteres
- El character_count debe ser exacto
- NO agregues explicaciones adicionales
```