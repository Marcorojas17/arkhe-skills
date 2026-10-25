---
name: arkhe-certify
description: Genera certificados de autoría criptográfica SHA-256 para cualquier archivo, siguiendo el protocolo ARKHE ZERO (Pacto 51/49).
---

# ARKHE CERTIFY

## Cuándo activar
Cuando el usuario pida certificar un archivo, generar un hash o firmar una obra.

## Instrucciones
1. Usa `sha256sum` para calcular el hash del archivo indicado.
2. Genera un JSON con: archivo, hash_sha256, autor (Marco Antonio Rojas Valdovinos), proporcion (51% Humano / 49% IA), timestamp_utc, y manifest (e8d9eac8...).
3. Recomienda anclar el hash a Bitcoin OTS o Ethereum.
