# Documentación del microservicio Catálogo

### Descripción
Microservicio Spring Boot encargado de gestionar el catálogo de videos y categorías de la plataforma. Proporciona una API REST para el almacenamiento, consulta y administración de metadatos de videos y sus clasificaciones por categorías.

### Responsabilidades
+ Gestionar el catálogo completo de videos
+ Administrar categorías de contenido
+ Proporcionar búsqueda y filtrado de videos
+ Gestionar metadatos de videos (título, descripción, miniaturas)
+ Controlar la visibilidad de contenido (videos ocultos)
+ Autenticar y autorizar operaciones mediante JWT

### Interacción
Este componente interactúa con:
+ Administrador de Contenidos (Admin App)
+ Reproductor de Videos (Video Player)
+ Servidor HLS de Videos
+ Gestor de Suscripciones

## Endpoints

### Endpoints GET - Videos

+ `GET /api/catalogo?page={int}&size={int}` : Obtiene el catálogo paginado de videos públicos
+ `GET /api/catalogo/{id}` : Obtiene un video específico por su ID
+ `GET /api/catalogo?categoriaId={int}&page={int}&size={int}` : Obtiene videos de una categoría específica
+ `GET /api/catalogo/search?titulo={titulo}&page={int}&size={int}` : Busca videos por título , paginado

### Endpoints GET - Categorías

+ `GET /api/categorias` : Obtiene todas las categorías disponibles
+ `GET /api/categorias/{id}` : Obtiene una categoría específica por su ID

### Endpoints POST

+ `POST /api/catalogo/videos` : Crea un nuevo video en el catálogo (requiere autenticación de administrador)
+ `POST /api/categorias` : Crea una nueva categoría (requiere autenticación de administrador)

### Endpoints PUT

+ `PUT /api/catalogo/videos/{id}` : Actualiza los datos de un video existente (requiere autenticación de administrador)
+ `PUT /api/categorias/{id}` : Actualiza una categoría existente (requiere autenticación de administrador)

### Endpoints DELETE

Delete videos no se usa porque en su lugar se maneja un campo `is_hidden` para ocultar videos sin eliminarlos físicamente.

+ `DELETE /api/catalogo/videos/{id}` : Elimina un video del catálogo (requiere autenticación de administrador)
+ `DELETE /api/categorias/{id}` : Elimina una categoría (requiere autenticación de administrador)

## Casos de uso

```mermaid
%%{init: {'theme':'base','themeVariables': {'primaryColor':'#0ea5a4','edgeColor':'#065f46','fontFamily':'"Inter", Arial'}} }%%
graph LR
  %% Agrupación de usuarios
  subgraph Usuarios
    direction TB
    U1[🎬 Video Player]
    U3[🛠️ App Admin]
  end

  %% Casos de uso divididos en dos áreas
  subgraph "Casos de uso"
    direction LR
    subgraph "Consulta Pública"
      direction TB
      UC1((🔎 Consultar catálogo completo))
      UC2((📂 Consultar por categoría))
      UC3((🔤 Buscar por título))
      UC4((📋 Listar categorías))
    end

    subgraph "Gestión de Videos"
      direction TB
      UC5((⬆️ Crear video))
      UC6((✏️ Modificar video))
      UC7((🗑️ Eliminar video\n(no usado — soft delete)))
      UC8((👁️ Ocultar/Mostrar video))
    end

    subgraph "Gestión de Categorías"
      direction TB
      UC9((➕ Crear categoría))
      UC10((✏️ Modificar categoría))
      UC11((🗑️ Eliminar categoría))
    end
  end

  %% Relaciones - Consulta (Video Player usa GET)
  U1 -->|GET| UC1
  U1 -->|GET| UC2
  U1 -->|GET| UC3
  U1 -->|GET| UC4

  %% Relaciones - Administración (Admin usa POST/PUT; DELETE raramente por soft delete)
  U3 -->|POST/PUT| UC5
  U3 -->|POST/PUT| UC6
  U3 -->|DELETE (soft)| UC7
  U3 -->|POST/PUT| UC8
  U3 -->|POST/PUT| UC9
  U3 -->|POST/PUT| UC10
  U3 -->|POST/DELETE| UC11

  %% Estilos
  class U1,U3 usernode
  class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10,UC11 usecase

  classDef usernode fill:#e0f2fe,stroke:#0369a1,stroke-width:2px,rx:8px;
  classDef usecase fill:#ecfccb,stroke:#65a30d,stroke-width:1.5px,rx:20px;
```

## Diagrama Entidad-Relación

```plantuml
@startuml

entity Video {
  +id : int <<PK>>
  --
  creator : varchar
  title : varchar
  description : text
  duration_seconds : int
  url_video : varchar
  url_thumbnail : varchar
  upload_date : datetime
  is_hidden : boolean
}

entity Categoria {
  +id : int <<PK>>
  --
  name : varchar
  description : text
}

entity Video_Categoria {
  +video_id : int <<FK>>
  +categoria_id : int <<FK>>
}

' ===========================
' RELACIONES
' ===========================

Video ||--o{ Video_Categoria
Categoria ||--o{ Video_Categoria

@enduml
```

## Modelo de datos

### Video
Representa un video en el catálogo con sus metadatos de negocio.

**Campos:**
- `id`: Identificador único del video
- `creator`: Usuario o entidad que creó el video
- `title`: Título del video
- `description`: Descripción detallada del contenido
- `duration_seconds`: Duración del video en segundos
- `url_video`: URL del archivo de video procesado (HLS)
- `url_thumbnail`: URL de la miniatura/thumbnail del video
- `upload_date`: Fecha y hora de subida
- `is_hidden`: Indica si el video está oculto o visible públicamente

### Categoria
Agrupa videos por temática o tipo de contenido.

**Campos:**
- `id`: Identificador único de la categoría
- `name`: Nombre de la categoría
- `description`: Descripción de la categoría

### Video_Categoria
Tabla de relación muchos-a-muchos entre videos y categorías.

**Campos:**
- `video_id`: Referencia al video
- `categoria_id`: Referencia a la categoría

## Diagramas de flujo

### Consultar catálogo de videos

```plantuml
@startuml
participant Usuario
participant VideoPlayer
participant CatalogoService
database "Base de Datos" as DB

Usuario -> VideoPlayer : Solicita ver catálogo
VideoPlayer -> CatalogoService : GET /api/catalogo/videos
activate CatalogoService

CatalogoService -> DB : SELECT videos WHERE is_hidden = false
activate DB
DB --> CatalogoService : Lista de videos públicos
deactivate DB

CatalogoService --> VideoPlayer : 200 OK\n[Lista de videos con metadatos]
deactivate CatalogoService
VideoPlayer --> Usuario : Muestra catálogo

@enduml
```

### Buscar videos por categoría

```plantuml
@startuml
participant Usuario
participant VideoPlayer
participant CatalogoService
database "Base de Datos" as DB

Usuario -> VideoPlayer : Filtra por categoría
VideoPlayer -> CatalogoService : GET /api/catalogo/videos/categoria/{id}
activate CatalogoService

CatalogoService -> DB : Verificar existencia de categoría
activate DB
DB --> CatalogoService : Categoría encontrada
deactivate DB

CatalogoService -> DB : SELECT videos JOIN video_categoria
activate DB
DB --> CatalogoService : Videos de la categoría
deactivate DB

alt Categoría válida con videos
    CatalogoService --> VideoPlayer : 200 OK\n[Videos de la categoría]
else Categoría no encontrada
    CatalogoService --> VideoPlayer : 404 Not Found
else Categoría sin videos
    CatalogoService --> VideoPlayer : 200 OK\n[Lista vacía]
end

deactivate CatalogoService
VideoPlayer --> Usuario : Muestra resultados

@enduml
```

### Crear nuevo video

```plantuml
@startuml
actor Administrador
participant AdminApp
participant CatalogoService
participant JwtFilter
database "Base de Datos" as DB

Administrador -> AdminApp : Crea nuevo video
AdminApp -> CatalogoService : POST /api/catalogo/videos\n(JWT Token, VideoPostDTO)
activate CatalogoService

CatalogoService -> JwtFilter : Validar token JWT
activate JwtFilter

alt Token válido y rol Admin
    JwtFilter --> CatalogoService : Token válido
    deactivate JwtFilter
    
    CatalogoService -> CatalogoService : Validar datos del video
    
    CatalogoService -> DB : INSERT nuevo video
    activate DB
    DB --> CatalogoService : Video creado (ID generado)
    deactivate DB
    
    CatalogoService -> DB : INSERT relaciones con categorías
    activate DB
    DB --> CatalogoService : Relaciones creadas
    deactivate DB
    
    CatalogoService --> AdminApp : 201 Created\n(VideoPrivateDTO)
else Token inválido
    JwtFilter --> CatalogoService : Token inválido
    deactivate JwtFilter
    CatalogoService --> AdminApp : 401 Unauthorized
else Rol insuficiente
    JwtFilter --> CatalogoService : Sin permisos
    deactivate JwtFilter
    CatalogoService --> AdminApp : 403 Forbidden
else Datos inválidos
    CatalogoService --> AdminApp : 400 Bad Request
end

deactivate CatalogoService
AdminApp --> Administrador : Confirmación

@enduml
```

### Modificar video existente

```plantuml
@startuml
actor Administrador
participant AdminApp
participant CatalogoService
participant JwtFilter
database "Base de Datos" as DB

Administrador -> AdminApp : Modifica video
AdminApp -> CatalogoService : PUT /api/catalogo/videos/{id}\n(JWT Token, VideoPostDTO)
activate CatalogoService

CatalogoService -> JwtFilter : Validar token JWT
activate JwtFilter
JwtFilter --> CatalogoService : Token válido
deactivate JwtFilter

CatalogoService -> DB : SELECT video WHERE id = {id}
activate DB

alt Video existe
    DB --> CatalogoService : Video encontrado
    deactivate DB
    
    CatalogoService -> CatalogoService : Validar nuevos datos
    
    CatalogoService -> DB : UPDATE video SET...
    activate DB
    DB --> CatalogoService : Video actualizado
    deactivate DB
    
    CatalogoService -> DB : Actualizar categorías
    activate DB
    DB --> CatalogoService : Categorías actualizadas
    deactivate DB
    
    CatalogoService --> AdminApp : 200 OK\n(VideoPrivateDTO actualizado)
else Video no existe
    DB --> CatalogoService : Video no encontrado
    deactivate DB
    CatalogoService --> AdminApp : 404 Not Found
end

deactivate CatalogoService
AdminApp --> Administrador : Confirmación

@enduml
```

### Eliminar video

```plantuml
@startuml
actor Administrador
participant AdminApp
participant CatalogoService
participant JwtFilter
database "Base de Datos" as DB

Administrador -> AdminApp : Elimina video
AdminApp -> CatalogoService : DELETE /api/catalogo/videos/{id}\n(JWT Token)
activate CatalogoService

CatalogoService -> JwtFilter : Validar token JWT
activate JwtFilter
JwtFilter --> CatalogoService : Token válido y Admin
deactivate JwtFilter

CatalogoService -> DB : SELECT video WHERE id = {id}
activate DB

alt Video existe
    DB --> CatalogoService : Video encontrado
    deactivate DB
    
    CatalogoService -> DB : DELETE FROM video_categoria\nWHERE video_id = {id}
    activate DB
    DB --> CatalogoService : Relaciones eliminadas
    deactivate DB
    
    CatalogoService -> DB : DELETE FROM video\nWHERE id = {id}
    activate DB
    DB --> CatalogoService : Video eliminado
    deactivate DB
    
    CatalogoService --> AdminApp : 204 No Content
else Video no existe
    DB --> CatalogoService : Video no encontrado
    deactivate DB
    CatalogoService --> AdminApp : 404 Not Found
end

deactivate CatalogoService
AdminApp --> Administrador : Confirmación

@enduml
```

### Gestión de categorías

```plantuml
@startuml
actor Administrador
participant AdminApp
participant CatalogoService
database "Base de Datos" as DB

== Crear Categoría ==
Administrador -> AdminApp : Crea nueva categoría
AdminApp -> CatalogoService : POST /api/catalogo/categorias\n(JWT, CategoriaPostDTO)
activate CatalogoService

CatalogoService -> DB : Verificar si ya existe
activate DB

alt Categoría no existe
    DB --> CatalogoService : No existe
    deactivate DB
    
    CatalogoService -> DB : INSERT nueva categoría
    activate DB
    DB --> CatalogoService : Categoría creada
    deactivate DB
    
    CatalogoService --> AdminApp : 201 Created\n(CategoriaPrivateDTO)
else Categoría ya existe
    DB --> CatalogoService : Ya existe
    deactivate DB
    CatalogoService --> AdminApp : 409 Conflict
end

deactivate CatalogoService

== Listar Categorías ==
Administrador -> AdminApp : Consulta categorías
AdminApp -> CatalogoService : GET /api/catalogo/categorias
activate CatalogoService

CatalogoService -> DB : SELECT todas las categorías
activate DB
DB --> CatalogoService : Lista de categorías
deactivate DB

CatalogoService --> AdminApp : 200 OK\n[Lista de categorías]
deactivate CatalogoService

@enduml
```

## Arquitectura y Tecnologías

### Stack Tecnológico
- **Framework**: Spring Boot 3.x
- **Lenguaje**: Java 17+
- **Base de Datos**: MySQL/PostgreSQL (JPA/Hibernate)
- **Seguridad**: Spring Security con JWT
- **API**: RESTful API con Jackson
- **Build**: Maven

### Componentes principales

#### Controllers
- `VideoController`: Gestiona endpoints de videos
- `CategoriaController`: Gestiona endpoints de categorías

#### Services
- `VideoService`: Lógica de negocio para videos
- `CategoriaService`: Lógica de negocio para categorías

#### Repositories
- `VideoRepository`: Acceso a datos de videos (Spring Data JPA)
- `CategoriaRepository`: Acceso a datos de categorías (Spring Data JPA)

#### Security
- `JwtAuthenticationFilter`: Filtro de autenticación JWT
- `JwtTokenProvider`: Generación y validación de tokens
- `SecurityConfig`: Configuración de seguridad
- `CorsConfig`: Configuración de CORS

#### DTOs
- **Public DTOs**: Información expuesta a usuarios no autenticados
- **Private DTOs**: Información completa para administradores
- **Post DTOs**: Datos para creación/actualización de recursos
