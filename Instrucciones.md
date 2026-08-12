# Generador de Reporte EOD — cómo usarlo

## Qué hace
Toma los datos de una tienda y genera el reporte Word con tu diseño de siempre.
Los porcentajes se calculan solos (sobre el total de encuestas); tú solo escribes los conteos.

## Archivos
- `plantilla_hippies.docx` — tu diseño convertido en plantilla (no la borres).
- `generar_reporte.py` — el motor que rellena la plantilla.
- `app.py` — la interfaz (Streamlit).

## Instalar (una sola vez)
1. Instala Python 3 (si no lo tienes).
2. Abre una terminal en esta carpeta y corre:
   pip install streamlit pillow

## Correr la app
   streamlit run app.py
Se abre en el navegador. Llena los datos, sube mapas/fotos, y "Generar reporte Word".
Viene precargado con Hippies como ejemplo; cambia los valores por los de tu tienda.

## Sin app (solo script)
Puedes editar el diccionario de datos en `generar_reporte.py` y correr:
   python generar_reporte.py
Genera el Word directamente.

## Notas
- Las imágenes son opcionales: si no subes, quedan las de la plantilla.
- Sube las fotos idealmente en el mismo formato (fachada/fotos = .jpg, mapas = .png).
- Los % salen de: conteo / nº de encuestas. Si en tu caso alguna pregunta usa otro
  denominador, avísame y lo ajustamos.
