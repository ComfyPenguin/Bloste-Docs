# Pasarela pagos

## Descripción

Servidor de Odoo para gestionar usuarios, suscripciones y metodos de pago.

## Responsabilidades

+ Crear y enviar tokens de seguridad para la interacción entre servicios
+ Gestionar altas, bajas, suspensiones y edición de perfiles
+ Validar métodos de pago y gestionar la información de tarjetas o cuentas asociadas a los usuarios
+ Registrar nuevos usuarios, autenticar credenciales y manejar el inicio de sesión para distintos roles
+ Crear, modificar y renovar planes de suscripción tanto desde la perspectiva del cliente como del administrador

## Interacion

Este componente interactua con:

+ Admin App
+ Video Player
+ Portal web

## Endpoints

***Por definir***

## Diagrama E-R

```plantuml
@startuml
entity user {
  +id : int <<PK>>
  --
  username : varchar <<U>>
  password_hash : varchar
  name : varchar
  surname : varchar
  email : varchar
  is_active : boolean
  created_at : datetime
}

entity role {
  +id : int <<PK>>
  --
  name : varchar
  description : varchar
}

entity user_role {
  +user_id : int <<FK>>
  +role_id : int <<FK>>
}

entity subscription_plan {
  +id : int <<PK>>
  --
  name : varchar
  price : decimal
  billing_period : enum
  description : varchar
  is_active : boolean
}

entity subscription {
  +id : int <<PK>>
  --
  start_date : date
  end_date : date
  status : enum
  auto_renew : boolean
  created_at : datetime
  --
  user_id : int <<FK>>
  plan_id : int <<FK>>
}

entity payment_method {
  +id : int <<PK>>
  --
  name : varchar
  description : varchar
}

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

user ||--o{ subscription : tiene
subscription }o--|| subscription_plan : usa
subscription ||--o{ payment : genera

user ||--o{ user_role
role ||--o{ user_role

payment }o--|| payment_method : usa

note right of subscription_plan
  billing_period:
  - MONTHLY
  - YEARLY
  - LIFETIME
end note

note right of subscription
  status:
  - ACTIVE
  - PAUSED
  - CANCELLED
  - EXPIRED
end note

note right of payment
  status:
  - PENDING
  - PAID
  - FAILED
  - REFUNDED
end note

@enduml
```

## Casos de uso

```mermaid
flowchart LR

    Usuario[👤 Usuario]
    Admin[🛠️ Administrador]
    subgraph Sistema Suscripciones
        UC1(Registrarse)
        UC2(Gestionar Método de Pago)
        UC3(Gestionar Suscripción)
        UC4(Iniciar Sesión)
        UC5(Gestionar Usuarios)
        UC6(Gestionar Roles)
        UC7(Gestionar Suscripciones)
        UC8(Asignar Roles a 
        Administradores)
    end

    Usuario --> UC1
    Usuario --> UC2
    Usuario --> UC3
    Usuario --> UC4

    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
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
participant PasarelaExterna as "Pasarela Extrana (Stripe/PayPal)"
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
