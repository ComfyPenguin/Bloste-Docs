# Gestor suscripcions web
Portal web que gestiona las suscripciones

### Que hace ?
+ Registra nuevos ususarios en el sistema Odoo
+ Inicio de sesión y autenticación contra Odoo
+ Visualización pública selección y alta de los tipos de suscripciones y precios
+ Introducción y modificación de métodos de pago
+ Consulta del estado actual de la suscripción
+ Trámite para dar de baja el servicio

### Interacción
Según el diagrama, este componente interactúa con:
+ Login Odoo

### Endpoints

***Por definir***

## Casos de uso
```mermaid
flowchart LR
    User([👤 Usuario])
    PortalWeb([🌐 Portal de Suscripciones])

    subgraph Gestion_Cuentas_Odoo
        CrearCuenta([UC1: Crear cuenta])
        Login([UC2: Iniciar sesión])
    end

    subgraph Gestion_Suscripciones_Odoo
        VerPlanes([UC3: Consultar planes])
        Contratar([UC4: Contratar suscripción])
        EstadoSub([UC6: Consultar estado])
        Cancelar([UC8: Cancelar suscripción])
    end

    subgraph Pasarela_Pagos_Odoo
        PagoMetodo([UC5/UC7: Gestionar método pago])
    end

    User --> PortalWeb
    PortalWeb --> CrearCuenta
    PortalWeb --> Login
    PortalWeb --> VerPlanes
    PortalWeb --> Contratar
    PortalWeb --> EstadoSub
    PortalWeb --> Cancelar
    PortalWeb --> PagoMetodo
```

## Diagramas de flujo

### Registro y Contratación

```plantuml
@startuml
actor Usuario
participant Portal as "Portal Web"
participant Odoo as "Gestor Odoo"

Usuario -> Portal : Proporcionar datos (nombre, correo, pass)
activate Portal
Portal -> Odoo : UC1: Crear cuenta
activate Odoo
Odoo --> Portal : Cuenta creada con éxito
deactivate Odoo

Portal -> Portal : UC2: Iniciar Sesión automática
Portal -> Odoo : UC3: Obtener planes disponibles
activate Odoo
Odoo --> Portal : Lista de planes y precios
deactivate Odoo

Usuario -> Portal : Selecciona un Plan
Portal -> Odoo : UC4: Contractar subscripció
activate Odoo
Odoo --> Portal : Suscripción creada (Pendiente de pago)
deactivate Odoo

Usuario -> Portal : UC5: Introducir datos tarjeta
Portal -> Odoo : Registrar método de pago
activate Odoo
Odoo -> Odoo : Validar con pasarela bancaria
Odoo --> Portal : Pago aceptado / Suscripción Activa
deactivate Odoo

Portal --> Usuario : Confirmación de suscripción activada
deactivate Portal
@enduml
```

### Cambio de Método de Pago o Cancelación

```plantuml
@startuml
actor Usuario
participant Portal as "Portal Web"
participant Odoo as "Gestor Odoo"

Usuario -> Portal : Acceder a "Mi Suscripción"
activate Portal
Portal -> Odoo : UC6: Consultar estado
activate Odoo
Odoo --> Portal : Datos de suscripción activa
deactivate Odoo

alt Modificar Pago
    Usuario -> Portal : UC7: Cambiar método de pago
    Portal -> Odoo : Actualizar datos bancarios
    Odoo --> Portal : Actualización confirmada
else Cancelar Servicio
    Usuario -> Portal : UC8: Cancelar suscripción
    Portal -> Odoo : Notificar baja
    Odoo --> Portal : Baja programada (Fin de periodo)
end

Portal --> Usuario : Operación finalizada con éxito
deactivate Portal
@enduml
```