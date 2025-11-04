# MCP/mcp_server_bosque.py

from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# Inicializa el servidor
mcp = FastMCP("servidor_bosque")

# Fuentes fijas
FUENTES = {
    "pot": "https://bogota.gov.co/bog/pot-2022-2035/",
    "biomimética": "https://asknature.org/",
    "suelo": "https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2019.02872/full",
    "briofitas": "https://stri.si.edu/es/noticia/briofitas",
}

def log_uso(fuente, tipo):
    """Guarda registro de cada fuente usada."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Usando {tipo}: {fuente}", flush=True)

@mcp.tool()
def leer_pagina(url: str) -> str:
    """Lee y devuelve texto de una página web."""
    log_uso(url, "página web")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return text[:4000]

@mcp.tool()
def explorar_pdf(tema: str) -> str:
    """
    Explora temas relacionados con filosofía de la biología, simbiosis,
    concepto de individuo y asociaciones.
    """
    tema = tema.lower().strip()

    # Respuestas predefinidas sobre temas filosóficos
    respuestas = {
        "filosofia_fungi": """
📄 Tema: Filosofía de los hongos

Resumen: Los hongos desafían nuestra noción tradicional de individualidad.
No son ni plantas ni animales, sino una forma de vida que cuestiona los límites
entre organismos. Un hongo puede extenderse por kilómetros como un solo organismo,
o puede existir en simbiosis con las raíces de los árboles.

Preguntas reflexivas:
- ¿Dónde termina un individuo y comienza otro en un bosque interconectado por redes fúngicas?
- ¿Qué significa ser un "individuo" si tu supervivencia depende completamente de otros organismos?
- ¿Podemos aplicar conceptos de cooperación fúngica a nuestras propias sociedades humanas?
        """,
        "margullis": """
📄 Tema: Teoría de la endosimbiosis de Lynn Margulis

Resumen: Margulis propuso que las células eucariotas se originaron por simbiosis entre
diferentes organismos procarióticos. Las mitocondrias y cloroplastos fueron alguna vez
bacterias independientes. Esto implica que la cooperación, no solo la competencia,
es fundamental para la evolución.

Preguntas reflexivas:
- Si nuestras células son el resultado de antiguas simbiosis, ¿somos realmente individuos o ecosistemas ambulantes?
- ¿Qué papel juega la cooperación en la evolución de la vida compleja?
- ¿Cómo cambia nuestra relación con la naturaleza si reconocemos que llevamos otros organismos dentro de nosotros?
        """,
        "hongo_planta": """
📄 Tema: Simbiosis entre hongos y plantas

Resumen: Las micorrizas son asociaciones simbióticas entre hongos y raíces de plantas.
El hongo ayuda a la planta a absorber nutrientes del suelo, mientras la planta
proporciona carbohidratos al hongo. Esta relación es tan antigua y fundamental
que permitió a las plantas colonizar la tierra hace 450 millones de años.

Preguntas reflexivas:
- ¿Dónde está el límite entre el hongo y la planta en una micorriza?
- ¿Pueden existir identidades separadas cuando dos organismos son completamente interdependientes?
- ¿Qué nos enseña la micorriza sobre las relaciones humanas y la interdependencia?
        """,
        "donna": """
📄 Tema: Pensamiento multiespecie (Donna Haraway)

Resumen: Haraway propone que debemos pensar más allá del antropocentrismo y
reconocer que vivimos en un mundo de "compañeros de especies". Los humanos no están
separados de la naturaleza, sino que somos parte de una red de relaciones con otros seres.

Preguntas reflexivas:
- ¿Cómo cambia nuestra percepción del mundo si nos vemos como parte de una red multiespecie?
- ¿Qué responsabilidades tenemos hacia otros seres con los que compartimos el planeta?
- ¿Puede el concepto de "individuo humano" sostenerse cuando dependemos de billones de microbios?
        """
    }

    if tema in respuestas:
        return respuestas[tema]
    else:
        return f"No se encontró información específica sobre '{tema}'. Temas disponibles: {', '.join(respuestas.keys())}"

@mcp.tool()
def explorar(tema: str) -> str:
    """
    Busca información sobre un tema combinando fuentes web.
    """
    tema = tema.lower().strip()
    respuesta = ""

    # Buscar fuente web
    for clave, link in FUENTES.items():
        if clave in tema:
            log_uso(link, "fuente web")
            try:
                resp = requests.get(link, timeout=10)
                soup = BeautifulSoup(resp.text, "html.parser")
                text = soup.get_text(separator="\n", strip=True)
                resumen = text[:1500]
                respuesta += f"🌐 Fuente web: {link}\n\n{resumen}\n\n"
            except Exception as e:
                respuesta += f"⚠️ Error al acceder a {link}: {str(e)}\n\n"

    if not respuesta.strip():
        respuesta = f"No encontré información registrada para el tema '{tema}'."

    return respuesta

@mcp.tool()
def inferir_especies(descripcion: str) -> str:
    """
    Analiza las condiciones descritas por el usuario (temperatura, humedad, luz, suelo, sonido etc.)
    y sugiere grupos de organismos que podrían estar activos o visibles.
    Ejemplo de entrada:
    "Hace frío, pero hay mucha luz y el suelo está seco."
    """

    descripcion = descripcion.lower()

    # Diccionarios de palabras clave
    condiciones = {
        "temperatura": {
            "frío": "baja",
            "helado": "baja",
            "calor": "alta",
            "cálido": "alta",
            "templado": "media"
        },
        "humedad": {
            "húmedo": "alta",
            "mojado": "alta",
            "charcos": "alta",
            "llovido": "alta",
            "rocío":"media",
            "seco": "baja",
            "árido": "baja"
        },
        "luz": {
            "mucha luz": "alta",
            "soleado": "alta",
            "nublado":"medio",
            "oscuro": "baja",
            "sombra": "baja",
            "noche": "baja"
        },
        "sonido": {
            "mucha ruido": "alta",
            "tránsito": "alta",
            "silencio": "baja",
            "pasos": "baja",
        }
    }

    # Interpretar condiciones
    interpretacion = {"temperatura": None, "humedad": None, "luz": None, "sonido": None}

    for cat, palabras in condiciones.items():
        for palabra, nivel in palabras.items():
            if palabra in descripcion:
                interpretacion[cat] = nivel

    # Reglas ecológicas simples
    posibles = []

    if interpretacion["luz"] == "alta":
        posibles.append("Araneidae - arañas de telas orbiculares, pone sus telas en sitios luminosos")
        posibles.append("Micrathena bogota - araña espinosa")
        posibles.append("Chrysomelidae - escarabajos de las hojas")
        posibles.append("Ichneumonidae - avispas parasitoides")
        posibles.append("Syrphidae - moscas de las flores")
        posibles.append("Bombus hortulanus - abejorro")
        posibles.append("Eurema - mariposas amarillas")
        posibles.append("Cladonia -Líquen")
        posibles.append("Lecanora caesiorubella -Líquen")
        posibles.append("Flavopunctelia flaventior -Líquen")
        posibles.append("Teloschistes exilis -Líquen")
        posibles.append("Taraxacum officinale - diente de león")
        posibles.append("Trifolium repens - trébol blanco")
        posibles.append("Trébol morado")

    if interpretacion["humedad"] == "alta":
        posibles.append("Aphididae (áfidos)")
        posibles.append("Ascalapha odorata (polilla bruja)")
        posibles.append("Sphagnum, Fissidens, Campylopus, Plagiochila, Plagiochila,Metzgeria - musgo")
        posibles.append("Usnea - Líquen")
        posibles.append("Cora - Líquen")
        posibles.append(" Pseudomonas - Bacterias del suelo")
        posibles.append("Pedomicrobium - Bacterias del suelo")
        posibles.append("Coprinellus - Hongo")
        posibles.append("Lactarius - Hongo")

    if interpretacion["temperatura"] == "alta":
        posibles.append("Chrysomelidae (escarabajos de las hojas)")
        posibles.append("Bombus hortulanus (abejorro)")
        posibles.append("Eurema (mariposas amarillas)")
        posibles.append("Taraxacum officinale (diente de león)")

    if interpretacion["luz"] == "media":
        posibles.append("Aphididae (áfidos)")
        posibles.append("Curculionidae (escarabajos picudos)")
        posibles.append("Compsus canescens (gorgojos)")
        posibles.append("Eurema (mariposas amarillas)")
        posibles.append("Campylopus  musgo")
        posibles.append("Sphagnum musgo")
        posibles.append("Cora liquen")
        posibles.append("Ganoderma")
        posibles.append("Lactarius")

    if interpretacion["humedad"] == "media":
        posibles.append("Chrysomelidae (escarabajos de las hojas)")
        posibles.append("Curculionidae (escarabajos picudos)")
        posibles.append("Ichneumonidae (avispas parasitoides)")
        posibles.append("Syrphidae (moscas de las flores)")
        posibles.append("Compsus canescens (gorgojos)")
        posibles.append("Bombus hortulanus (abejorro)")
        posibles.append("Eurema (mariposas amarillas)")
        posibles.append("Cladonia Líquen")
        posibles.append("Lecanora caesiorubella Líquen")
        posibles.append("Flavopunctelia flaventiorLíquen")
        posibles.append("Teloschistes exilis Líquen")
        posibles.append("Glomus (hongos micorrízicos)")
        posibles.append("Acaulospora (micorrízico)")
        posibles.append("Ganoderma Hongos")
        posibles.append("Phellinus Hongos")
        posibles.append("Taraxacum officinale (diente de león)")
        posibles.append("Trifolium repens (trébol blanco)")
        posibles.append("Trébol morado")

    if interpretacion["temperatura"] == "media":
        posibles.append("Aphididae (áfidos)")
        posibles.append("Curculionidae (escarabajos picudos)")
        posibles.append("Ichneumonidae (avispas parasitoides)")
        posibles.append("Syrphidae (moscas de las flores)")
        posibles.append("Ascalapha odorata (polilla bruja)")
        posibles.append("Compsus canescens (gorgojos)")
        posibles.append("Cora Líquenes")
        posibles.append("Usnea Líquenes")
        posibles.append("Cladonia Líquenes")
        posibles.append("Lecanora caesiorubella Líquenes")
        posibles.append("Flavopunctelia flaventior Líquenes")
        posibles.append("Teloschistes exilisLíquenes")
        posibles.append("Pseudomonas - Bacteria")
        posibles.append("Acinetobacter Bacteria")
        posibles.append("Pedomicrobium Bacteria")
        posibles.append("Glomus (hongos micorrízicos)")
        posibles.append("Acaulospora (micorrízico)")
        posibles.append("Coprinellus Hongos")
        posibles.append("Ganoderma Hongos")
        posibles.append("Lactarius Hongos")
        posibles.append("Phellinus Hongos")
        posibles.append("Trifolium repens (trébol blanco)")
        posibles.append("Trébol morado")

    if interpretacion["luz"] == "baja":
        posibles.append("Sclerosomatidae (opiliones)")
        posibles.append("Ascalapha odorata (polilla bruja)")
        posibles.append("Fissidens Briófita")
        posibles.append("Plagiochila Briófita")
        posibles.append("Metzgeria Briófita")
        posibles.append("Glomus (hongos micorrízicos)")
        posibles.append("Acaulospora (micorrízico)")
        posibles.append("Coprinellus Hongos")
        posibles.append("Phellinus Hongos")

    if interpretacion["sonido"] == "baja":
        posibles.append("Ascalapha odorata (polilla bruja) - Sensible a sonidos fuertes ")

    if interpretacion["temperatura"] == "baja":
        posibles.append(" Campylopus Briofitas")
        posibles.append("Fissidens Briofitas")
        posibles.append("Sphagnum Briofitas")
        posibles.append("Plagiochila Briofitas")
        posibles.append("Metzgeria Briofitas")

    # Redacción
    if posibles:
        salida = (
            "Basado en tu descripción, es posible que observes:\n\n- "
            + "\n- ".join(posibles)
            + "\n\nCada uno responde de manera distinta a las condiciones ambientales descritas."
        )
    else:
        salida = "No pude inferir condiciones claras a partir de tu descripción."

    return salida

# CRÍTICO: Cambiar el if __name__ == "__main__" por esto
if __name__ == "__main__":
    import sys
    import asyncio

    # Usar el método correcto para ejecutar el servidor
    asyncio.run(mcp.run())
