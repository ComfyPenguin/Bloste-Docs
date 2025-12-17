import os
import re
import subprocess
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type


class PlantUMLPlugin(BasePlugin):
    config_scheme = (
        ('plantuml_jar', Type(str, default='/path/to/plantuml.jar')),
        ('output_format', Type(str, default='png')),
        ('output_dir', Type(str, default='diagrames'))
    )

    def on_config(self, config):
        """
        Valida i configura els paràmetres del plugin.
        """
        self.plantuml_jar = self.config['plantuml_jar']
        self.output_format = self.config['output_format']
        self.output_base_dir = os.path.join(config['site_dir'], self.config['output_dir'])

        # Comprova si el fitxer JAR de PlantUML existeix
        if not os.path.isfile(self.plantuml_jar):
            raise FileNotFoundError(f"No s'ha trobat el fitxer JAR de PlantUML: {self.plantuml_jar}")

        return config

    def on_pre_build(self, config):
        """
        Configura els patrons d'enllaços que es volen ignorar.
        """
        self.ignored_patterns = [
            re.compile(r'^../diagrames/.*')  # Ignora els enllaços que apuntin a la carpeta 'diagrames'
        ]
        print(f"[DEBUG] Ignorant patrons: {self.ignored_patterns}")

    def on_post_page(self, output_content, page, config):
        """
        Ignora els enllaços que coincideixin amb els patrons configurats.
        """
        for pattern in self.ignored_patterns:
            output_content = re.sub(pattern, '', output_content)
        return output_content

    def on_page_markdown(self, markdown, page, config, files):
        """
        Renderitza blocs PlantUML dins del Markdown i genera imatges.
        """
        print(f"[DEBUG] Processant markdown per: {page.file.src_path}")

        # Determina el directori de sortida per a aquest document
        page_output_dir = os.path.join(self.output_base_dir, os.path.dirname(page.file.dest_path))

        def render_plantuml(match):
            # Identificador únic per al diagrama
            diagram_id = abs(hash(match.group(1)))  # Evita valors negatius
            puml_content = match.group(1)

            # Nom del fitxer generat
            output_image = f"diagram_{diagram_id}.{self.output_format}"
            output_path = os.path.join(page_output_dir, output_image)

            # Crea el directori per a aquest document si no existeix
            if not os.path.exists(page_output_dir):
                os.makedirs(page_output_dir, exist_ok=True)

            # Generar fitxer temporal PlantUML
            temp_puml_file = os.path.join(page_output_dir, f"temp_{diagram_id}.puml")
            with open(temp_puml_file, "w", encoding="utf-8") as temp_file:
                temp_file.write("@startuml\n")
                temp_file.write(puml_content.strip())
                temp_file.write("\n@enduml")

            # Generar imatge amb PlantUML
            subprocess.run(["java", "-jar", self.plantuml_jar, f"-t{self.output_format}", temp_puml_file])

            # Renombra el fitxer generat al lloc correcte
            os.rename(temp_puml_file.replace(".puml", f".{self.output_format}"), output_path)

            # Elimina el fitxer temporal
            os.remove(temp_puml_file)

            # Calcula la ruta relativa per a la imatge respecte al document
            relative_path = os.path.relpath(output_path, os.path.dirname(os.path.join(config['site_dir'], page.file.dest_path)))

            # Retorna la referència de la imatge en Markdown
            return f"![Diagrama UML]({relative_path})"

        # Cerca blocs `plantuml` dins del Markdown
        return re.sub(r"```plantuml(.*?)```", render_plantuml, markdown, flags=re.DOTALL)

    def on_files(self, files, config):
        """
        Afegeix tota la carpeta 'diagrames' com a part dels fitxers supervisats per MkDocs.
        """
        from mkdocs.structure.files import File

        # Registra tots els fitxers dins de la carpeta 'diagrames'
        for root, _, filenames in os.walk(self.output_base_dir):
            for filename in filenames:
                if filename.endswith(f".{self.output_format}"):
                    # Ruta relativa respecte al directori de documentació
                    relative_path = os.path.relpath(
                        os.path.join(root, filename), config['docs_dir']
                    )

                    # Crea un objecte File per al fitxer generat
                    diagram_file = File(
                        path=relative_path,
                        src_dir=config['docs_dir'],
                        dest_dir=config['site_dir'],
                        use_directory_urls=False,
                    )

                    # Depuració: Mostra els fitxers que s'afegeixen
                    print(f"[DEBUG] Afegeixo fitxer: {diagram_file.src_path} -> {diagram_file.dest_path}")

                    # Afegeix el fitxer a la llista de fitxers supervisats
                    files.append(diagram_file)

        return files
