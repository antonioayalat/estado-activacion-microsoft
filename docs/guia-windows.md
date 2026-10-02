# Activar Windows por teléfono

Guía paso a paso para activar Windows 10/11 con el ID de confirmación, sin
llamar a nadie y sin cuenta de Microsoft. Fuente oficial del servicio
[activar.dev](https://activar.dev/).

> Guía completa en el portal: [activar windows por teléfono](https://activar.dev/guias/activar-windows-por-telefono/)

## Cuándo aplica

Cuando Windows muestra el error `0xC004C008` o `0xC004C020` al activar: la clave
**es válida** pero ya usó su cupo de activaciones en línea. La vía telefónica (ID
de confirmación) es la que Microsoft mismo recomienda.

**No aplica** si la clave fue bloqueada (revocada), si es de un equipo distinto,
o para Microsoft 365 / Windows 11 Pro EDU / Pro for Workstations.

## Paso 1 — Obtener el ID de instalación (IID)

1. Abre **Símbolo del sistema como administrador**.
2. Ejecuta:

```
slui 4
```

3. Se abre la ventana de activación telefónica. Verás una lista de países y un
   número largo: ese es tu **ID de instalación** (9 grupos de 6 dígitos, 54 en
   total para Windows).

## Paso 2 — Convertir el IID en CID

- En [activar.dev](https://activar.dev/), pega tu ID de instalación y obtén el
  **ID de confirmación** en segundos. Cuesta **$0.10 USD** y se cobra solo si
  se genera. *(Por la vía oficial de Microsoft tendrías que llamar o pasar el
  CAPTCHA del portal `aka.ms/aoh`, y entrar a tu cuenta.)*

## Paso 3 — Aplicar el CID

1. En la misma ventana de `slui 4`, en "Paso 3", pega el **ID de confirmación**.
2. Clic en **Activar Windows**.
3. Windows completa la activación. Reinicia si te lo pide.

## Errores comunes

- **0xC004C008** — cupo en línea agotado → este flujo es la solución.
- **0xC004C020** — necesita activación telefónica → este flujo.
- **0xC004C060** — clave usada en otro equipo más veces de lo permitido.

Ver todos: [errores de activación](https://activar.dev/errores/).

## Límites

- Funciona para claves **válidas** con el cupo en línea agotado.
- Microsoft puede cambiar la vía telefónica; no promete permanencia.
- No aplica a claves bloqueadas ni a Microsoft 365.
