# Documentación FFmpeg

Una solución para grabar, convertir y transmitir audio y vídeo.

FFmpeg incluye:

+ ffmpeg: El comando principal para convertir (transcodificar) archivos multimedia.

+ ffplay: Un reproductor multimedia simple.

+ ffprobe: Para analizar y obtener información de archivos multimedia.

+ Librerías (libavcodec, libavformat, etc.): El corazón del proyecto, usadas por miles de aplicaciones (VLC, OBS, Chrome, etc.).

El flujo de procesamiento que siguen los videos es:

!!! note
    [Archivo de Entrada] → [Demuxer] → [Paquetes Codificados] → [Decoder] → [Frames/Crudos] → [Filtros] → [Frames/Procesados] → [Encoder] → [Paquetes Codificados] → [Muxer] → [Archivo de Salida]
