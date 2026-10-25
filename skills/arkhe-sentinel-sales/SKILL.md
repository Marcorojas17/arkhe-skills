---
name: arkhe-sentinel-sales
description: Audita y firma mensajes de venta antes de enviarlos, usando HMAC. Bloquea mensajes enganosos o tipo spam. Úsala cuando el usuario diga "audita el mensaje", "firma el mensaje", "revisa el mensaje antes de enviar".
---

# ARKHE SENTINEL CUSTOMER SALES

## Cuándo activar
Cuando el usuario tenga un mensaje redactado y quiera autorización antes de enviarlo.

## Instrucciones
1. Revisa el mensaje buscando:
   - Promesas ilegales ("te garantizo ganar el juicio")
   - Lenguaje spam ("¡ EŨLTIMA OPORTUNIDADE!!!")
   - Falta de consentimiento previo
2. Si el mensaje pasa la auditoría:
   - Cálculo SHA-256 del mensaje.
   - Firma HMAC usando ARKHE_SECRET.
   - Devuelve el mensaje + el sello JSON.
.3. Si el mensaje falla:
   - Devuelve las razones por las que se bloqu{ó.
   - Sugiere una reescritura sobria.
