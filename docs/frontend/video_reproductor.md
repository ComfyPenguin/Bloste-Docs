# Reproductor Móvil
Este es el reproductor principal de blosteflix, una app móvil multiplataforma desarrollada con Flutter para consultar el catálogo y reproducir contenido.

## Showcase
![Carrousel de blosteflix](../assets/blosteflixApp.gif){ style="display: block; margin: 0 auto; width: 300px;" }

## Arquitectura

La aplicación está construida siguiendo los principios de **Clean Architecture**, dividida en tres capas principales:

- **Domain**: Entidades, repositorios abstractos y casos de uso
- **Infrastructure**: Implementación de repositorios, APIs y mappers de datos
- **Presentation**: Interfaces de usuario, providers de estado y servicios

### Tecnologías principales

+ **Flutter** (SDK 3.10.7+): Framework multiplataforma
+ **Riverpod**: Gestión de estado reactiva
+ **Chewie + Video Player**: Reproducción de video HLS
+ **Flutter Secure Storage**: Almacenamiento seguro de tokens
+ **HTTP**: Comunicación con APIs REST

### Que hace ?

+ Login y registro de usuarios con JWT
+ Autenticación con tokens de acceso y refresh
+ Muestra catálogo de videos con scroll infinito
+ Búsqueda y filtrado de contenido por categorías
+ Reproduce videos en formato HLS con selección de calidad (Auto, 480p, 720p, 1080p)
+ Visualización de videos relacionados
+ Gestión de cuenta de usuario

### Interacción
Este componente interactúa con:

+ **Catálogo Backend**: Gestión de videos y categorías
+ **Auth Backend**: Autenticación y gestión de usuarios
+ **Media Backend**: Streaming HLS de videos

### Endpoints

#### Endpoints de autenticación
+ `POST /api/auth/token`: Login de usuario (retorna access y refresh tokens)
+ `POST /api/auth/register`: Registro de nuevo usuario
+ `POST /api/auth/refresh`: Renovación de access token usando refresh token
+ `GET /api/users/me`: Obtener detalles del usuario autenticado (requiere Bearer token)

#### Endpoints catálogo
+ `GET /api/catalogo`: Recibe videos paginados (params: page, size, categoriaId opcional). La paginación es 0-indexed (page=0 para la primera página)
+ `GET /api/catalogo/search`: Búsqueda de videos por título (params: titulo, page, size). La paginación es 0-indexed
+ `GET /api/catalogo/:id`: Recibe detalles de un video específico
+ `GET /api/categorias`: Recibe categorías paginadas (params: page, size). La paginación es 0-indexed
+ `GET /api/categorias/:id`: Recibe una categoría específica

#### Endpoints video backend (Media Server)
Todos los endpoints de media requieren autenticación Bearer token en el header:
+ `GET /api/hls/:videoid/master.m3u8`: Playlist HLS adaptativo (Auto)
+ `GET /api/hls/:videoid/480/playlist.m3u8`: Playlist para calidad 480p
+ `GET /api/hls/:videoid/720/playlist.m3u8`: Playlist para calidad 720p
+ `GET /api/hls/:videoid/1080/playlist.m3u8`: Playlist para calidad 1080p
+ `GET /api/hls/:videoid/:segment.ts`: Recibe los segmentos de video para reproducción

## Casos de uso

```mermaid
flowchart LR
    User([👤 User])
    Player([🎬 Video Player])

    subgraph Servidor_Catálogo
       VerCatalogo([Ver catálogo])
       Filtrar([Buscar/Filtrar contenido])
       Detalles([Ver detalles])
       Categorias([Ver categorías])
    end

    subgraph Servidor_Video
        ReproducirVideo([Reproducir Video])
        SeleccionarCalidad([Seleccionar calidad])
        VideosRelacionados([Ver relacionados])
    end

    subgraph Servidor_Auth
        Login([Login])
        Registro([Registro])
        RefreshToken([Renovar sesión])
        GestionCuenta([Gestión de cuenta])
    end

    User --> Player
    Player --> VerCatalogo
    Player --> ReproducirVideo
    Player --> Login
    Player --> Registro
    Player --> Filtrar
    Player --> Detalles
    Player --> Categorias
    Player --> SeleccionarCalidad
    Player --> VideosRelacionados
    Player --> RefreshToken
    Player --> GestionCuenta

```

### Diagramas de flujo

#### Explorar catálogo

```plantuml
@startuml
actor Usuario
participant AppCliente
participant CatalogoServer

Usuario -> AppCliente : Acceder a catálogo
AppCliente -> CatalogoServer : GET /api/catalogo?page=0&size=30
alt Servicio responde
    CatalogoServer --> AppCliente : Lista paginada de videos
    AppCliente --> Usuario : Mostrar catálogo con scroll infinito
else Servicio no responde
    CatalogoServer --> AppCliente : Error
    AppCliente --> Usuario : Mostrar error general
end
@enduml

```

#### Buscar contenidos

```plantuml
@startuml
actor Usuario
participant AppCliente
participant CatalogoServer

Usuario -> AppCliente : Introducir término de búsqueda
AppCliente -> CatalogoServer : GET /api/catalogo/search?titulo=...&page=0&size=30
alt Hay resultados
    CatalogoServer --> AppCliente : Lista paginada de videos
    AppCliente --> Usuario : Mostrar resultados
else Sin resultados
    CatalogoServer --> AppCliente : Lista vacía
    AppCliente --> Usuario : Mostrar mensaje informativo
end
@enduml

```

#### Consultar detalle de un video

```plantuml
@startuml
actor Usuario
participant AppCliente
participant CatalogoServer

Usuario -> AppCliente : Seleccionar vídeo
AppCliente -> CatalogoServer : GET /api/catalogo/{id}
alt Vídeo encontrado
    CatalogoServer --> AppCliente : Metadatos completos del video
    AppCliente --> Usuario : Mostrar ficha del vídeo
else Vídeo no encontrado
    CatalogoServer --> AppCliente : Error 404
    AppCliente --> Usuario : Mostrar error
end
@enduml

```

#### Iniciar sesión / Registro

```plantuml

@startuml
actor Usuario
participant AppCliente
participant AuthService
participant SecureStorage

Usuario -> AppCliente : Introducir credenciales
AppCliente -> AuthService : POST /api/auth/token
alt Credenciales válidas
    AuthService --> AppCliente : Access Token + Refresh Token (JWT)
    AppCliente -> SecureStorage : Guardar tokens
    AppCliente -> AuthService : GET /api/users/me (Bearer token)
    AuthService --> AppCliente : Datos del usuario
    AppCliente --> Usuario : Acceso completo al catálogo
else Credenciales incorrectas
    AuthService --> AppCliente : Error 401/403
    AppCliente --> Usuario : Mostrar error de autenticación
end

Usuario -> AppCliente : Registrarse
AppCliente -> AuthService : POST /api/auth/register
alt Registro exitoso
    AuthService --> AppCliente : Access Token + Refresh Token
    AppCliente -> SecureStorage : Guardar tokens
    AppCliente --> Usuario : Cuenta creada, acceso completo
else Error en registro
    AuthService --> AppCliente : Error (usuario existente, etc.)
    AppCliente --> Usuario : Mostrar error
end
@enduml


```

#### Reproducir video

```plantuml
@startuml
actor Usuario
participant AppCliente
participant SecureStorage
participant MediaServer

Usuario -> AppCliente : Solicitar reproducción
AppCliente -> SecureStorage : Obtener access token
alt Token válido
    SecureStorage --> AppCliente : Access Token
    AppCliente -> MediaServer : GET /api/hls/:videoid/master.m3u8<br/>(Authorization: Bearer token)
    alt Autenticación exitosa
        MediaServer --> AppCliente : Playlist HLS adaptativo
        AppCliente -> MediaServer : GET segmentos .ts
        MediaServer --> AppCliente : Segmentos de video
        AppCliente --> Usuario : Iniciar reproducción
        
        Usuario -> AppCliente : Cambiar calidad (480p/720p/1080p)
        AppCliente -> MediaServer : GET /api/hls/:videoid/{calidad}/playlist.m3u8
        MediaServer --> AppCliente : Playlist calidad específica
        AppCliente --> Usuario : Continuar reproducción en nueva calidad
    else Error de autenticación
        MediaServer --> AppCliente : Error 401/403
        AppCliente -> SecureStorage : Intentar refresh token
        AppCliente --> Usuario : Renovar sesión o error
    end
else Token no disponible
    SecureStorage --> AppCliente : No hay token
    AppCliente --> Usuario : Redirigir a login
end
@enduml

```

#### Renovar token de acceso

```plantuml
@startuml
actor Usuario
participant AppCliente
participant SecureStorage
participant AuthService

AppCliente -> AppCliente : Access token expirado
AppCliente -> SecureStorage : Obtener refresh token
alt Refresh token disponible
    SecureStorage --> AppCliente : Refresh Token
    AppCliente -> AuthService : POST /api/auth/refresh
    alt Refresh exitoso
        AuthService --> AppCliente : Nuevo Access Token + Refresh Token
        AppCliente -> SecureStorage : Actualizar tokens
        AppCliente --> Usuario : Sesión renovada (transparente)
    else Refresh token inválido
        AuthService --> AppCliente : Error 401
        AppCliente -> SecureStorage : Limpiar tokens
        AppCliente --> Usuario : Redirigir a login
    end
else No hay refresh token
    AppCliente --> Usuario : Redirigir a login
end
@enduml

```

#### Ver videos relacionados

```plantuml
@startuml
actor Usuario
participant AppCliente
participant CatalogoServer

Usuario -> AppCliente : Reproduciendo video
AppCliente -> CatalogoServer : GET /api/catalogo?page=0&size=30
alt Videos disponibles
    CatalogoServer --> AppCliente : Lista de videos
    AppCliente -> AppCliente : Filtrar video actual
    AppCliente --> Usuario : Mostrar videos relacionados (máx 20)
    
    Usuario -> AppCliente : Seleccionar video relacionado
    AppCliente --> Usuario : Reproducir nuevo video
else Error al cargar
    CatalogoServer --> AppCliente : Error
    AppCliente --> Usuario : Mensaje sin videos relacionados
end
@enduml

```

#### Filtrar por categorías

```plantuml
@startuml
actor Usuario
participant AppCliente
participant CatalogoServer

Usuario -> AppCliente : Seleccionar categoría
AppCliente -> CatalogoServer : GET /api/categorias?page=0&size=20
CatalogoServer --> AppCliente : Lista de categorías
AppCliente --> Usuario : Mostrar categorías

Usuario -> AppCliente : Filtrar por categoría
AppCliente -> CatalogoServer : GET /api/catalogo?page=0&size=30&categoriaId={id}
alt Videos en categoría
    CatalogoServer --> AppCliente : Videos filtrados
    AppCliente --> Usuario : Mostrar videos de la categoría
else Sin videos
    CatalogoServer --> AppCliente : Lista vacía
    AppCliente --> Usuario : Mensaje sin contenido
end
@enduml
```
