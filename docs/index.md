# Bienvenido a la documentacion de Blosteflix

Blosteflix es un proyecto de desarrollo de una app al estilo Netflix.
Esta formado por varios componentes cada uno con su responsabilidad, entre ellos tenemos:

+ Repoductor video, hecho en Flutter
+ Un gestor de los videos subidos a la plataforma, hecho en Vue
+ Un servidor API REST que muestra el catálogo, hecho en Spring
+ Un servidor de contenido HLS, hecho en hls
+ Y a futuro una pasarela de pagos administrada mediante Odoo.


 ## Documentación FFmpeg
 Una solución para grabar, convertir y transmitir audio y vídeo. 

FFmpeg incluye:
+ ffmpeg: El comando principal para convertir (transcodificar) archivos multimedia.

+ ffplay: Un reproductor multimedia simple.

+ ffprobe: Para analizar y obtener información de archivos multimedia.

+ Librerías (libavcodec, libavformat, etc.): El corazón del proyecto, usadas por miles de aplicaciones (VLC, OBS, Chrome, etc.).

El flujo de procesamiento que siguen los videos es:
```
[Archivo de Entrada] → [Demuxer] → [Paquetes Codificados] → [Decoder] → [Frames/Crudos] → [Filtros] → [Frames/Procesados] → [Encoder] → [Paquetes Codificados] → [Muxer] → [Archivo de Salida]
```
