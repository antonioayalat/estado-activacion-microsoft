# API de activar.dev

Referencia para implementar la API de activar.dev — la misma que alimenta el bot
y el portal, con autenticación por **API key** para integradores
(server-to-server) o por **sesión web** (`sess_*`).

**Base URL:** `https://api.activar.dev/` · **Docs oficiales:** https://activar.dev/api/docs/

> Todo cuerpo de petición usa `extra="forbid"` (campos desconocidos = 400).
> Salvo `checkkey` / `validate-iid` / `generate-iid` (que aceptan token Turnstile
> O credencial), los endpoints piden credencial Bearer.

## Autenticación

Envía la key en el header `Authorization` como Bearer:

```
Authorization: Bearer gck_xxxxxxxx
```

Una petición sin credencial a un endpoint privado responde `401 KEY_MISSING`.
Los integradores server-to-server usan una key `gck_*` (y pasan el rate limit
por IP); los clientes web usan `sess_*`.

## Endpoints

### Salud

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/healthz` | Liveness del servicio. |
| GET | `/readyz` | Readiness (deps listas). |

### Cuenta y movimientos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/v1/balance` | Saldo actual. |
| GET | `/v1/movs?limit=30` | Bitácora de movimientos. |
| GET | `/v1/compras?limit=100` | Historial de compras. |
| GET | `/v1/usage?limit=50` | Uso/consumo por operación. |

### Herramientas públicas (humano o integrador)

| Método | Ruta | Body | Descripción |
|--------|------|------|-------------|
| POST | `/v1/checkkey` | `{key}` o `{keys: [...]}` + `turnstile?` | Verifica clave a clave (batch web). Gratis. |
| POST | `/v1/validate-iid` | `{iid}` | Valida un ID de instalación. |
| POST | `/v1/generate-iid` | `{tipo}` (`office`|`windows`) | Genera un IID de prueba. |

Estos tres se protegen con **Turnstile o credencial** (puerta anti-abuso) más
rate limit por IP que protege el pipeline contra Microsoft.

### Operaciones de negocio

| Método | Ruta | Body | Descripción |
|--------|------|------|-------------|
| POST | `/v1/cid` | — | Genera el CID para un IID (cobra $0.10 de saldo). |
| POST | `/v1/topup` | `{order_id}` | Acredita una recarga (Binance/OT). |
| POST | `/v1/auth/telegram` | — | Intercambio de auth por sesión. |
| GET | `/v1/shop` | — | Catálogo de la tienda (precios/stock en vivo). |
| POST | `/v1/shop/buy` | `{product_name, cantidad:1}` | Compra de clave; el CID va incluido. |
| GET | `/v1/shop/dl-pack?product=&lang=es-ES&bits=64` | — | Descarga del instalador (ZIP) del producto. |

## Ejemplos

Verificar una clave (con key):

```bash
curl -X POST https://api.activar.dev/v1/checkkey \
  -H "Authorization: Bearer gck_xxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"key":"XXXXX-XXXXX-XXXXX-XXXXX-XXXXX"}'
```

Consultar saldo:

```bash
curl https://api.activar.dev/v1/balance \
  -H "Authorization: Bearer gck_xxxxxxxx"
```

## Errores

| Status | Código | Significado |
|--------|--------|-------------|
| 400 | — | Body inválido / campo desconocido. |
| 401 | `KEY_MISSING` / `INVALID_KEY` | Falta o no vale la credencial. |
| 429 | — | Rate limit por IP. |
| 402 | — | Saldo insuficiente (operaciones que cobran). |
