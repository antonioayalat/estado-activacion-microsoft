#!/usr/bin/env python3
"""verify_docs.py — gate del repo de documentación (estado-activacion-microsoft).

Este repo no tiene código ejecutable: su contrato es el markdown. El verificador
comprueba que el contenido publicado sea navegable y no reintroduzca errores ya
corregidos.

Uso:  python3 scripts/verify_docs.py [raíz]
Salida: 0 si todo pasa; 1 con la lista de fallos.
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
FALLOS = []

# Errores ya corregidos que no deben volver (regresión).
PROHIBIDO = {
    "INVALID_KEY": "el código real de la API es KEY_INVALID",
    'cscript "%ProgramFiles%\\Microsoft Office\\Office16\\OSPP.VBS"':
        "ruta MSI; la mayoría de instalaciones son Click-to-Run (root\\Office16)",
}


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for fn in filenames:
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


def check_file(path):
    rel = os.path.relpath(path, ROOT)
    with open(path, encoding="utf-8") as fh:
        texto = fh.read()

    if texto.count("```") % 2 != 0:
        FALLOS.append(f"{rel}: bloques de código sin cerrar (``` impar)")

    for mal, motivo in PROHIBIDO.items():
        if mal in texto:
            FALLOS.append(f"{rel}: contiene {mal!r} — {motivo}")

    for destino in re.findall(r"\]\(([^)\s]+)\)", texto):
        if destino.startswith(("http://", "https://", "mailto:", "#")):
            continue
        limpio = destino.split("#", 1)[0]
        if not limpio:
            continue
        objetivo = os.path.normpath(os.path.join(os.path.dirname(path), limpio))
        if not os.path.exists(objetivo):
            FALLOS.append(f"{rel}: enlace relativo roto -> {destino}")


def main():
    archivos = sorted(md_files())
    if not archivos:
        print("❌ no encontré archivos .md")
        return 1
    for path in archivos:
        check_file(path)
    print(f"verify_docs: {len(archivos)} archivos revisados")
    if FALLOS:
        print("❌ FALLOS:")
        for f in FALLOS:
            print("   -", f)
        return 1
    print("✅ verify_docs OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
