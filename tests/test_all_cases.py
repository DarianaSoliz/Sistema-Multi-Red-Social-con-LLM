import json
import os
import sys
from datetime import datetime

# Configurar rutas
project_root = os.path.dirname(os.path.dirname(__file__))
services_path = os.path.join(project_root, "src", "services")
sys.path.insert(0, services_path)

# Cargar variables de entorno
try:
    from dotenv import load_dotenv

    env_path = os.path.join(project_root, ".env")
    load_dotenv(env_path)
except ImportError:
    print("Warning: python-dotenv no instalado.")

from llm_apadter import process_content

CASOS_PRUEBA = {
    "corporativo": {
        "titulo": "Nuestra empresa alcanza los 10,000 clientes",
        "contenido": "Con gran orgullo anunciamos que nuestra empresa ha alcanzado la importante cifra de 10,000 clientes activos. Este milestone representa no solo nuestro crecimiento, sino también la confianza que nuestros usuarios depositan en nuestros servicios. Durante estos años hemos trabajado incansablemente para ofrecer soluciones innovadoras que realmente marquen la diferencia. Agradecemos a cada cliente que forma parte de esta increíble comunidad y reafirmamos nuestro compromiso de seguir mejorando día a día para brindar la mejor experiencia posible.",
        "target_networks": ["facebook", "instagram", "linkedin", "tiktok", "whatsapp"],
    },
    "producto": {
        "titulo": "Lanzamiento de SmartApp 2.0: Tu asistente personal inteligente",
        "contenido": "Hoy estamos emocionados de presentar SmartApp 2.0, una revolucionaria aplicación móvil que combina inteligencia artificial con diseño intuitivo. Las nuevas características incluyen: reconocimiento de voz avanzado, análisis predictivo personalizado, integración con más de 50 servicios populares, y una interfaz completamente rediseñada. SmartApp 2.0 aprende de tus hábitos y preferencias para ofrecerte sugerencias proactivas que realmente mejoran tu productividad. Disponible ahora en App Store y Google Play con una versión de prueba gratuita de 30 días.",
        "target_networks": ["facebook", "instagram", "linkedin", "tiktok", "whatsapp"],
    },
    "evento": {
        "titulo": "Conferencia TechFuture 2025: El futuro de la tecnología está aquí",
        "contenido": "Te invitamos a la conferencia más importante del año en tecnología: TechFuture 2025. Únete a más de 2,000 profesionales, emprendedores y líderes de la industria los días 15-17 de marzo en el Centro de Convenciones TechHub. Durante tres días intensivos exploraremos las últimas tendencias en IA, blockchain, sostenibilidad digital y el futuro del work. Contaremos con speakers internacionales de Google, Microsoft, Tesla y startups disruptivas. Incluye workshops prácticos, networking exclusivo y acceso a demos de tecnologías emergentes. Early bird hasta el 31 de enero con 40% de descuento.",
        "target_networks": ["facebook", "instagram", "linkedin", "tiktok", "whatsapp"],
    },
}


def mostrar_resumen_caso(caso_nombre, results):
    """Muestra resumen detallado de un caso específico"""
    caso = CASOS_PRUEBA[caso_nombre]

    print(f"\n📋 CASO: {caso_nombre.upper()}")
    print("=" * 60)
    print(f"📝 Título: {caso['titulo'][:50]}...")
    print("=" * 60)

    # Resumen por red social
    print(f"\n📊 RESUMEN POR RED SOCIAL:")
    for network, content in results.items():
        if not network.startswith("_"):
            char_count = content.get("character_count", "N/A")
            hashtags_count = len(content.get("hashtags", []))
            tone = content.get("tone", "N/A")

            print(f"\n🔹 {network.upper()}:")
            print(
                f"   📏 {char_count} caracteres | 🏷️  {hashtags_count} hashtags | 🎭 {tone}"
            )

            # Campos específicos por plataforma
            if network == "instagram" and "suggested_image_prompt" in content:
                image_prompt = (
                    content["suggested_image_prompt"][:70] + "..."
                    if len(content["suggested_image_prompt"]) > 70
                    else content["suggested_image_prompt"]
                )
                print(f"   📸 Imagen: {image_prompt}")

            elif network == "tiktok" and "suggested_video_prompt" in content:
                video_prompt = (
                    content["suggested_video_prompt"][:70] + "..."
                    if len(content["suggested_video_prompt"]) > 70
                    else content["suggested_video_prompt"]
                )
                print(f"   🎬 Video: {video_prompt}")

            # Mostrar algunos hashtags
            hashtags = content.get("hashtags", [])[:4]
            if hashtags:
                print(f"   🏷️  Tags: {', '.join(hashtags)}")


def validar_campos_especificos(results):
    print(f"\n🔍 VALIDACIÓN DE CAMPOS ESPECÍFICOS:")

    validaciones = []

    for network, content in results.items():
        if not network.startswith("_"):
            if network == "instagram":
                if "suggested_image_prompt" in content:
                    validaciones.append(
                        f"✅ Instagram: suggested_image_prompt incluido"
                    )
                else:
                    validaciones.append(f"❌ Instagram: falta suggested_image_prompt")

            elif network == "tiktok":
                if "suggested_video_prompt" in content:
                    validaciones.append(f"✅ TikTok: suggested_video_prompt incluido")
                else:
                    validaciones.append(f"❌ TikTok: falta suggested_video_prompt")

            elif network in ["facebook", "linkedin", "whatsapp"]:
                # Estas redes NO deben tener campos de medios
                has_media = (
                    "suggested_image_prompt" in content
                    or "suggested_video_prompt" in content
                )
                if not has_media:
                    validaciones.append(
                        f"✅ {network.capitalize()}: sin campos de medios (correcto)"
                    )
                else:
                    validaciones.append(
                        f"❌ {network.capitalize()}: tiene campos de medios no permitidos"
                    )

    for validacion in validaciones:
        print(f"  {validacion}")


def analizar_contenido_por_tipo(caso_nombre, results):
    """Análisis específico según el tipo de caso"""

    elementos_por_caso = {
        "corporativo": [
            "milestone",
            "clientes",
            "crecimiento",
            "comunidad",
            "compromiso",
        ],
        "producto": [
            "smartapp",
            "ia",
            "inteligencia artificial",
            "app store",
            "google play",
            "gratis",
            "30 días",
        ],
        "evento": [
            "techfuture",
            "conferencia",
            "marzo",
            "15-17",
            "registro",
            "early bird",
            "descuento",
        ],
    }

    elementos = elementos_por_caso.get(caso_nombre, [])

    if elementos:
        print(f"\n🔍 ANÁLISIS DE CONTENIDO:")
        print("✅ Elementos clave detectados por red:")

        for network, content in results.items():
            if not network.startswith("_"):
                text = content.get("text", "").lower()
                elementos_encontrados = [
                    elemento for elemento in elementos if elemento in text
                ]

                if elementos_encontrados:
                    print(
                        f"   {network.capitalize()}: {', '.join(elementos_encontrados)}"
                    )


def ejecutar_caso(caso_nombre):

    if caso_nombre not in CASOS_PRUEBA:
        print(f"❌ Caso '{caso_nombre}' no existe")
        return None

    caso = CASOS_PRUEBA[caso_nombre]

    print(f"\n🚀 EJECUTANDO CASO: {caso_nombre.upper()}")
    print("-" * 50)

    try:
        # Procesar directamente con los datos del caso
        results = process_content(caso)

        if results:
            print("✅ Procesamiento completado exitosamente")

            # Mostrar análisis completo
            mostrar_resumen_caso(caso_nombre, results)
            validar_campos_especificos(results)
            analizar_contenido_por_tipo(caso_nombre, results)

            # Guardar resultados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_{caso_nombre}_{timestamp}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"\n💾 Resultados guardados en: {filename}")
            return results

        else:
            print(f"❌ Error procesando caso {caso_nombre}")
            return None

    except Exception as e:
        print(f"❌ Error ejecutando {caso_nombre}: {e}")
        return None


def ejecutar_todos_los_casos():
    """Ejecuta todos los casos de prueba"""

    print("🎯 EJECUTANDO TODOS LOS CASOS DE PRUEBA")
    print("=" * 60)

    resultados_globales = {}
    casos_exitosos = 0
    casos_fallidos = 0

    for caso_nombre in CASOS_PRUEBA.keys():
        resultado = ejecutar_caso(caso_nombre)

        if resultado:
            resultados_globales[caso_nombre] = resultado
            casos_exitosos += 1
        else:
            casos_fallidos += 1

        print("\n" + "=" * 60)

    # Resumen final
    print(f"\n📈 RESUMEN FINAL DE EJECUCIÓN:")
    print(f"  ✅ Casos exitosos: {casos_exitosos}")
    print(f"  ❌ Casos fallidos: {casos_fallidos}")
    print(f"  📊 Total ejecutados: {casos_exitosos + casos_fallidos}")

    if resultados_globales:
        # Guardar resultados consolidados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_all_cases_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(resultados_globales, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Resultados consolidados guardados en: {filename}")

    return resultados_globales


def mostrar_casos_disponibles():
    """Muestra la lista de casos disponibles"""
    print("\n📋 CASOS DE PRUEBA DISPONIBLES:")
    print("-" * 40)

    for i, (caso_id, caso) in enumerate(CASOS_PRUEBA.items(), 1):
        print(f"{i}. {caso_id.upper()}")
        print(f"   📝 {caso['titulo'][:50]}...")
        print(f"   🎯 Redes: {len(caso['target_networks'])} plataformas")
        print()


def modo_interactivo():
    """Modo interactivo para seleccionar casos"""
    print("🎮 MODO INTERACTIVO - SELECCIÓN DE CASOS")
    print("=" * 50)

    mostrar_casos_disponibles()

    print("Opciones:")
    print("  • Ingresa el ID del caso (ej: corporativo)")
    print("  • Ingresa 'all' o 'todos' para ejecutar todos")
    print("  • Ingresa 'q' para salir")

    while True:
        seleccion = input("\n> ").strip().lower()

        if seleccion in ["q", "quit", "salir"]:
            print("👋 Saliendo...")
            return

        if seleccion in ["all", "todos", "todo"]:
            ejecutar_todos_los_casos()
            return

        if seleccion in CASOS_PRUEBA:
            ejecutar_caso(seleccion)
            return

        print(f"❌ Opción '{seleccion}' no válida. Intenta de nuevo.")
        print(f"   Casos disponibles: {', '.join(CASOS_PRUEBA.keys())}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Sistema de Pruebas Unificado - Adaptación LLM"
    )
    parser.add_argument(
        "--caso",
        "-c",
        choices=list(CASOS_PRUEBA.keys()),
        help="Ejecutar caso específico",
    )
    parser.add_argument(
        "--all", "-a", action="store_true", help="Ejecutar todos los casos"
    )
    parser.add_argument(
        "--list", "-l", action="store_true", help="Mostrar casos disponibles"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Modo interactivo"
    )

    args = parser.parse_args()

    # Verificar API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY no configurada")
        print("   Configura tu clave API en el archivo .env")
        sys.exit(1)

    print("🤖 SISTEMA DE PRUEBAS - ADAPTACIÓN DE CONTENIDO LLM")
    print("   TechFuture 2025 - Versión Optimizada")
    print("=" * 60)

    if args.list:
        mostrar_casos_disponibles()
    elif args.all:
        ejecutar_todos_los_casos()
    elif args.caso:
        ejecutar_caso(args.caso)
    elif args.interactive:
        modo_interactivo()
    else:
        # Por defecto: modo interactivo
        modo_interactivo()
