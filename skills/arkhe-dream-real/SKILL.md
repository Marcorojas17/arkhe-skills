---
name: arkhe-dream-real
description: Interpreta sueños sin magia, con neurociencia y psicología real. Usa base de 859 símbolos del libro 'Significado e Interpretación de sueños' (653 páginas) pero traduciendo a patrones de memoria, apego y estrés. Guarda journaling en mis_sueños.log y genera resumen semanal. Activa cuando el usuario mencione soñé, sueño, dream, pesadilla.
---

# ARKHE DREAM REAL

## Cuándo activar
Cuando el usuario diga: "soñé que...", "tuve un sueño", "qué significa soñar con X", "interpretar sueño".

## Instrucciones
1. Extrae palabras clave (sustantivos >4 letras).
2. Busca en sueños.db.json (859 entradas).
3. NO des interpretación mágica (no genios, no fortuna). Traduce a REAL:
   - ENAMORADO = apego/dopamina, idealización
   - SERPIENTE = detección de amenaza social, amígdala
   - DINERO = estrés prefrontal, control/escasez
   - BOTELLA/BOTELLAS = emoción contenida no verbalizada
   - RIO = transición de estado mental
   - BONSAI = perfeccionismo/microgestión
   - ACANTILADO = límite, decisión al borde
4. Si hay 2+ símbolos, haz cruce REAL: ¿qué patrón se repite?
5. Guarda en mis_sueños.log formato: ISO | frase | PALABRA1,PALABRA2
6. Pregunta de acción real, no predicción futura.

## Ejemplo de salida
ARKHE REAL - soñé que se caía mi botella en un rio
BOTELLAS: Emoción contenida no dicha
RIO: Transición, cambio de etapa
Foco real: ¿Qué estás conteniendo que necesita fluir?

## Archivos
- dream.py es el motor
- sueños.db.json es la base de 859 símbolos
- mis_sueños.log es el journaling
