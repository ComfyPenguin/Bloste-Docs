# Diagramas Entidad Relación

## Catálogo de contenidos

```mermaid
erDiagram
    VIDEO {
        int id PK
        string titulo
        int duracion
        string thumbnail
        string url
        string creador
    }

    GENERO {
        int id PK
        string tipo
    }

    VIDEO_GENERO {
        int video_id FK
        int genero_id FK
    }

    VIDEO ||--o{ VIDEO_GENERO : "tiene"
    GENERO ||--o{ VIDEO_GENERO : "clasifica"
    VIDEO }o--o{ GENERO : "muchos_a_muchos"
```
