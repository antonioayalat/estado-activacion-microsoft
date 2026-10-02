# Preguntas frecuentes

Mismo contenido que [activar.dev/faq](https://activar.dev/faq/) — respuestas
cortas, sin letra chica.

## El servicio

### ¿Qué es exactamente lo que recibo?

Un **ID de confirmación** (CID): el número que la activación telefónica de
Microsoft pide para activar tu propia clave de Windows u Office cuando ya no
activa por internet. Tu equipo lo genera como **ID de instalación** (IID);
activar.dev te devuelve el ID de confirmación correspondiente, sin llamada y sin
cuenta de Microsoft.

### ¿Es oficial y legal?

Sí. La activación telefónica es un mecanismo oficial de Microsoft para claves
válidas. activar.dev automatiza el paso intermedio y trabaja con **tu** licencia;
no vende activación pirata ni software. No está afiliado a Microsoft.

### ¿Necesito una cuenta de Microsoft?

No. Solo tu cuenta de Telegram (o una API key si eres desarrollador).

### ¿Guardan mi clave o mi ID de instalación?

No pedimos tu clave de producto, nunca. Necesitamos tu ID de instalación porque
es el dato que Microsoft pide. Guardamos solo un identificador derivado y el
registro de la operación para no cobrarte dos veces.

## Precios y cobros

- **Revisar tu clave:** gratis.
- **ID de confirmación:** $0.10 USD, se cobra solo si se genera.
- **Incluido** si compras tu clave en activar.dev.
- **Sin recobro:** si ya generamos el CID de tu IID antes, el acierto desde
  caché no se cobra otra vez.

### ¿Y si no me activa a la primera?

Reintentarlo es gratis: pega el mismo ID de instalación y no se vuelven a cobrar
los $0.10. Solo un ID distinto (otra instalación) es operación nueva.

### ¿Cómo recargo saldo?

Desde el panel, con Binance Pay, USDT/USDC o PayPal. El saldo se comparte entre
web, bot y API.

## Compatibilidad

- **Sí:** Windows 10/11 y Office (retail o volumen) con activación por teléfono.
- **No:** Microsoft 365 (suscripción), Windows 11 Pro EDU / Pro for
  Workstations, Office para Mac.
- Un IID vale por su instalación; los retailers activan un equipo, las de
  volumen traen miles de activaciones.

## Técnico

- **IID:** `slui 4` (Windows) o `cscript ospp.vbs /dinstid` (Office).
- **CID:** la respuesta de Microsoft que completa la activación, permanente.

## ¿Sigue tu duda?

Soporte por Telegram: [t.me/cidiid_bot](https://t.me/cidiid_bot)
