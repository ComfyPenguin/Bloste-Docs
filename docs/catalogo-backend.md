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