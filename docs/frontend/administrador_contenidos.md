# Administrador Contenidos (VUE)

## Descripción

Aplicación web para la gestión de contenidos de video, permitiendo a los administradores subir nuevos videos y gestionar el catálogo de videos disponibles para los usuarios finales.

### Responsabilidades

+ Subida de  videos al servidor de contenidos
+ Edicion de datos del catalogo de videos (título, descripción, categorías)

### Interacción

Este componente interactua con:

+ `Login/Signin` (Backend Odoo)
+ `Catálogo` (Backend SpringBoot)
+ `VideoServer` (Backend ExpressJS)

### Endpoints

Endpoint usados por la app de administración:

#### Endpoints catalogo

+ POST `api/catalogo`: Registra nueva entrada de video
+ PUT `api/catalogo/:id`: Modificar datos de un video existente
+ GET `api/catalogo/:id`: Obtener datos de un video existente en específico para edición
+ GET `api/catalogo`: Obtener lista completa de videos para mostrar en el panel de administración
+ GET `api/categorias`: Obtener lista de categorías disponibles

#### Endpoints del servidor de contenidos

+ POST `api/upload`: Subir un video en bruto para procesar y generar los segmentos, miniaturas y metadatos técnicos

## Casos de uso

```mermaid
flowchart LR
    Admin([👤 Administrador])
    AppAdmin([🖥️ App Administración])
    
    subgraph Servidor de contenidos ExpressJS
        SubirVideo([Subir video /api/upload])
        ConectarWS([Conectar WebSocket])
        RecibirMeta([Recibir metadatos])
    end


    subgraph Catalogo SpringBoot
        RegistrarVideo([Registrar video al catálogo])
        ModificarVideo([Editar catálogo])
    end

    subgraph Seguridad Odoo
        Login([Iniciar sesión])
        Signin([Registrar nuevo administrador])
    end

    Admin --> AppAdmin

    AppAdmin --> Login
    AppAdmin --> Signin

    AppAdmin --> SubirVideo
    SubirVideo --> RecibirMeta
    RecibirMeta --> AppAdmin

    SubirVideo --> ConectarWS

    AppAdmin --> RegistrarVideo
    AppAdmin --> ModificarVideo

```

## Diagramas de flujo

### Autenticación del Administrador

```plantuml
@startuml
actor Administrador
participant AppEscritorio as "App Vue\n(Frontend)"
participant Backend as "Servicio Autenticación\n(Odoo)"

Administrador -> AppEscritorio : Introducir credenciales\n(email, password)
activate AppEscritorio

AppEscritorio -> Backend : POST /api/auth/token\n(credenciales)
activate Backend

Backend -> Backend : Validar credenciales
Backend -> Backend : Verificar permisos de administrador

alt Autenticación exitosa
    Backend --> AppEscritorio : 200 OK\n(JWT + permisos)
    AppEscritorio -> AppEscritorio : Guardar token (storage)
    AppEscritorio -> AppEscritorio : Actualizar estado auth
    AppEscritorio --> Administrador : Redirección al panel de administración
else Credenciales incorrectas
    Backend --> AppEscritorio : 401 Unauthorized
    AppEscritorio --> Administrador : Mostrar error de autenticación
else Error de servicio
    Backend --> AppEscritorio : 503 Service Unavailable
    AppEscritorio --> Administrador : Mostrar error de conexión
end

deactivate Backend
deactivate AppEscritorio
@enduml
```

### Gestión de Contenido: Subida

```plantuml
@startuml
actor Administrador
participant AppEscritorio as "App Vue\n(Frontend)"
participant VideoServer as "Video Server\n(ExpressJS)"
participant Catalogo as "Servicio Catálogo\n(SpringBoot)"

Administrador -> AppEscritorio : Seleccionar video local
activate AppEscritorio

AppEscritorio -> VideoServer : POST /api/upload\n(archivo de vídeo)
activate VideoServer

note over VideoServer : El servidor procesa el video\n(FFmpeg) y genera metadatos

VideoServer --> AppEscritorio : 200 OK (metadatos técnicos + endpoints)
deactivate VideoServer

Administrador -> AppEscritorio : Editar metadatos catálogo\n(título, descripción, etiquetas)

AppEscritorio -> Catalogo : POST /api/catalogo\n(datos técnicos + datos editados)
activate Catalogo

alt Registro exitoso
    Catalogo --> AppEscritorio : 201 Created (Confirmación)
    AppEscritorio --> Administrador : Vídeo registrado correctamente
else Error en datos
    Catalogo --> AppEscritorio : 400 Bad Request (Faltan campos)
    AppEscritorio --> Administrador : Error: Metadatos incompletos
end

deactivate Catalogo
deactivate AppEscritorio
@enduml
```

```plantuml
@startuml
actor Administrador
participant AppEscritorio as "App Vue\n(Frontend)"
participant VideoServer as "Video Server\n(ExpressJS)"
participant WS as "WebSocket\n(ExpressJS)"
participant Catalogo as "Servicio Catálogo\n(Spring Boot)"

== Subida de vídeo ==
Administrador -> AppEscritorio : Seleccionar vídeo local
activate AppEscritorio

AppEscritorio -> WS : Conectar WebSocket
WS --> AppEscritorio : Conexión establecida

AppEscritorio -> VideoServer : POST /api/upload\n(archivo de vídeo)
activate VideoServer

VideoServer -> VideoServer : Procesar vídeo (FFmpeg)
VideoServer -> VideoServer : Extraer metadatos técnicos
VideoServer -> VideoServer : Generar recursos (HLS, miniaturas)

== Notificaciones asíncronas ==
VideoServer -> WS : Evento progreso / finalización\n(metadatos + endpoints)
WS --> AppEscritorio : Notificación procesado completado
deactivate VideoServer

== Completar información ==
Administrador -> AppEscritorio : Introducir metadatos funcionales\n(título, descripción, etiquetas)

== Registro en catálogo ==
AppEscritorio -> Catalogo : POST /api/catalogo\n(metadatos técnicos + funcionales)
activate Catalogo

alt Registro exitoso
    Catalogo --> AppEscritorio : 201 Created
    AppEscritorio --> Administrador : Vídeo registrado correctamente
else Error de validación
    Catalogo --> AppEscritorio : 400 Bad Request
    AppEscritorio --> Administrador : Mostrar error de validación
end

deactivate Catalogo
deactivate AppEscritorio
@enduml

@enduml
```

### Gestión de Contenido: Edición

```plantuml
@startuml
actor Administrador
participant AppEscritorio as "App Vue\n(Frontend)"
participant Catalogo as "Servicio Catálogo\n(Spring Boot)"

== Carga del contenido ==
Administrador -> AppEscritorio : Acceder a edición de vídeo
activate AppEscritorio

AppEscritorio -> Catalogo : GET /api/catalogo/{videoId}
activate Catalogo

Catalogo -> Catalogo : Validar permisos admin
Catalogo -> Catalogo : Obtener datos del vídeo

alt Vídeo encontrado
    Catalogo --> AppEscritorio : 200 OK\n(metadatos funcionales)
else Vídeo no existe
    Catalogo --> AppEscritorio : 404 Not Found
    AppEscritorio --> Administrador : Mostrar error de recurso inexistente
    deactivate Catalogo
    deactivate AppEscritorio
    return
end

deactivate Catalogo

== Edición ==
Administrador -> AppEscritorio : Modificar metadatos\n(título, descripción, etiquetas, visibilidad)

== Guardado de cambios ==
AppEscritorio -> Catalogo : PUT /api/catalogo/{videoId}\n(metadatos actualizados)
activate Catalogo

Catalogo -> Catalogo : Validar datos
Catalogo -> Catalogo : Actualizar registro

alt Actualización exitosa
    Catalogo --> AppEscritorio : 200 OK\n(confirmación)
    AppEscritorio --> Administrador : Cambios guardados correctamente
else Error de validación
    Catalogo --> AppEscritorio : 400 Bad Request\n(datos inválidos)
    AppEscritorio --> Administrador : Mostrar errores de validación
end

deactivate Catalogo
deactivate AppEscritorio
@enduml
```

## UI/UX

### Login

![Login](../assets/admin-vue/admin-login.png)

### Registro

![Registro](../assets/admin-vue/admin-register.png)

### Subida de video

Sin video de seleccionado:

![Subida sin video de seleccionado](../assets/admin-vue/admin-upload-no-video.png)

Con video de seleccionado:

![Subida con video de seleccionado](../assets/admin-vue/admin-upload-with-video.png)

### Panel de edición de video

![Panel de edición de video](../assets/admin-vue/admin-edit-panel.png)

### Popup de edición de video

![Popup de edición de video](../assets/admin-vue/admin-edit-popup.png)