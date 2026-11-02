# API de activar.dev

Referencia para integrar la API v1: genera **IDs de confirmación (CID)** de
activación de Windows y Office con una llamada HTTP. Es la misma API que
alimenta el bot y el portal.

- **Base URL:** `https://api.activar.dev`
- **Documentación navegable:** https://activar.dev/api/docs/
- **Especificación:** https://api.activar.dev/openapi.json (OpenAPI 3.1)

Todas las respuestas son JSON. El body máximo es de **8 192 bytes** (salvo
`/v1/ocr/iid`, que acepta imágenes de hasta 5 MiB) y cada petición de CID tiene
un límite de **90 segundos** de proceso. Todos los cuerpos usan `extra="forbid"`:
un campo desconocido devuelve `400`.

## Autenticación

Hay dos grupos de rutas:

- **Autenticadas** (`/v1/cid`, `/v1/balance`, `/v1/movs`, `/v1/usage`,
  `/v1/topup`, `/v1/shop/buy`) exigen:

  ```
  Authorization: Bearer <tu-clave>
  ```

  Las claves de integrador empiezan con `gck_`; las sesiones web del portal con
  `sess_`. Sin credencial: `401 KEY_MISSING`. Con una clave que no existe o no
  coincide: `401 KEY_INVALID`.

- **Públicas**: `/healthz`, `/readyz`, `/v1/shop`, `/v1/shop/dl-pack`, y las
  herramientas gratuitas (`/v1/checkkey`, `/v1/validate-iid`,
  `/v1/generate-iid`, `/v1/ocr/iid`). Estas últimas aceptan **token Turnstile**
  (humano en navegador) **o tu clave Bearer** (server-to-server, sin Turnstile).

Emites y gestionas tus claves en el bot de Telegram
([@cidiid_bot](https://t.me/cidiid_bot), comando `/api`). La clave se entrega
**una sola vez** por mensaje directo: en la base solo vive su hash. Se puede
rotar o revocar cuando quieras, y cada una tiene tope diario de gasto
($5.00 por defecto).

### Límites por minuto

| Camino | Límite |
|---|---|
| Anónimo con Turnstile | 6 claves por minuto por IP (un lote cuenta por clave) |
| Integrador con Bearer | 30 operaciones por minuto por clave |
| OCR con Bearer | 3 por minuto por clave (Tesseract corre en CPU local) |

La cuota del integrador va **por clave, no por IP**: puedes llamar desde Vercel,
AWS o cualquier proveedor compartido sin mezclar tu límite con el de otros.

## Endpoints

### Salud

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/healthz` | — | Liveness del servicio. |
| GET | `/readyz` | — | Readiness: confirma la base y reporta slots de generación libres. |

### Cuenta

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/v1/balance` | Bearer | Saldo, tope diario y gasto del día (UTC). |
| GET | `/v1/movs?limit=30` | Bearer | Movimientos de saldo (recargas y cobros). |
| GET | `/v1/usage?limit=50` | Bearer | Bitácora de consumo de tu clave. `limit` 1–200. |
| POST | `/v1/topup` | Bearer | Recarga por Binance Pay, USDT/USDC (BEP-20 / TRC-20) o PayPal. |

### Herramientas gratuitas (Turnstile o Bearer)

| Método | Ruta | Body | Descripción |
|---|---|---|---|
| POST | `/v1/checkkey` | `{"key":"..."}` o `{"keys":["...", ...]}` (máx. 10) + `turnstile?` | Verifica claves y cuántas activaciones les quedan. |
| POST | `/v1/validate-iid` | `{"iid":"..."}` + `turnstile?` | Valida estructura y dígito de control de un IID. |
| POST | `/v1/generate-iid` | `{"tipo":"office"\|"windows"}` + `turnstile?` | Genera un IID bien formado para pruebas (no es el de un equipo real). |
| POST | `/v1/ocr/iid` | `multipart/form-data` con `file` + `turnstile?` | Extrae el IID de una captura (JPEG/PNG, ≤5 MiB, ≤20 MP). |

### Negocio

| Método | Ruta | Body | Descripción |
|---|---|---|---|
| POST | `/v1/cid` | `{"iid":"..."}` | Genera el CID y cobra **$0.10** de saldo. |
| GET | `/v1/shop` | — | Catálogo público con precios y stock en vivo. |
| POST | `/v1/shop/buy` | `{"product_name":"...","cantidad":1}` | Compra claves con saldo; las entrega en la respuesta. |
| GET | `/v1/shop/dl-pack?product=&lang=es-ES&bits=64` | — | Pack de instalación (ZIP) para claves de volumen. Público. |
| POST | `/v1/auth/telegram` | `{"id":123456,"first_name":"..."}` | Login con Telegram Login Widget; devuelve una sesión `sess_*`. |

## Flujo completo: IID → CID

```bash
curl -X POST https://api.activar.dev/v1/cid \
  -H "Authorization: Bearer gck_TU_CLAVE" \
  -H "Content-Type: application/json" \
  -d '{"iid":"00269538026695922170826852518480286383828529569486954"}'
```

Respuesta `200`:

```json
{
  "ok": true,
  "cid": "012345-678901-234567-890123-456789-012345-678901-234567",
  "blocks": ["012345","678901","234567","890123","012345","678901","678901","234567"],
  "cached": false,
  "source": "soap",
  "charged": 0.1,
  "request_id": "uuid-de-la-peticion",
  "balance": 4.90
}
```

| Campo | Significado |
|---|---|
| `cid` | El ID de confirmación listo para teclear en el asistente de activación. |
| `blocks` | El mismo CID partido en bloques de 6, como lo pide el asistente. |
| `cached` | `true` si ya se había generado antes: responde al instante y **no se cobra**. |
| `charged` | Lo cobrado por esta petición, en USD (`0.0` en aciertos de caché). |
| `request_id` | Referencia exacta en la bitácora para soporte o auditoría. |
| `balance` | Saldo resultante, en USD. |

El IID se valida **antes** de cobrar: si su checksum es inválido, la petición se
rechaza sin cargo. Un acierto de caché responde en milisegundos; una generación
nueva tarda segundos y el límite duro es de 90 s.

## Errores

El envelope es el mismo en toda la API, incluido `checkkey`:

```json
{"detail": {"code": "IID_INVALID", "message": "..."}}
```

| HTTP | Código | Significado | ¿Cobra? |
|---|---|---|---|
| 400 | `IID_INVALID` | El IID no tiene formato de ID de instalación. | No |
| 400 | `IID_CHECKSUM_INVALID` | El IID no pasa el dígito de control. | No |
| 400 | — | Body inválido o campo desconocido. | No |
| 401 | `KEY_MISSING` | Falta el header `Authorization`. | No |
| 401 | `KEY_INVALID` | La clave no existe o no coincide. | No |
| 402 | `NO_BALANCE` | Saldo insuficiente para el precio del CID. | No |
| 403 | `KEY_PENDING` | La clave se emitió pero aún no confirmas su entrega por DM en el bot. | No |
| 403 | `KEY_REVOKED` | La clave fue revocada. | No |
| 409 | `IN_PROGRESS` | El IID ya está en proceso por otra petición. Respeta `Retry-After`. | No |
| 409 | `IID_ALREADY_USED` | Ese IID ya se usó. | No |
| 413 | `PAYLOAD_TOO_LARGE` | Body mayor a 8 192 bytes (o imagen mayor a 5 MiB en OCR). | No |
| 429 | `CAP_DIARIO` | Alcanzaste el tope diario de gasto de tu clave. | No |
| 429 | `RATE_LIMITED` | Demasiadas peticiones seguidas. Respeta `Retry-After`. | No |
| 502 | `UPSTREAM_ERROR` | Microsoft rechazó la generación. No reintentar en automático. | No |
| 503 | `BUSY` | Sin slots libres ahora. Reintenta con `Retry-After`. | No |
| 503 | `TIMEOUT` | La generación rebasó 90 s. Seguro reintentar. | No |
| 503 | `CACHE_UNAVAILABLE` | El caché está temporalmente caído. Reintenta. | No |

**Regla de cobro:** el cargo es atómico con la entrega. Nunca hay un cobro sin
CID ni un CID sin su registro en la bitácora. Si la respuesta es un error de
generación (`502`/`503`), no hubo cobro.

## Ejemplos

Consultar saldo:

```bash
curl https://api.activar.dev/v1/balance \
  -H "Authorization: Bearer gck_TU_CLAVE"
```

Verificar una clave (gratis):

```bash
curl -X POST https://api.activar.dev/v1/checkkey \
  -H "Authorization: Bearer gck_TU_CLAVE" \
  -H "Content-Type: application/json" \
  -d '{"key":"AAAAA-BBBBB-CCCCC-DDDDD-EEEEE"}'
```

Lote de hasta 10 claves:

```bash
curl -X POST https://api.activar.dev/v1/checkkey \
  -H "Authorization: Bearer gck_TU_CLAVE" \
  -H "Content-Type: application/json" \
  -d '{"keys":["AAAAA-BBBBB-CCCCC-DDDDD-EEEEE","11111-22222-33333-44444-55555"]}'
```

Validar un IID (63 dígitos = Office, 54 = Windows):

```bash
curl -X POST https://api.activar.dev/v1/validate-iid \
  -H "Authorization: Bearer gck_TU_CLAVE" \
  -H "Content-Type: application/json" \
  -d '{"iid":"631436-...-7696"}'
```

OCR de una captura:

```bash
curl -X POST https://api.activar.dev/v1/ocr/iid \
  -H "Authorization: Bearer gck_TU_CLAVE" \
  -F "file=@captura.png;type=image/png"
```

Catálogo público:

```bash
curl https://api.activar.dev/v1/shop
```

## Costos

- **CID:** $0.10 USD por generación nueva. Los aciertos de caché no se cobran.
- **Herramientas** (`checkkey`, `validate-iid`, `generate-iid`, `ocr/iid`): gratis.
- El saldo es el mismo del chat de Telegram: lo recargas desde el bot o con
  `/v1/topup`.

## Límites del servicio

- Aplica a licencias perpetuas de Windows (10/11) y Office (2016/2019/2021/2024).
- **No** aplica a Microsoft 365, Mac, ni ediciones EDU / Workstations.
- Microsoft puede cambiar la vía telefónica; nada garantiza permanencia.
