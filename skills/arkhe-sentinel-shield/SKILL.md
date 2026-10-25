---
name: arkhe-sentinel-shield
description: Consulta el estado en tiempo real de ARKHE SENTINEL, el cortafuegos forense para agentes de IA. Permite verificar si hay amenazas activas, cuántos ataques han sido bloqueados, y el estado del Hash Chain inmutable.
---

# ARKHE SENTINEL SHIELD

## Cuándo activar
Cuando el usuario pregunte por seguridad, amenazas, ataques bloqueados o el estado de ARKHE SENTINEL.

## Instrucciones
1. Si el usuario te da un token, úsalo como header `X-Admin-Token`.
2. Consulta el endpoint `https://arkhe-auth.onrender.com/v1/guard/logs`.
3. Interpreta: `active_defense: true` es bueno. `status: "BLOCKED"` son ataques detenidos.
4. Reporta cuántos ataques hay y el estado del Hash Chain.
