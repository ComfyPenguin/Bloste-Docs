# Backend catálogo

Documentación del backend catálogo.

## Endpoints

### Endpoints GET

+ `api/catalogo` : Recibe todo el catálogo de vídeos
+ `api/catalogo/:id` : Recibe todo el catálogo de vídeos
+ `api/catalogo/:categoria` : Recibe una lista de videos de la categoría especificada
+ `api/catalogo/:titulo` : Recibe un vídeo del título especificado

### Endpoints POST

+ `api/catalogo/:id` : Sube los datos de un video al catálogo

### Endpoints PUT

+ `api/catalogo/:id` : Modifica los datos de un vídeo

## CASOS DE USO

```mermaid
%%{init: {'theme':'base','themeVariables': {'primaryColor':'#0ea5a4','edgeColor':'#065f46','fontFamily':'"Inter", Arial'}} }%%
graph LR
  %% Agrupación de usuarios
  subgraph Usuarios
    direction TB
    U2[👤 App Usuario]
    U3[🛠️ App Admin]
  end

  %% Casos de uso divididos en dos áreas
  subgraph "Casos de uso"
    direction LR
    subgraph Consulta
      direction TB
      UC2((🔎 Consultar catálogo completo))
      UC3((📂 Consultar por categoría))
      UC4((🔤 Consultar por título))
    end

    subgraph "Administración"
      direction TB
      UC5((⬆️ Subir video))
      UC6((✏️ Modificar video))
      UC7((🗑️ Eliminar video))
    end
  end

  %% Relaciones
  U2 --> UC2
  U2 --> UC3
  U2 --> UC4

  U3 --> UC5
  U3 --> UC6
  U3 --> UC7

  %% Estilos
  class U2,U3 usernode
  class UC2,UC3,UC4,UC5,UC6,UC7 usecase

  classDef usernode fill:#e0f2fe,stroke:#0369a1,stroke-width:2px,rx:8px;
  classDef usecase fill:#ecfccb,stroke:#65a30d,stroke-width:1.5px,rx:20px;
```

## Diagrama Entidad Relación

```plantuml
@startuml

entity video {
  +id : int <<PK>>
  --
  creator : varchar
  title : varchar
  description : text
  duration_seconds : int
  url_video : varchar
  url_thumbnail : varchar
  uppload_date : datetime
  is_hidden : boolean
}

entity category {
  +id : int <<PK>>
  --
  name : varchar
  description : varchar
}

entity video_category {
  +video_id : int <<FK>>
  +category_id : int <<FK>>
}

' ===========================
' RELACIONES
' ===========================

video ||--o{ video_category
category ||--o{ video_category

@enduml
```
