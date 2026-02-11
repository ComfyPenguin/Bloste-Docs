# Módulo Odoo: Bloste Custom Auth JWT

`Bloste_custom_auth_jwt` es un módulo de Odoo diseñado para exponer una **API REST** de autenticación basada en **JWT (JSON Web Token)**. Su propósito principal es permitir que aplicaciones externas (*frontends* en Vue, Flutter, o servicios *backend*) autentiquen usuarios sin depender del sistema de sesiones basado en cookies tradicional de Odoo.

## Funcionalidades Clave

* **Registro de usuarios:** Permite dar de alta cuentas de usuario de tipo "Portal" desde clientes externos.
* **Autenticación:** Genera un token JWT válido tras validar las credenciales del usuario (login y contraseña).
* **Validación de sesión:** Recupera la información del usuario autenticado enviando el JWT en la cabecera.
* **Refresco de Token:** Incluye un endpoint para renovar el *access token* mediante un *refresh token*, manteniendo la sesión activa de forma segura.

## Endpoints Disponibles

Todos los endpoints aceptan y devuelven datos en formato `application/json`.

| Método | Endpoint | Descripción |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Crear una nueva cuenta de usuario (tipo portal). |
| `POST` | `/api/auth/token` | Generar JWT (**Access** y **Refresh Tokens**). |
| `GET` | `/api/users/me` | Obtener datos del usuario autenticado. |
| `POST` | `/api/auth/refresh` | Refrescar un token de acceso usando un token de refresco. |

## Configuración

Para que el módulo funcione correctamente, es imperativo configurar el archivo `odoo.conf` con los siguientes parámetros:

```
jwt_secret = tu_clave_super_secreta
jwt_expiration = 3600
private = /ruta/a/tu/clave_privada.pem
public = /ruta/a/tu/clave_publica.pem

```

### Descripción de parámetros:

1. **`jwt_secret`**: Clave utilizada para firmar los tokens JWT.
2. **`jwt_expiration`**: Tiempo de validez del token de acceso expresado en segundos (ej. `3600` para 1 hora).
3. **`private`**: Ruta absoluta al archivo de **clave privada RSA** (necesaria para la firma de tokens).
4. **`public`**: Ruta absoluta al archivo de **clave pública RSA** (necesaria para la verificación).

## Consideraciones Importantes

* **Flujo de Registro:** El registro de usuarios **no inicia sesión automáticamente**. El frontend debe registrar al usuario y luego llamar explícitamente al endpoint `/api/auth/token` para obtener los tokens.
* **Gestión de Sesión:** El control de la sesión recae exclusivamente en el frontend externo. Este módulo **no crea cookies** ni sesiones tradicionales en el servidor de Odoo.
* **Estilo de API:** Se utiliza un estilo **REST sencillo**. A diferencia de otros módulos de Odoo, **NO** se emplea el formato envoltorio de JSON-RPC.

## Dependencias Externas

Este módulo requiere las siguientes librerías de Python, las cuales deben incluirse en el archivo `requirements.txt`:

* **`PyJWT==2.10.1`**: Para la gestión de los JSON Web Tokens.
* **`cryptography`**: Fundamental para manejar el algoritmo **RS256** usado en la firma.
* *Versión para Python < 3.12:* `3.4.8`
* *Versión para Python >= 3.12:* `42.0.8`



---

*Documentación generada para el módulo de autenticación Bloste.*