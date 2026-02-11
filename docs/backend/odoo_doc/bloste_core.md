# Pasarela pagos

### Descripción
Servidor de Odoo para gestionar usuarios, suscripciones y métodos de pago. Incluye el módulo personalizado `bloste_core` que extiende la funcionalidad base de Odoo para adaptarla a las necesidades específicas de la plataforma BlosteFlix.

### Responsabilidades
+ Crear y enviar tokens de seguridad (JWT) para la interacción entre servicios
+ Gestionar altas, bajas, suspensiones y edición de perfiles de usuario
+ Validar métodos de pago y gestionar la información de tarjetas o cuentas asociadas a los usuarios
+ Registrar nuevos usuarios, autenticar credenciales y manejar el inicio de sesión para distintos roles
+ Crear, modificar y renovar planes de suscripción tanto desde la perspectiva del cliente como del administrador
+ Gestionar el historial de suscripciones de cada usuario
+ Calcular automáticamente fechas de caducidad de suscripciones
+ Controlar permisos y roles (usuario normal vs administrador)

### Interacción

Este componente interactúa con:
+ App Admin (Administrador de Contenidos)
+ Video Player (Reproductor de Videos)
+ Portal Web
+ Catálogo de Contenidos (validación de acceso)

## Módulo Bloste Core

### Descripción del Módulo
`bloste_core` es un módulo personalizado de Odoo que extiende la funcionalidad base del sistema para implementar la lógica de negocio específica de BlosteFlix. Este módulo gestiona usuarios, planes de suscripción y la relación entre ambos.

![Menú Bloste Software](../../assets/backend-odoo/bloste_core_menu.png)

### Componentes del Módulo

#### Modelos (models/)

##### bloste.subscription
Representa los planes de suscripción disponibles en la plataforma.

![Lista de Planes de Suscripción](../../assets/backend-odoo/bloste_subscription_list.png)

**Campos:**
- `name`: Nombre del plan (ej: "Plan Básico", "Plan Premium")
- `price`: Precio del plan de suscripción
- `duration`: Duración en días del plan (por defecto 30 días)
- `user_subscription_ids`: Relación con usuarios que tienen este plan
- `product_id`: Vinculación con producto de venta de Odoo
- `sale_order_id`: Orden de venta asociada
- `partner_id`: Cliente (heredado de sale_order)

**Responsabilidades:**
- Definir los diferentes planes de suscripción disponibles
- Mantener información de precios y duración
- Vincular con el sistema de ventas de Odoo

##### bloste.user_subscription
Tabla de relación entre usuarios y sus suscripciones (historial).

<!-- TODO: Imagen -->
![Historial de Suscripciones](../../assets/backend-odoo/bloste_user_subscription_list.png)

**Campos:**
- `user_id`: Usuario que tiene la suscripción
- `subscription_id`: Plan de suscripción asociado
- `start_date`: Fecha de inicio (por defecto hoy)
- `end_date`: Fecha de caducidad (calculada automáticamente)

**Métodos:**
- `_compute_end_date()`: Calcula automáticamente la fecha de caducidad sumando la duración del plan a la fecha de inicio

**Responsabilidades:**
- Mantener historial completo de suscripciones de cada usuario
- Calcular automáticamente fechas de vencimiento
- Permitir múltiples suscripciones por usuario (historial)

##### res.users (extensión)
Extiende el modelo de usuarios estándar de Odoo con funcionalidad específica de BlosteFlix.

![Formulario de Usuario Bloste](../../assets/backend-odoo/bloste_user_form.png)

**Campos añadidos:**
- `user_subscription_ids`: Relación con todas las suscripciones del usuario
- `bloste_api_uuid`: UUID único para identificación en API
- `bloste_status`: Estado del usuario ('user' o 'admin')
- `is_admin_bloste`: Indicador booleano de administrador
- `active_subscription_id`: Suscripción activa actual (calculado)
- `subscription_expiry_date`: Fecha de expiración de la suscripción activa (calculado)
- `new_subscription_id`: Campo auxiliar para asignar nuevas suscripciones
- `password_display`: Indicador visual de contraseña configurada

**Métodos clave:**
- `_compute_active_subscription()`: Determina cuál es la suscripción activa (la que caduca más pronto entre las válidas)
- `_compute_subscription_expiry()`: Obtiene la fecha de caducidad de la suscripción activa
- `_compute_password_display()`: Muestra un indicador visual de contraseña
- `_make_odoo_admin()`: Convierte un usuario en administrador de Odoo
- `_remove_odoo_admin()`: Quita permisos de administrador y convierte en usuario portal
- `create()`: Sobrescribe creación para usar email como login si no se proporciona
- `write()`: Gestiona la lógica de asignación de suscripciones y cambios de rol

**Responsabilidades:**
- Gestionar el estado de suscripción de cada usuario
- Calcular automáticamente la suscripción activa
- Controlar permisos según el rol (usuario/admin)
- Mantener sincronización entre estado BlosteFlix y permisos Odoo
- Gestionar asignación de nuevas suscripciones

##### product.template (extensión)
Extiende el modelo de productos de Odoo.

**Campos añadidos:**
- `is_subscription_product`: Marca si el producto es un plan de suscripción

**Responsabilidades:**
- Diferenciar productos de suscripción de otros productos
- Integrar suscripciones con el módulo de ventas de Odoo

#### Vistas (views/)

<!-- TODO: Imagen -->
![Estructura de Vistas](../../assets/backend-odoo/bloste_core_views_structure.png)

- **menu_view.xml**: Define el menú principal "Bloste Software" en la interfaz de Odoo
- **subscriptors.xml**: Vista para gestionar planes de suscripción
- **user_subscription.xml**: Vista para el historial de suscripciones de usuarios
- **res_users.xml**: Vista extendida de usuarios con campos personalizados
- **product_view.xml**: Vista extendida de productos para marcar planes de suscripción

#### Seguridad (security/)

<!-- TODO: Imagen -->
![Configuración de Seguridad](../../assets/backend-odoo/bloste_core_security_csv.png)

**ir.model.access.csv**: Define los permisos de acceso a los modelos:
- `access_bloste_subscription`: Permisos completos (CRUD) para usuarios internos
- `access_bloste_user_subscription`: Permisos completos (CRUD) para usuarios internos
- `access_bloste_res_users`: Permisos completos (CRUD) para gestión de usuarios

### Dependencias

El módulo `bloste_core` depende de:
- `base`: Módulo base de Odoo (usuarios, grupos, permisos)
- `sale`: Módulo de ventas (órdenes, productos)
- `product`: Módulo de productos

### Configuración del Manifiesto

```python
{
    'name': 'Bloste-Software',
    'version': '1.0',
    'summary': 'Bloste Software Core Module',
    'description': 'Módulo para la gestión de suscripciones y usuarios, 
                    y creación y validación de tokens',
    'author': 'Bloste Team',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'product'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

## Diagrama E-R

```plantuml
@startuml
' Modelo de usuario extendido
entity res_users {
  +id : int <<PK>>
  --
  login : varchar <<U>>
  password : varchar
  name : varchar
  email : varchar
  active : boolean
  created_at : datetime
  --
  **Campos Bloste**
  bloste_api_uuid : varchar
  bloste_status : enum
  is_admin_bloste : boolean
  active_subscription_id : int <<FK>>
  subscription_expiry_date : date
}

' Modelo de roles (base Odoo)
entity res_groups {
  +id : int <<PK>>
  --
  name : varchar
  category_id : int
}

' Modelo de planes de suscripción
entity bloste_subscription {
  +id : int <<PK>>
  --
  name : varchar
  price : decimal
  duration : int
  --
  product_id : int <<FK>>
  sale_order_id : int <<FK>>
  partner_id : int <<FK>>
}

' Modelo de relación usuario-suscripción (historial)
entity bloste_user_subscription {
  +id : int <<PK>>
  --
  start_date : date
  end_date : date (computed)
  --
  user_id : int <<FK>>
  subscription_id : int <<FK>>
}

' Modelo de métodos de pago
entity payment_method {
  +id : int <<PK>>
  --
  name : varchar
  description : varchar
}

' Modelo de pagos
entity payment {
  +id : int <<PK>>
  --
  amount : decimal
  currency : varchar
  status : enum
  paid_at : datetime
  created_at : datetime
  --
  payment_method_id : int <<FK>>
  subscription_id : int <<FK>>
}

' Modelo de productos (extendido)
entity product_product {
  +id : int <<PK>>
  --
  name : varchar
  list_price : decimal
  --
  **Campos Bloste**
  is_subscription_product : boolean
}

' Modelo de órdenes de venta
entity sale_order {
  +id : int <<PK>>
  --
  name : varchar
  date_order : datetime
  state : enum
  amount_total : decimal
  --
  partner_id : int <<FK>>
}

' Modelo de clientes/partners
entity res_partner {
  +id : int <<PK>>
  --
  name : varchar
  email : varchar
  phone : varchar
}

' ===========================
' RELACIONES PRINCIPALES
' ===========================

' Usuario tiene múltiples suscripciones (historial)
res_users ||--o{ bloste_user_subscription : "tiene historial"

' Usuario tiene una suscripción activa
res_users }o--|| bloste_subscription : "suscripción activa"

' Plan de suscripción usado en múltiples user_subscriptions
bloste_subscription ||--o{ bloste_user_subscription : "usado en"

' Grupos/roles de usuarios
res_users }o--o{ res_groups : "pertenece a"

' Suscripción vinculada a producto
bloste_subscription }o--|| product_product : "vinculada a"

' Suscripción vinculada a orden de venta
bloste_subscription }o--|| sale_order : "generada por"

' Orden de venta pertenece a cliente
sale_order }o--|| res_partner : "pertenece a"

' Pagos generados por suscripciones
bloste_subscription ||--o{ payment : "genera"

' Pagos usan método de pago
payment }o--|| payment_method : "usa"

note right of res_users
  bloste_status:
  - user (Usuario Normal)
  - admin (Administrador)
  
  active_subscription_id:
  Se calcula automáticamente como
  la suscripción con fecha de
  caducidad más próxima (válida)
end note

note right of bloste_user_subscription
  end_date se calcula automáticamente:
  end_date = start_date + duration
  
  Permite mantener historial completo
  de todas las suscripciones del usuario
end note

note right of bloste_subscription
  duration: días de duración
  (por defecto 30 días)
end note

note right of payment
  status:
  - PENDING
  - PAID
  - FAILED
  - REFUNDED
end note

note right of sale_order
  state:
  - draft
  - sent
  - sale
  - done
  - cancel
end note

@enduml
```

## Modelo de Datos

### res.users (extendido)
Usuarios del sistema con funcionalidad específica de BlosteFlix.

**Campos estándar:**
- `id`: Identificador único
- `login`: Nombre de usuario para autenticación
- `password`: Contraseña encriptada
- `name`: Nombre completo
- `email`: Correo electrónico
- `active`: Indica si el usuario está activo

**Campos BlosteFlix:**
- `bloste_api_uuid`: UUID para identificación en API externa
- `bloste_status`: Estado del usuario ('user' o 'admin')
- `is_admin_bloste`: Indica si es administrador de BlosteFlix
- `active_subscription_id`: Referencia a la suscripción activa actual
- `subscription_expiry_date`: Fecha de caducidad calculada
- `user_subscription_ids`: Historial completo de suscripciones

### bloste.subscription
Planes de suscripción disponibles en la plataforma.

![Formulario de Plan de Suscripción](../../assets/backend-odoo/bloste_subscription_form.png)

**Campos:**
- `id`: Identificador único del plan
- `name`: Nombre del plan (ej: "Plan Mensual", "Plan Anual")
- `price`: Precio del plan
- `duration`: Duración en días (por defecto 30)
- `product_id`: Vinculación con producto de Odoo
- `sale_order_id`: Orden de venta asociada
- `partner_id`: Cliente (heredado de sale_order)
- `user_subscription_ids`: Usuarios que tienen/tuvieron este plan

### bloste.user_subscription
Historial de suscripciones de usuarios (relación usuario-plan).

<!-- TODO: Imagen -->
![Formulario de Suscripción de Usuario](../../assets/backend-odoo/bloste_user_subscription_form.png)

**Campos:**
- `id`: Identificador único de la relación
- `user_id`: Usuario asociado
- `subscription_id`: Plan de suscripción asociado
- `start_date`: Fecha de inicio (por defecto hoy)
- `end_date`: Fecha de caducidad (calculada automáticamente)

**Lógica de cálculo:**
- `end_date = start_date + duration` (de la suscripción)

### product.product (extendido)
Productos de Odoo extendidos para soportar suscripciones.

**Campos añadidos:**
- `is_subscription_product`: Marca si el producto representa un plan de suscripción

### payment_method
Métodos de pago disponibles.

**Campos:**
- `id`: Identificador único
- `name`: Nombre del método (ej: "Tarjeta de Crédito", "PayPal")
- `description`: Descripción del método

### payment
Historial de pagos realizados.

**Campos:**
- `id`: Identificador único
- `amount`: Monto del pago
- `currency`: Moneda (ej: "EUR", "USD")
- `status`: Estado del pago (PENDING, PAID, FAILED, REFUNDED)
- `paid_at`: Fecha y hora del pago
- `payment_method_id`: Método de pago utilizado
- `subscription_id`: Suscripción asociada


<!-- TODO: Revisar casos de uso, no se entiende nada, igual con plantuml es mejor -->
## Casos de uso

```mermaid
%%{init: {'theme':'base','themeVariables': {'primaryColor':'#0ea5a4','edgeColor':'#065f46','fontFamily':'"Inter", Arial'}} }%%
graph LR
  %% Agrupación de usuarios
  subgraph Usuarios
    direction TB
    U1[Usuario/Cliente]
    U2[Administrador]
    U3[Portal Web]
    U4[Video Player]
  end

  %% Casos de uso divididos en áreas
  subgraph "Casos de uso"
    direction LR
    
    subgraph "Gestión de Usuarios"
      direction TB
      UC1((Crear usuario))
      UC2((Autenticar usuario))
      UC3((Editar perfil))
      UC4((Cambiar contraseña))
      UC5((Activar/Desactivar))
    end

    subgraph "Gestión de Suscripciones"
      direction TB
      UC6((Crear plan suscripción))
      UC7((Asignar suscripción))
      UC8((Renovar suscripción))
      UC9((Consultar estado))
      UC10((Ver historial))
      UC11((Cancelar suscripción))
    end

    subgraph "Gestión de Roles"
      direction TB
      UC12((Asignar admin))
      UC13((Revocar admin))
      UC14((Gestionar permisos))
    end

    subgraph "Gestión de Pagos"
      direction TB
      UC15((Registrar método pago))
      UC16((Procesar pago))
      UC17((Consultar pagos))
      UC18((Reembolsar))
    end
    
    subgraph "Integración API"
      direction TB
      UC19((Generar JWT))
      UC20((Validar token))
      UC21((Consultar suscripción activa))
    end
  end

  %% Relaciones - Usuario Cliente
  U1 -->|POST| UC1
  U1 -->|POST| UC2
  U1 -->|PUT| UC3
  U1 -->|PUT| UC4
  U1 -->|GET| UC9
  U1 -->|POST| UC15
  U1 -->|GET| UC17

  %% Relaciones - Administrador
  U2 -->|POST/PUT| UC1
  U2 -->|POST/PUT| UC5
  U2 -->|POST/PUT| UC6
  U2 -->|POST| UC7
  U2 -->|GET| UC10
  U2 -->|POST| UC12
  U2 -->|POST| UC13
  U2 -->|POST/PUT| UC14
  U2 -->|POST| UC16
  U2 -->|GET| UC17
  U2 -->|POST| UC18

  %% Relaciones - Portal Web
  U3 -->|POST| UC2
  U3 -->|POST| UC8
  U3 -->|POST| UC16
  U3 -->|GET| UC9

  %% Relaciones - Video Player
  U4 -->|POST| UC19
  U4 -->|POST| UC20
  U4 -->|GET| UC21

  %% Estilos
  class U1,U2,U3,U4 usernode
  class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10,UC11,UC12,UC13,UC14,UC15,UC16,UC17,UC18,UC19,UC20,UC21 usecase

  classDef usernode fill:#e0f2fe,stroke:#0369a1,stroke-width:2px,rx:8px;
  classDef usecase fill:#ecfccb,stroke:#65a30d,stroke-width:1.5px,rx:20px;
```

## Diagramas de flujo

### Autenticación y Generación de Token

```plantuml
@startuml
actor Actor
participant PasarelaPagos
participant DB_Odoo

Actor -> PasarelaPagos : POST /api/auth/login\n(user, password)
activate PasarelaPagos

PasarelaPagos -> DB_Odoo : Buscar Persona por username
activate DB_Odoo
DB_Odoo --> PasarelaPagos : Datos Persona (hash_password, rol)
deactivate DB_Odoo

PasarelaPagos -> PasarelaPagos : Validar password
PasarelaPagos -> PasarelaPagos : Generar Token de Seguridad (JWT)

alt Credenciales válidas
    PasarelaPagos --> Actor : 200 OK (Token + Rol)
else Credenciales incorrectas
    PasarelaPagos --> Actor : 401 Unauthorized
else Cuenta suspendida
    PasarelaPagos --> Actor : 403 Forbidden
end

deactivate PasarelaPagos
@enduml
```

### Gestión de Suscripción y Pago

```plantuml
@startuml
actor Usuario
participant PasarelaPagos
participant PasarelaExterna as "Pasarela Externa (Stripe/PayPal)"
participant DB_Odoo

Usuario -> PasarelaPagos : POST /api/suscripcion/renovar\n(plan_id, token)
activate PasarelaPagos

PasarelaPagos -> PasarelaPagos : Validar Token
PasarelaPagos -> DB_Odoo : Obtener METODO_PAGO del usuario
activate DB_Odoo
DB_Odoo --> PasarelaPagos : Detalles del pago
deactivate DB_Odoo

PasarelaPagos -> PasarelaExterna : Procesar cobro (importe, detalles)
activate PasarelaExterna

alt Cobro exitoso
    PasarelaExterna --> PasarelaPagos : Confirmación transacción
    PasarelaPagos -> DB_Odoo : Actualizar SUSCRIPCION\n(fecha_fin)
    PasarelaPagos --> Usuario : 200 OK (Suscripción actualizada)
else Fondos insuficientes / Error tarjeta
    PasarelaExterna --> PasarelaPagos : Error cobro
    PasarelaPagos --> Usuario : 402 Payment Required
end

deactivate PasarelaExterna
deactivate PasarelaPagos
@enduml
```

### Asignar Suscripción a Usuario (Módulo Bloste Core)

```plantuml
@startuml
actor Administrador
participant "Odoo Interface" as UI
participant "ResUsers Model" as Users
participant "UserSubscription Model" as UserSub
database "Base de Datos" as DB

Administrador -> UI : Selecciona usuario\ny plan de suscripción
UI -> UI : Campo new_subscription_id\nestablecido

Administrador -> UI : Guarda cambios
UI -> Users : write({'new_subscription_id': plan_id})
activate Users

Users -> Users : Validar datos

Users -> UserSub : create({\n  user_id: user.id,\n  subscription_id: plan_id,\n  start_date: today()\n})
activate UserSub

UserSub -> UserSub : _compute_end_date()
note right
  end_date = start_date + 
  subscription.duration
end note

UserSub -> DB : INSERT bloste_user_subscription
activate DB
DB --> UserSub : Registro creado
deactivate DB

UserSub --> Users : Suscripción creada
deactivate UserSub

Users -> Users : _compute_active_subscription()
note right
  Recalcula cuál es la 
  suscripción activa
end note

Users -> Users : _compute_subscription_expiry()
note right
  Actualiza fecha de 
  caducidad visible
end note

Users -> Users : new_subscription_id = False
note right
  Limpia el campo auxiliar
end note

Users -> DB : UPDATE res_users
activate DB
DB --> Users : Usuario actualizado
deactivate DB

Users --> UI : 200 OK
deactivate Users
UI --> Administrador : Confirmación\n"Suscripción asignada correctamente"

@enduml
```

### Calcular Suscripción Activa

```plantuml
@startuml
participant "Sistema" as Sys
participant "ResUsers Model" as Users
participant "UserSubscription Model" as UserSub
database "Base de Datos" as DB

Sys -> Users : Acceso a usuario\n(lectura de active_subscription_id)
activate Users

Users -> Users : @api.depends trigger\n(_compute_active_subscription)

Users -> UserSub : Obtener user_subscription_ids
activate UserSub
UserSub -> DB : SELECT * FROM bloste_user_subscription\nWHERE user_id = {id}
activate DB
DB --> UserSub : Lista de suscripciones
deactivate DB
UserSub --> Users : user.user_subscription_ids
deactivate UserSub

Users -> Users : Filtrar suscripciones válidas
note right
  valid_subs = suscripciones
  donde end_date >= today()
end note

alt Hay suscripciones válidas
    Users -> Users : Ordenar por end_date (ascendente)
    Users -> Users : active_sub = primera del listado
    note right
      La que caduca más pronto
      es la suscripción activa
    end note
    Users -> Users : active_subscription_id = active_sub.subscription_id
else No hay suscripciones válidas
    Users -> Users : active_subscription_id = None
end

Users --> Sys : active_subscription_id
deactivate Users

@enduml
```

### Cambiar Rol de Usuario (User a Admin)

```plantuml
@startuml
actor Administrador
participant "Odoo Interface" as UI
participant "ResUsers Model" as Users
database "Base de Datos" as DB

Administrador -> UI : Marca usuario como Admin
UI -> Users : write({'bloste_status': 'admin'})
activate Users

Users -> Users : Detectar cambio en bloste_status

alt bloste_status == 'admin'
    Users -> Users : Establecer is_admin_bloste = True
    
    Users -> Users : _make_odoo_admin(user)
    activate Users
    
    Users -> Users : Obtener grupos de Odoo
    note right
      internal_user_group
      portal_group
      system_group
    end note
    
    Users -> DB : UPDATE res_users_groups_rel\nRemove: portal_group\nAdd: internal_user_group\nAdd: system_group
    activate DB
    DB --> Users : Grupos actualizados
    deactivate DB
    
    Users --> Users : Usuario convertido a Admin
    deactivate Users
    
    Users -> DB : UPDATE res_users SET\nbloste_status='admin',\nis_admin_bloste=true
    activate DB
    DB --> Users : Actualizado
    deactivate DB
end

Users --> UI : 200 OK
deactivate Users
UI --> Administrador : "Usuario promovido a Administrador"

note right of Users
  El usuario ahora tiene:
  - Acceso completo a Odoo (system_group)
  - Permisos de usuario interno
  - No es usuario portal
  - Estado admin en BlosteFlix
end note

@enduml
```

### Crear Usuario Nuevo

```plantuml
@startuml
actor Actor
participant "Sistema/API" as API
participant "ResUsers Model" as Users
database "Base de Datos" as DB

Actor -> API : POST /api/users/create\n(name, email, password)
API -> Users : create(vals)
activate Users

Users -> Users : Validar datos

alt login no proporcionado
    Users -> Users : login = vals['email']
    note right
      Si no hay login, 
      usar email como login
    end note
end

Users -> Users : Hash de contraseña

Users -> DB : INSERT INTO res_users
activate DB
DB --> Users : Usuario creado (ID)
deactivate DB

Users -> Users : Asignar grupo por defecto
note right
  Por defecto: group_portal
  (usuario básico)
end note

Users -> DB : INSERT permisos/grupos
activate DB
DB --> Users : Permisos asignados
deactivate DB

Users -> Users : Establecer valores por defecto
note right
  bloste_status = 'user'
  is_admin_bloste = False
  active = True
end note

Users --> API : Usuario creado (ID, datos)
deactivate Users
API --> Actor : 201 Created\n(usuario_id, email, name)

@enduml
```

### Consultar Estado de Suscripción (API Externa)

```plantuml
@startuml
participant "Video Player" as VP
participant "API Gateway" as API
participant "Odoo/Bloste Core" as Odoo
database "Base de Datos" as DB

VP -> API : GET /api/user/{uuid}/subscription\n(JWT Token)
activate API

API -> API : Validar JWT Token

alt Token válido
    API -> Odoo : Consultar usuario por UUID
    activate Odoo
    
    Odoo -> DB : SELECT * FROM res_users\nWHERE bloste_api_uuid = {uuid}
    activate DB
    DB --> Odoo : Datos del usuario
    deactivate DB
    
    Odoo -> Odoo : Acceder a active_subscription_id
    note right
      Dispara _compute_active_subscription()
      automáticamente
    end note
    
    Odoo -> Odoo : Acceder a subscription_expiry_date
    note right
      Dispara _compute_subscription_expiry()
      automáticamente
    end note
    
    alt Usuario tiene suscripción activa
        Odoo --> API : {\n  has_subscription: true,\n  plan_name: "...",\n  expiry_date: "YYYY-MM-DD",\n  is_admin: false/true\n}
        API --> VP : 200 OK (datos suscripción)
    else Usuario sin suscripción activa
        Odoo --> API : {\n  has_subscription: false,\n  expiry_date: null\n}
        API --> VP : 200 OK (sin suscripción)
    end
    
    deactivate Odoo
else Token inválido
    API --> VP : 401 Unauthorized
end

deactivate API

@enduml
```

## Arquitectura y Tecnologías

### Stack Tecnológico
- **Framework**: Odoo 16/17
- **Lenguaje**: Python 3.8+
- **Base de Datos**: PostgreSQL
- **ORM**: Odoo ORM
- **API**: RESTful API / XML-RPC / JSON-RPC
- **Autenticación**: JWT + Odoo Session

### Módulos de Odoo Utilizados
- **base**: Funcionalidad base (usuarios, grupos, permisos)
- **sale**: Gestión de ventas y órdenes
- **product**: Gestión de productos
- **portal**: Funcionalidad de portal para usuarios externos

### Componentes del Módulo Bloste Core

#### Models (Lógica de negocio)
- `bloste.subscription`: Planes de suscripción
- `bloste.user_subscription`: Historial usuario-suscripción
- `res.users (inherit)`: Extensión del modelo de usuarios
- `product.template (inherit)`: Extensión de productos

#### Views (Interfaz de usuario)
- Formularios y listas para gestión de suscripciones
- Vistas personalizadas de usuarios con campos Bloste
- Menús de navegación personalizados

#### Security (Control de acceso)
- Reglas de acceso basadas en grupos de Odoo
- Permisos CRUD granulares por modelo

#### Computed Fields
- **active_subscription_id**: Calcula automáticamente la suscripción activa del usuario
- **subscription_expiry_date**: Calcula la fecha de expiración de la suscripción activa
- **end_date** (en user_subscription): Calcula la fecha de fin basada en duración

### Flujo de Datos

1. **Creación de plan**: Admin crea `bloste.subscription` con precio y duración
2. **Asignación**: Admin usa `new_subscription_id` en usuario
3. **Registro automático**: Se crea `bloste.user_subscription` con fecha de inicio
4. **Cálculo de caducidad**: `end_date` se calcula automáticamente
5. **Actualización de estado**: `active_subscription_id` se actualiza automáticamente
6. **Consulta externa**: APIs consultan `active_subscription_id` y `subscription_expiry_date`

### Seguridad y Permisos

#### Grupos de Odoo

<!-- TODO: Imagen -->
![Configuración de Grupos Odoo](../../assets/backend-odoo/bloste_core_groups_config.png)

- **Portal User** (`base.group_portal`): Usuario básico con acceso limitado
- **Internal User** (`base.group_user`): Usuario interno con acceso a backend
- **System Administrator** (`base.group_system`): Administrador con acceso completo

#### Sincronización de Roles
- Usuario con `bloste_status='admin'` → Se asignan grupos de administrador de Odoo
- Usuario con `bloste_status='user'` → Se mantiene como usuario portal

### Integraciones

#### API REST/JSON-RPC
- Consulta de estado de suscripción por UUID
- Validación de tokens JWT
- Sincronización con servicios externos (Video Player, Admin App)

#### Sistema de Ventas
- Vinculación de suscripciones con productos de Odoo
- Generación de órdenes de venta
- Tracking de pagos y renovaciones
