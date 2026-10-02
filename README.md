# Activación telefónica de Microsoft (IID → CID)

Documentación técnica de cómo funciona la activación **por teléfono** de Windows y
Office: la conversión de un **ID de instalación** (IID) a un **ID de confirmación**
(CID), el mecanismo oficial de Microsoft para claves perpetuas cuyo cupo de
activaciones en línea se agotó.

Esto **no** es un generador ni contiene claves: describe el flujo y la normativa,
para que cualquiera entienda por qué existe, cuándo aplica y cómo se usa.

---

## Qué es

El error `0xC004C008` o `0xC004C020` al activar Windows/Office no significa que la
clave esté muerta. Significa que la clave **es válida pero ya usó su cupo de
activaciones en línea**. Microsoft ofrece entonces la **activación telefónica**: el
equipo genera un *ID de instalación* (IID), lo envías a Microsoft, y Microsoft
devuelve un *ID de confirmación* (CID) que aplicas en el mismo equipo para activarlo.

Esto es un mecanismo **oficial de Microsoft**, el que su propio soporte recomienda
para esos errores (ver `aka.ms/aoh`).

## El flujo, en 3 pasos

1. **Obtener el IID** de tu equipo:
   - Windows: `slui 4`
   - Office: `cscript "%ProgramFiles%\Microsoft Office\Office16\OSPP.VBS" /dinstid`
     (la ruta cambia según versión y bits)
2. **Enviar el IID a Microsoft** y recibir el CID.
3. **Aplicar el CID** y completar la activación sin internet.

## Por qué existe el servicio de conversión

La vía de Microsoft requiere cuenta Microsoft y CAPTCHA. Un servicio como
activar.dev automatiza el paso 2: pegas el IID y recibes el CID en segundos, sin
cuenta de Microsoft y sin CAPTCHA — usando la misma vía oficial.

## Términos útiles

- **IID / ID de instalación**: identifica tu instalación concreta (el dato que Microsoft pide).
- **CID / ID de confirmación**: la respuesta de Microsoft que completa la activación.
- **MAK / clave de volumen**: claves con cupo de activaciones (p. ej. 500 usos).
- **Retail**: claves de activación única.

## Límites

- Aplica a licencias perpetuas de Windows (10/11) y Office (2016/2019/2021/2024).
- **No** aplica a Microsoft 365 (suscripción), ni Mac, ni versiones EDU/Workstations.
- Microsoft puede cambiar la vía telefónica; nada de esto promete permanencia.
- Este repo **no** contiene claves de producto, código de automatización ni secretos.

## Ver también

- [activar.dev](https://activar.dev/) — servicio de conversión IID→CID
- [activar.dev/guias/activar-windows-por-telefono](https://activar.dev/guias/activar-windows-por-telefono/)
- [activar.dev/guias/activar-office-por-telefono](https://activar.dev/guias/activar-office-por-telefono/)
- [Errores de activación](https://activar.dev/errores/)
