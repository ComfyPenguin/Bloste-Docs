# Bienvenido a la documentacion de Blosteflix

Blosteflix es un proyecto de desarrollo de una app al estilo Netflix.
Esta formado por varios componentes cada uno con su responsabilidad, entre ellos tenemos:

+ Repoductor video, hecho en Flutter
+ Un gestor de los videos subidos a la plataforma, hecho en Vue
+ Un servidor API REST que muestra el catálogo, hecho en Spring
+ Un servidor de contenido HLS, hecho en hls
+ Y a futuro una pasarela de pagos administrada mediante Odoo.

## Diagrama C4

```mermaid
C4Context
title Diagrama C4 – Nivel 1 (Contexto) – blosteflix

Person(usuario, "👤 Usuario", "Consume contenido en streaming")
Person(admin, "🛠️ Administrador", "Gestiona vídeos, catálogo y usuarios")

System(blosteflix, "🎬 blosteflix", "Plataforma de streaming de vídeo bajo demanda")

System_Ext(videoServer, "📹 Servidor de Vídeo", "Almacena y sirve contenido multimedia (HLS)")
System_Ext(catalogo, "📚 Servidor de Catálogo (Spring Boot)", "Gestiona metadatos de películas y series")
System_Ext(pagos, "💳 Pasarela de Pagos (Odoo)", "Gestión de pagos y suscripciones")

Rel(usuario, blosteflix, "Reproduce vídeos, gestiona su suscripción")
Rel(admin, blosteflix, "Administra vídeos y catálogo")

Rel(blosteflix, videoServer, "Solicita playlists y segmentos HLS")
Rel(blosteflix, catalogo, "Consulta y gestiona metadatos")
Rel(blosteflix, pagos, "Gestiona pagos y suscripciones")
```

```mermaid
C4Container
title Diagrama C4 – Nivel 2 (Contenedores) – blosteflix

Person(usuario, "👤 Usuario", "Consume contenido en streaming")
Person(admin, "🛠️ Administrador", "Gestiona vídeos, catálogo y usuarios")

System_Boundary(blosteflix, "🎬 blosteflix") {

    Container(appClient, "📱 App Cliente", "Web / App móvil", "Reproducción de vídeo y navegación del catálogo")
    Container(appAdmin, "🧑‍💼 App Administrador", "Aplicación web", "Gestión de vídeos, usuarios y catálogo")

    Container(catalogoApi, "📚 Servidor de Catálogo", "API Spring Boot", "Gestión de metadatos de películas y series")
    Container(mediaServer, "📹 Media Server", "Node.js + Express", "Almacenamiento y streaming HLS")
}

System_Ext(pagos, "💳 Pasarela de Pagos", "Odoo", "Gestión de pagos y suscripciones")

ContainerDb(catalogoDb, "🗄️ BD Catálogo", "PostgreSQL", "Metadatos del contenido")
ContainerDb(mediaDb, "🗄️ BD Media", "Sistema de ficheros / BD", "Vídeos y segmentos HLS")
ContainerDb(pagosDb, "🗄️ BD Pagos", "PostgreSQL", "Pagos y suscripciones")

Rel(usuario, appClient, "Utiliza")
Rel(admin, appAdmin, "Utiliza")

Rel(appClient, catalogoApi, "Consulta catálogo (REST)")
Rel(appClient, mediaServer, "Reproduce vídeo (HLS)")

Rel(appAdmin, catalogoApi, "Gestiona metadatos (REST)")
Rel(appAdmin, mediaServer, "Sube vídeos")

Rel(catalogoApi, catalogoDb, "Lee / Escribe")
Rel(mediaServer, mediaDb, "Almacena contenido")

Rel(appClient, pagos, "Gestiona suscripción")
Rel(appAdmin, pagos, "Gestión administrativa")
Rel(pagos, pagosDb, "Persistencia")

```

```mermaid
C4Component
title Diagrama C4 – Nivel 3 – Componentes del Servidor de Catálogo

Container(catalogoApi, "📚 Servidor de Catálogo", "Spring Boot", "Gestión de metadatos del contenido")

Component(controller, "🎮 Controllers REST", "Spring MVC", "Exponen endpoints del catálogo")
Component(service, "🧠 Servicios de Dominio", "Spring Service", "Lógica de negocio del catálogo")
Component(repository, "🗄️ Repositorios", "Spring Data JPA", "Acceso a datos")
Component(search, "🔍 Motor de Búsqueda", "JPA / Queries", "Búsqueda y filtrado de contenidos")

ContainerDb(db, "🗄️ BD Catálogo", "PostgreSQL", "Metadatos")

Rel(controller, service, "Llama")
Rel(service, repository, "Usa")
Rel(service, search, "Consulta")
Rel(repository, db, "Lee / Escribe")

Rel_U(catalogoApi, controller, "HTTP REST")

```

```mermaid
C4Component
title Diagrama C4 – Nivel 3 – Componentes del Media Server

Container(mediaServer, "📹 Media Server", "Node.js + Express", "Gestión y streaming de vídeo HLS")

Component(upload, "⬆️ Upload Controller", "Express Route", "Recepción de archivos de vídeo")
Component(metadata, "📊 Metadata Extractor", "FFmpeg", "Extracción de metadatos técnicos")
Component(hls, "📦 HLS Processor", "FFmpeg", "Segmentación y generación HLS")
Component(stream, "▶️ Streaming Controller", "Express Route", "Entrega de playlists y segmentos")
Component(storage, "💾 Storage Manager", "Filesystem", "Gestión de archivos de vídeo")

ContainerDb(fs, "🗄️ Almacenamiento", "Filesystem", "Vídeos originales y HLS")

Rel(upload, metadata, "Extrae metadatos")
Rel(upload, storage, "Guarda vídeo original")
Rel(metadata, hls, "Inicia procesamiento")
Rel(hls, storage, "Genera segmentos HLS")
Rel(stream, storage, "Lee playlists y segmentos")
Rel(storage, fs, "Persiste archivos")

Rel_U(mediaServer, upload, "HTTP POST")
Rel_U(mediaServer, stream, "HTTP GET (HLS)")

```

## Requisitos funcionales y no funcionales
### Requisitos funcionales
#### Funciones específicas
+ Se debe permitir a los usuarios registrarse con username y contraseña.
+ Se debe permitir a todos los usuarios registrados ver el catálogo.

+ Se debe subir el video a la base de datos cuando se confirma y estar disponible en el catálogo.
+ Se debe restringir que solo los administradores den de alta a nuevos administradores.
+ Se debe restingir que solo los usuarios accedan a la app reproductor y catálogo y que solo los administradores accedan a la app de administrador
+ Los permisos de los administradores se dividen en roles, permiso de videos y permiso de usuarios.


+ Se debe validar la subscripción del usuario con cada interacción relacionada con reproducir video.
+ Se debe cambiar el estado de la subscripción del usuario cuando haga una modificación en su subscripción.
+ Se debe permitir el pago con targeta.

#### Reglas de negocio
+ Al clicar en una portada del catálogo que debe llevar una página con el video con los detalles del video.
+ Al clicar en el play de un video debe mostrar las opciones, pantalla completa, parar el video, barra de duración.
+ El titulo de la barra de navegación debe mostrar el catálogo.
+ El botón categorías debe abrir un desplegable con todos los tipos de video y al clicar en uno mostrarte un catálogo con solo los videos que contengan esa categoría.
+ Al hacer clic en buscar debe aparecer una barra buscadora que busque por título o por fragmento de título.

### Requisitos no funcionales

+ Rendimiento, que cargue el video en menos de 5 segundos.
+ Escalabilidad, el código y la base de datos puedan crecer al ritmo de la aplicación de manera fácil.
+ Seguridad Básica, que todo el tráfico sea a través del protocolo HTTPS, que las contraseñas encriptadas en la base de datos y un sistema de login seguro con tokens que expiran.
+ Compatibilidad, que sea compatible en diferentes navegadores y SO de móviles.