# Activación telefónica de Microsoft (IID → CID)

Documentación técnica de la **activación por teléfono** de Windows y Office: la
conversión de un **ID de instalación** (IID) a un **ID de confirmación** (CID),
el mecanismo oficial de Microsoft para claves perpetuas cuyo cupo de
activaciones en línea se agotó.

**Sitio oficial:** [activar.dev](https://activar.dev/) · **API:** [activar.dev/api/docs](https://activar.dev/api/docs/)

Este repo es la fuente técnica del servicio activar.dev. **No** contiene claves
de producto, código de automatización del servicio ni secretos: explica el
flujo, la documentación y cómo implementar la API.

---

## Qué es

El error `0xC004C008` o `0xC004C020` al activar Windows/Office no significa que la
clave esté muerta. Significa que la clave **es válida pero ya usó su cupo de
activaciones en línea**. Microsoft ofrece entonces la **activación telefónica**: el
equipo genera un *ID de instalación* (IID), lo envías a Microsoft, y Microsoft
devuelve un *ID de confirmación* (CID) que aplicas en el mismo equipo para
activarlo.

Es un mecanismo **oficial de Microsoft** (ver `aka.ms/aoh`), el que su propio
soporte recomienda para esos errores.

## El flujo, en 3 pasos

1. **Obtener el IID** de tu equipo:
   - Windows: `slui 4`
   - Office: `cscript "%ProgramFiles%\Microsoft Office\Office16\OSPP.VBS" /dinstid`
     (la ruta cambia según versión y bits)
2. **Enviar el IID a Microsoft** y recibir el CID.
3. **Aplicar el CID** y completar la activación.

## Qué ofrece activar.dev

- **Verificador de clave (gratis):** [activar.dev](https://activar.dev/#instrumento)
- **Conversión IID → CID:** pegas el IID y obtienes el CID en segundos, sin
  cuenta de Microsoft ni CAPTCHA — usando la misma vía oficial.
- **Tienda de claves** Windows / Office / Project / Visio.
- **API para desarrolladores:** `api.activar.dev` (auth por API key, ver
  [docs/API.md](docs/API.md)).

## Documentación

| Ruta | Contenido |
|------|-----------|
| [docs/API.md](docs/API.md) | Implementar la API de activar.dev (endpoints, auth, ejemplos curl). |
| [docs/guia-windows.md](docs/guia-windows.md) | Guía completa: activar Windows por teléfono. |
| [docs/guia-office.md](docs/guia-office.md) | Guía completa: activar Office por teléfono. |
| [docs/faq.md](docs/faq.md) | Preguntas frecuentes (mismo contenido que activar.dev/faq). |

## Errores de activación

- **`0xC004C008`** — clave válida pero cupo en línea agotado → requiere CID.
  [Documentación](https://activar.dev/errores/error-0xc004c008/)
- **`0xC004C020`** — necesitas activar vía telefónica (ID de instalación).
  [Documentación](https://activar.dev/errores/error-0xc004c020/)
- **`0xC004C060`** — la clave se usó en otro equipo más veces de las permitidas.
- Más errores en [activar.dev/errores](https://activar.dev/errores/).

## Términos útiles

- **IID / ID de instalación**: identifica tu instalación concreta.
- **CID / ID de confirmación**: la respuesta de Microsoft que completa la activación.
- **MAK / clave de volumen**: claves con cupo de activaciones (p. ej. 500 usos).
- **Retail**: claves de activación única.

## Límites

- Aplica a licencias perpetuas de Windows (10/11) y Office (2016/2019/2021/2024).
- **No** aplica a Microsoft 365 (suscripción), ni Mac, ni versiones EDU/Workstations.
- Microsoft puede cambiar la vía telefónica; nada promete permanencia.
- Este repo **no** contiene claves de producto, automatización ni secretos.

## Enlaces

- [activar.dev](https://activar.dev/) — servicio en vivo
- [Documentación de la API](https://activar.dev/api/docs/)
- [Datos de operación del servicio](https://activar.dev/datos/)
