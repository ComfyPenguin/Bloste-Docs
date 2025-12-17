# Documentación para MkDocs

Estos son los pasos mínimos para ejecutar y desarrollar el sitio MkDocs en local.

## Requisitos

- Python 3.8+ instalado
- Git (opcional)

## Crear y activar un entorno virtual

```bash
# Crear el venv
python -m venv .venv

# Activar (bash / zsh)
source .venv/bin/activate

# Activar (fish)
source .venv/bin/activate.fish
```

## Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Construir el sitio (build)

```bash
# Genera la carpeta `site/`
mkdocs build
```

## Servir localmente (live reload)

```bash
# Inicia servidor en http://127.0.0.1:8000
mkdocs serve
# Alternativa usando el python del venv
./.venv/bin/python -m mkdocs serve
```

**Notas**:

- No subir el directorio `.venv/` al repositorio. Añadirlo a `.gitignore`.
- El workflow de GitHub Actions usa `requirements.txt` para instalar dependencias antes de construir y desplegar.
- Si los diagramas Mermaid aparecen como texto, asegúrate de no envolver todo el archivo Markdown en una valla de código y ejecutar `mkdocs build` para regenerar `site/`.

## Instalar una dependencia y actualizar `requirements.txt`

Si necesitas añadir una dependencia al proyecto, sigue uno de estos flujos según prefieras sobrescribir o añadir a `requirements.txt`:

- Instalar y actualizar `requirements.txt` (sobrescribe con el estado actual del entorno):

```bash
# Instala el paquete dentro del venv del proyecto
./.venv/bin/pip install <nombre-paquete>

# Sobrescribe requirements.txt con las versiones actuales
./.venv/bin/pip freeze > requirements.txt
```

- Instalar una versión concreta y fijarla:

```bash
./.venv/bin/pip install <nombre-paquete>==1.2.3
./.venv/bin/pip freeze > requirements.txt
```

Plugins externos añadir una línea con `-e ./plugins` en `requirements.txt`

## Script de automatización

`scripts/mkdocs_local.sh` automatiza la creación del entorno virtual, la instalación de dependencias, la construcción y el servido local.

Uso rápido:

```bash
# Marcar ejecutable (una sola vez)
chmod +x scripts/mkdocs_local.sh

# Crear venv, instalar dependencias y construir el sitio
./scripts/mkdocs_local.sh -a

# Solamente construir el sitio (usa el mkdocs dentro del venv)
./scripts/mkdocs_local.sh -b

# Servir el sitio (usa el mkdocs dentro del venv)
./scripts/mkdocs_local.sh -s

# Forzar recreación del venv y reinstalar
./scripts/mkdocs_local.sh -a -f
```

**Notas**:

- El script crea/usa `.venv/` en la raíz del proyecto.
- No necesitas activar el venv en la shell; el script invoca directamente los binarios dentro de `.venv/bin/`.
- Si prefieres usar tu propio entorno, puedes omitir el paso de creación e instalación y ejecutar `./.venv/bin/mkdocs serve`.
