# Servidor HLS de videos (EXPRESSJS)

## Descripción

Servidor express encargado de procesar videos en segmentos y servirlos, además de generar miniaturas y metadatos para los servicios de reproducción.

### Responsabilidades

+ Comprobar autenticación y autorización de los clientes
+ Generar HLS y segmentos de video en distintas resoluciones
+ Generar miniaturas para cada video
+ Generar metadatos técnicos de cada video
+ Servir los segmentos y miniaturas a los clientes

### Interacción

Este componente interactua con:

+ Video Player (Flutter)
+ Admin App (Vue)
+ Autentificaciones (odoo)

## Endpoints

### Endpoints GET

+ `api/hls/:videoid` : Sirve el mapa hls para que el cliente pueda reproducir el video
+ `api/thumbnail/:videoid` : Sirve la miniatura del video al cliente

### Endpoints POST

+ `api/upload` : Recibe un video en bruto para procesarlo y generar los segmentos, miniaturas y metadatos técnicos. Este endpoint es utilizado por la Admin App para subir nuevos videos al sistema.
Además, este endpoint se encarga de validar el formato del video, extraer los metadatos técnicos (duración, resolución, codec) y devolverlos.

## Casos de uso

```mermaid
flowchart LR
    Player([🎬 Video Player])
    Admin([👤 Admin App])

    subgraph Servidor HLS
        DescargarSegmentos((Descargar segmentos HLS))
        DescargarThumbnails((Descargar miniaturas))
        SubirVideo((Subir video para procesar))
    end

    Player --> DescargarSegmentos
    Player --> DescargarThumbnails
    Admin --> SubirVideo

```

## Diagramas de flujo

### Reproducir video

```plantuml
@startuml
participant VideoReproductor
participant VideoServer

VideoReproductor -> VideoServer : GET /api/hls/{videoId}/master.m3u8
activate VideoServer

VideoServer -> VideoServer : Validar token

alt Token inválido
    VideoServer --> VideoReproductor : 401 Unauthorized
else Token válido
    VideoServer -> VideoServer : Comprobar vídeo disponible

    alt Vídeo no disponible
        VideoServer --> VideoReproductor : 404 Not Found
    else Vídeo disponible
        VideoServer --> VideoReproductor : 200 OK\n(master.m3u8)
    end
end

deactivate VideoServer
@enduml
```

### Recibir miniatura

```plantuml
@startuml
participant VideoReproductor
participant VideoServer

VideoReproductor -> VideoServer : GET /api/thumbnail/{videoId}
activate VideoServer

VideoServer -> VideoServer : Validar token

alt Token inválido
    VideoServer --> VideoReproductor : 401 Unauthorized
else Token válido
    VideoServer -> VideoServer : Comprobar existencia de miniatura

    alt Miniatura encontrada
        VideoServer --> VideoReproductor : 200 OK\n(image/png)
    else Miniatura no encontrada
        VideoServer --> VideoReproductor : 404 Not Found
    end
end

deactivate VideoServer
@enduml

```

### Subir video

```plantuml
@startuml
actor WebAdmin
participant VideoServer
participant WebSocketServer
participant CatalogoServer

== Inicialización ==
WebAdmin -> WebSocketServer : Conectar (WebSocket)
WebSocketServer --> WebAdmin : Conexión establecida

== Subida de vídeo ==
WebAdmin -> VideoServer : POST /api/upload (archivo de vídeo)
VideoServer --> WebAdmin : Confirmación de recepción

== Procesamiento ==
VideoServer -> VideoServer : Validar formato

VideoServer -> VideoServer : Extraer metadatos técnicos

VideoServer -> VideoServer : Trocear vídeo

VideoServer -> VideoServer : Generar miniaturas

== Finalización ==
VideoServer -> WebSocketServer : Evento finalización\n(metadatos técnicos,\nendpoints)
WebSocketServer --> WebAdmin : Notificación finalización
WebAdmin <- VideoServer : Metadatos técnicos + endpoints
WebAdmin <- WebSocketServer : Desconectar (WebSocket)

== Registro en catálogo ==
WebAdmin -> WebAdmin : Añadir datos funcionales\n(título, descripción, etiquetas, autor)
WebAdmin -> CatalogoServer : POST /api/catalogo\n(metadatos completos)
CatalogoServer -> CatalogoServer : Guardar información del vídeo
CatalogoServer --> WebAdmin : Confirmación de registro
@enduml
```
