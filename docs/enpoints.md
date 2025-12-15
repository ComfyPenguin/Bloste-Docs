# Endpoints

## Endpoints del catálogo

### Endpoints GET

`/api/catalog`: devuelve la lista con todos los videos que hay en la bd (por ahora)
`/api/catalog/:id`: devuelve el video con el id que coincide
`/api/catalog/:topic`: devuelve una lista de videos que coinciden con el tópico

### Endpoints POST

`api/catalog/new`: recibe un json con el objeto de videoEntry

## Enpoints del VideoServer

### Endpoints GET
`api/hls/:videoid` : Envia los videos en formato hls para que el cliente pueda reproducir
### Endpoints POST
`api/videoserver/upload` : Recibe un video en bruto, devuelve los metadatos técnicos (duracion, resolucion, codec, bitrate, fps, tamaño, audio tracks)


