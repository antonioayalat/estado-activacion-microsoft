# Activar Office por teléfono

Guía paso a paso para activar licencias perpetuas de **Office (2016/2019/2021/
2024)** con el ID de confirmación, sin llamar a nadie y sin cuenta de Microsoft.
Fuente oficial del servicio [activar.dev](https://activar.dev/).

> Guía completa en el portal: [activar office por teléfono](https://activar.dev/guias/activar-office-por-telefono/)

## Cuándo aplica

Cuando Office muestra un error de activación por cupo agotado en línea (como
`0xC004C008`, `0xC004C020` o `0xC004C060`): la clave **es válida** pero ya usó
sus activaciones en línea. La vía telefónica la resuelve.

**No aplica** a Microsoft 365 (suscripción, no hay nada que activar), a Office
para Mac (solo acepta licencias canjeadas en cuenta Microsoft), ni a claves
bloqueadas.

## Paso 1 — Obtener el ID de instalación (IID)

Office no usa `slmgr`; usa su propio script `ospp.vbs` desde la carpeta de
Office. En **Símbolo del sistema como administrador**:

```
cscript "%ProgramFiles%\Microsoft Office\Office16\OSPP.VBS" /dinstid
```

Si Office está en otra ruta o son 32 bits en 64 bits, ajusta la carpeta
(`Office16`, `Office15`, `...\Office16\`, `C:\Program Files (x86)\Microsoft
Office\Office16\`). El script imprime tu **ID de instalación** (conjuntos de 6
dígitos, 63 en total para Office).

## Paso 2 — Convertir el IID en CID

- En [activar.dev](https://activar.dev/), pega tu ID de instalación y obtén el
  **ID de confirmación** en segundos. Cuesta **$0.10 USD** y se cobra solo si
  se genera.

## Paso 3 — Aplicar el CID

1. En la misma consola:

```
cscript "%ProgramFiles%\Microsoft Office\Office16\OSPP.VBS" /dinstid
cscript "%ProgramFiles%\Microsoft Office\Office16\OSPP.VBS" /actcid:XXXXXXXXXXXXXXXXXXXXXXXXXXX
```

   (Sustituye `XXXX...` por el ID de confirmación.)

2. Confirma el mensaje "Product activation successful". Reinicia Office si lo pide.

## Errores comunes

- **0xC004C008** — cupo en línea agotado → este flujo es la solución.
- **0xC004C020** — necesita activación telefónica.
- **0xC004C060** — clave usada en más equipos de lo permitido.

Ver todos: [errores de activación](https://activar.dev/errores/).

## Límites

- Funciona para claves **válidas** con el cupo en línea agotado.
- Microsoft puede cambiar la vía telefónica; no promete permanencia.
- No aplica a Office para Mac ni a Microsoft 365.
