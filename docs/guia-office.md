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

Office no usa `slmgr`; usa su propio script `ospp.vbs`, que vive en la carpeta
de instalación. **Abre el Símbolo del sistema como administrador** y localiza la
carpeta:

```
dir "C:\Program Files\Microsoft Office" /b
```

- **Click-to-Run** (lo normal en Office 2016/2019/2021/2024 instalado desde el
  portal o con el instalador moderno): existe la carpeta `root`.
- **MSI clásico** (instalador corporativo `.msi`): no hay `root`; la carpeta
  `Office16` cuelga directo de `Microsoft Office`.

Con la ruta correcta, pide el IID:

```
cd /d "C:\Program Files\Microsoft Office\root\Office16"
cscript ospp.vbs /dinstid
```

Si es **MSI clásico**, cambia la primera línea por:

```
cd /d "C:\Program Files\Microsoft Office\Office16"
```

Variantes de ruta:

| Caso | Carpeta |
|---|---|
| Click-to-Run (64 bits) | `C:\Program Files\Microsoft Office\root\Office16` |
| Click-to-Run (32 bits en Windows 64) | `C:\Program Files (x86)\Microsoft Office\root\Office16` |
| MSI clásico (64 bits) | `C:\Program Files\Microsoft Office\Office16` |
| MSI clásico (32 bits en Windows 64) | `C:\Program Files (x86)\Microsoft Office\Office16` |
| Office 2013 | `Office15` en lugar de `Office16` |
| Office 2010 | `Office14` en lugar de `Office16` |

El script imprime tu **ID de instalación**: conjuntos de 6 dígitos, 63 en total
para Office.

> Nunca descargues `ospp.vbs` de sitios de DLL: es un script que corre con
> permisos de administrador y debe ser el que ya está en tu equipo.

## Paso 2 — Convertir el IID en CID

- En [activar.dev](https://activar.dev/), pega tu ID de instalación y obtén el
  **ID de confirmación** en segundos. Cuesta **$0.10 USD** y se cobra solo si
  se genera.
- O por API: `POST https://api.activar.dev/v1/cid` con `{"iid":"..."}`
  ([referencia](API.md)).

## Paso 3 — Aplicar el CID

En la **misma** consola, sin cambiar de carpeta:

```
cscript ospp.vbs /actcid:XXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Sustituye `XXXX...` por tu ID de confirmación. Debe aparecer
**"Product activation successful"**; reinicia Office si lo pide.

Si la consola se cerró, vuelve a entrar a la carpeta del Paso 1 y corre solo el
comando `/actcid`.

## Errores comunes

- **0xC004C008** — cupo en línea agotado → este flujo es la solución.
- **0xC004C020** — necesita activación telefónica.
- **0xC004C060** — clave usada en más equipos de lo permitido.

Ver todos: [errores de activación](https://activar.dev/errores/).

## Límites

- Funciona para claves **válidas** con el cupo en línea agotado.
- Microsoft puede cambiar la vía telefónica; no promete permanencia.
- No aplica a Office para Mac ni a Microsoft 365.
