---
name: arkhe-prospector
description: Encuentra y califica leads B2B para vender certificados KRONOS-360. Usa datos públicos para enriquecer la ficha del prospecto. Usa la cuando el usuario diga "busca clientes", "prospecta", "genera leads".
---

# ARKHE PROSPECTOR

## Cuándo activar
Cuando el usuario pida "busca leads", "prospecta clientes", "genera lista de clientes ancla".

## Instrucciones
1. Pide al usuario: ciudad, giro (constructora / aseguradora / artesano / abogado), y cantidad de leads (máximo 20 por día para evitar spam).
2. Para cada lead, genera una ficha con:
   - Nombre del negocio o persona
   - Canal de contacto (Instagram DM, LinkedIn, WhatsApp público, email)
   - Un dato específico y verificable (ej: "publicó 3 fotos de obra en agosto")
   - Nivel de urgencia (alta/media/baja) según si muestran fotos de archivo o casos judiciales
.3. Devuelve la lista en formato CSV (nombre, canal, dato, urgencia).
4. **Regla de oro:** no inventes datos. Si no puedes verificar algo, márcalo como "sin verificar".
