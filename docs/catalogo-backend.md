
# Backend catálogo
Documentación del backend catálogo.
## ENDPOINTS:
```
        BUSCAR TODO         --> api/catalogo
GET:    BUSCAR POR CATEGORÍA--> api/catalogo/categoria
        BUSCAR POR TITULO   --> api/catalogo/titulo

POST:   SUBIR ENTRADA-CATALOGO--> api/catalogo/:id

PUT:   MODIFICAR VIDEO--> api/catalogo/:id

DELETE:   ELIMINAR VIDEO--> api/catalogo/:id
```
## CASOS DE USO
``` mermaid
graph TD
    U2[Usuario: App Usuario]
    U3[Usuario: App Admin]
    
    UC2[Consultar catálogo completo]
    UC3[Consultar por categoría]
    UC4[Consultar por título]
    
    U2 --> UC2
    U2 --> UC3
    U2 --> UC4
    
    UC5[Subir video]
    UC6[Modificar video]
    UC7[Eliminar video]
    
    U3 --> UC5
    U3 --> UC6
    U3 --> UC7
```
## Diagrama Entidad Relación

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