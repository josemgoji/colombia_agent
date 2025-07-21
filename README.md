# Colombia Agent - RAG con LangChain, FastAPI y Docker

Este proyecto implementa un agente RAG (Retrieval-Augmented Generation) capaz de responder preguntas **solo sobre Colombia**, utilizando contenido extraído de su página oficial de Wikipedia.

## ✅ Funcionalidades

- Extrae y limpia el texto de la URL de Wikipedia
- Fragmenta el texto (chunking) para su procesamiento
- Genera embeddings con modelos open source
- Crea una base vectorial usando **ChromaDB**
- Implementa un pipeline **RAG** con LangChain
- Usa un **prompt personalizado** para evitar respuestas fuera de contexto
- Expone una API REST con **FastAPI**
- Se despliega fácilmente con **Docker**

---

## 🧱 Estructura del proyecto

```bash
colombia_agent/
│
├── .env                   # Variables de entorno locales (no subir)
├── .env.example           # Ejemplo sin datos sensibles
├── .gitignore             # Ignora .env, __pycache__, /data, etc.
├── Dockerfile             # Instrucciones para Docker
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
│
├── data/                  # Almacena la base vectorial
│
├── src/
│   ├── agent/             # Clase principal del agente
│   ├── api/               # FastAPI y rutas
│   ├── config/            # Variables de entorno y constantes
│   ├── prompts/           # Plantilla base del LLM
│   └── rag/               # Flujo de RAG: scraping, chunks, embeddings, retriever
│
├── tests/                 # Tests unitarios con pytest
```

---

## 🔄 Flujo del agente

El agente sigue un pipeline completo de RAG (Retrieval-Augmented Generation) para responder preguntas sobre Colombia. A continuación, se describe cada etapa con los módulos implicados:

1. **Extracción de información (Scraping)**
   - 🧩 Módulo: `src/rag/wikipedia_scraper.py`
   - Se descarga el contenido de la página de Wikipedia sobre Colombia usando `requests` y `BeautifulSoup`.
   - Se limpia el HTML eliminando referencias, tablas y enlaces no útiles.

2. **Fragmentación del texto (Chunking)**
   - 🧩 Módulo: `src/rag/text_chunker.py`
   - El texto limpio se divide en fragmentos o "chunks" con un tamaño configurable.
   - Esto permite manejar el texto de forma eficiente para el embedding y la recuperación.

3. **Embeddings y base vectorial**
   - 🧩 Módulo: `src/rag/data_preparator.py`
   - Se generan embeddings a partir de los chunks usando modelos open source de Hugging Face.
   - Se guarda en una base vectorial local con **ChromaDB** (`data/chroma/`).

4. **Creación y uso del Retriever**
   - 🧩 Módulo: `src/rag/retriever_factory.py`
   - Si la base vectorial no existe, se genera automáticamente usando `DataPreparator`.
   - Se configura un `retriever` que buscará los chunks más relevantes para cada pregunta.

5. **Consulta del agente**
   - 🧩 Módulo: `src/agent/wiki_agent.py`
   - El agente `WikiAgent` recibe una pregunta y consulta al `retriever`.
   - Utiliza un prompt definido en `src/prompts/template.txt` para generar una respuesta precisa y restringida a temas sobre Colombia.
   - Si la pregunta no está relacionada con Colombia o no se encuentra en la información cargada, el agente responde que no puede contestar.

---

## ⚙️ Tecnologías usadas

| Tecnología      | Propósito                             |
|----------------|----------------------------------------|
| LangChain       | Orquestación RAG                      |
| HuggingFace     | Embeddings + LLMs                     |
| ChromaDB        | Almacenamiento vectorial              |
| FastAPI         | Servidor de la API                    |
| Docker          | Despliegue contenedorizado            |
| BeautifulSoup   | Scraping de Wikipedia                 |
| Pydantic        | Configuración por entorno             |

---

## 🚀 Cómo correr el proyecto

### 1. Clonar y crear entorno

```bash
git clone https://github.com/tu_usuario/colombia_agent.git
cd colombia_agent
python -m venv .venv
source .venv/bin/activate  # O .\.venv\Scriptsctivate en Windows
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia `.env.example` y renómbralo como `.env`, luego completa los valores:

```env
WIKIPEDIA_URL='https://es.wikipedia.org/wiki/Colombia'
CHROMA_DB_PATH="data/chroma"
HF_TOKEN=hf_XXXXXXXXXXXXXXXXX
HF_REPO_ID=mistralai/Devstral-Small-2507
HF_PROVIDER=featherless-ai
HF_TEMPERATURE=0.5
HF_MAX_TOKENS=128
EMBEDDING_MODEL="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

🔐 Consigue tu token en: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## 🧪 Probar la API local

```bash
uvicorn src.api.main:app --reload
```

Abrir en navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Usar con Docker

### Construir imagen

```bash
docker build -t colombia-agent .
```

### Ejecutar contenedor

```bash
docker run --env-file .env -p 8000:8000 colombia-agent
```

---

## ✅ Pruebas unitarias

```bash
pytest
```

Incluye tests para:

- Verificar funcionamiento del retriever y vector store
- Validar respuestas del agente

Comando para ejecutar los tests

```bash
python -m pytest tests/
```

---

## ✨ Ejemplo de uso

```python
from src.agent.wiki_agent import WikiAgent

agent = WikiAgent()
respuesta = agent.ask("¿Cuál es la capital de Colombia?")
print(respuesta)
```

---

## 📌 Notas

- El agente **solo responde temas sobre Colombia**, gracias al prompt y validaciones.
- Se evita el uso de APIs pagas con modelos open source (aunque se necesita un token gratuito de HuggingFace).
- La base vectorial se crea automáticamente si no existe.


