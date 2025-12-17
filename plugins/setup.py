from setuptools import setup

setup(
    name="mkdocs-jarplantuml",
    version="0.1",
    description="Plugin per renderitzar PlantUML amb el jar a MkDocs",
    packages=["mkdocs_jarplantuml"],
    entry_points={
        "mkdocs.plugins": [
            "mkdocs_jarplantuml = mkdocs_jarplantuml.plugin:PlantUMLPlugin"
        ]
    },
)
