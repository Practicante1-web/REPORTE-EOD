# -*- coding: utf-8 -*-
"""App EOD (v2, categorías flexibles) — genera el reporte Word de una tienda.
Correr:  streamlit run app.py
"""
import streamlit as st, tempfile, os
from generar_reporte import construir_reporte, HIPPIES

st.set_page_config(page_title="Reporte EOD", page_icon="📍", layout="wide")
st.title("📍 Generador de Reporte EOD")
st.caption("Llena los datos de la tienda (los lees del Dashboard de ArcGIS), sube mapas/fotos y descarga el Word.")
st.subheader("📂 Cargar datos EOD")

archivo_csv = st.file_uploader(
    "Sube el archivo CSV descargado de ArcGIS",
    type=["csv"]
)

if archivo_csv is not None:
    import pandas as pd

    df = pd.read_csv(archivo_csv)

    st.success(f"Archivo cargado correctamente ✅ — {len(df)} registros")

    st.write("Columnas encontradas:")
    st.write(df.columns.tolist())

    st.dataframe(df.head(10))
PLANTILLA = os.path.join(os.path.dirname(__file__), "plantilla_hippies.docx")
H = HIPPIES

c1, c2 = st.columns(2)
with c1:
    st.subheader("Identificación")
    tienda  = st.text_input("Tienda", H['tienda'])
    periodo = st.text_input("Periodo", H['periodo'])
    n_enc   = st.number_input("Nº de encuestas", value=H['n_encuestas'], step=1)
    trafico = st.number_input("Tráfico 15/min", value=H['trafico'], step=1)
    st.subheader("Perfil del cliente")
    edad    = st.number_input("Edad promedio", value=H['edad'], step=1)
    gen_h   = st.number_input("Género H", value=H['gen_h'], step=1)
    gen_m   = st.number_input("Género M", value=H['gen_m'], step=1)
    estrato = st.text_input("Estrato principal", str(H['estrato']))
    st.markdown("**Ocupación** (conteos — la app toma la mayor)")
    _oc=H.get('ocupacion',{})
    oc_emp = st.number_input("Empleado", value=_oc.get('empleado',0), step=1)
    oc_est = st.number_input("Estudiante", value=_oc.get('estudiante',0), step=1)
    oc_ind = st.number_input("Independiente", value=_oc.get('independiente',0), step=1)
    oc_hog = st.number_input("Hogar", value=_oc.get('hogar',0), step=1)
    oc_des = st.number_input("Desempleado", value=_oc.get('desempleado',0), step=1)
    oc_pen = st.number_input("Pensionado", value=_oc.get('pensionado',0), step=1)
    st.subheader("Medio de llegada")
    m_apie = st.number_input("A pie", value=H['medio']['apie'], step=1)
    m_moto = st.number_input("Moto", value=H['medio']['moto'], step=1)
    m_auto = st.number_input("Automóvil", value=H['medio']['auto'], step=1)
    m_otro = st.number_input("Otro", value=H['medio'].get('otro',0), step=1)
with c2:
    st.subheader("Origen — De dónde viene")
    o_t = st.number_input("Origen · Trabajo", value=H['origen']['trabajo'], step=1)
    o_c = st.number_input("Origen · Casa", value=H['origen']['casa'], step=1)
    o_co= st.number_input("Origen · Colegio", value=H['origen'].get('colegio',0), step=1)
    o_u = st.number_input("Origen · Universidad", value=H['origen']['universidad'], step=1)
    o_o = st.number_input("Origen · Otro", value=H['origen']['otro'], step=1)
    st.subheader("Destino — A dónde se dirige")
    d_t = st.number_input("Destino · Trabajo", value=H['destino']['trabajo'], step=1)
    d_c = st.number_input("Destino · Casa", value=H['destino']['casa'], step=1)
    d_co= st.number_input("Destino · Colegio", value=H['destino'].get('colegio',0), step=1)
    d_u = st.number_input("Destino · Universidad", value=H['destino']['universidad'], step=1)
    d_o = st.number_input("Destino · Otro", value=H['destino']['otro'], step=1)
    st.subheader("Radios de influencia (conteos)")
    r1 = st.number_input("100m", value=H['radios']['m100'], step=1)
    r2 = st.number_input("200m", value=H['radios']['m200'], step=1)
    r3 = st.number_input("300m", value=H['radios']['m300'], step=1)
    r4 = st.number_input("+300m", value=H['radios']['mas300'], step=1)
    _s=int(r1)+int(r2)+int(r3)+int(r4)
    if _s:
        _p=lambda x:round(int(x)/_s*100)
        st.caption(f"Para la narrativa: 100m ({_p(r1)}%), 200m ({_p(r2)}%), 300m ({_p(r3)}%) y +300m ({_p(r4)}%)")

st.divider()
c3, c4 = st.columns(2)
with c3:
    st.subheader("Principal motivo de compra (top 3)")
    st.caption("Categorías posibles: Cercanía, Comodidad, Servicio, Experiencia, Surtido, Precios, No aplica.")
    mot=[]
    for i in range(3):
        a,b = st.columns([2,1])
        l = a.text_input(f"Motivo {i+1}", H['motivo'][i][0] if i<len(H['motivo']) else "", key=f"ml{i}")
        c = b.number_input(f"Cant. {i+1}", value=H['motivo'][i][1] if i<len(H['motivo']) else 0, step=1, key=f"mc{i}")
        if l.strip(): mot.append((l,c))
with c4:
    st.subheader("Alternativa de compra (hasta 6)")
    st.caption("Escribe solo los competidores que apliquen a esta tienda; los que dejes en blanco no salen.")
    alt=[]
    for i in range(6):
        a,b = st.columns([2,1])
        dl = H['alternativa'][i][0] if i<len(H['alternativa']) else ""
        dc = H['alternativa'][i][1] if i<len(H['alternativa']) else 0
        l = a.text_input(f"Competidor {i+1}", dl, key=f"al{i}")
        c = b.number_input(f"Resp. {i+1}", value=dc, step=1, key=f"ac{i}")
        if l.strip(): alt.append((l,c))

st.divider()
st.subheader("Textos (los escribes tú)")
percepcion = st.text_area("Percepción del servicio", H['percepcion_texto'], height=80)
radios_txt = st.text_area("Narrativa de radios de influencia", H['radios_texto'], height=120)
alt_nota   = st.text_area("Nota alternativa de compra", H['alt_nota'], height=60)
st.markdown("**Insights clave**")
ins=[]
for i in range(3):
    t  = st.text_input(f"Insight {i+1} · Título", H['insights'][i]['titulo'], key=f"it{i}")
    p1 = st.text_area(f"Insight {i+1} · Texto", H['insights'][i]['p1'], height=90, key=f"ip{i}")
    p2 = st.text_input(f"Insight {i+1} · Texto 2 (opcional)", H['insights'][i].get('p2',''), key=f"ip2{i}")
    ins.append({'titulo':t,'p1':p1,'p2':p2})

st.divider()
st.subheader("Imágenes (opcional)")
i1 = st.file_uploader("Foto de cabecera (fachada)", type=['jpg','jpeg','png'])
i2 = st.file_uploader("Mapa de radios (anillos)", type=['jpg','jpeg','png'])
i3 = st.file_uploader("Mapa de isócrona", type=['jpg','jpeg','png'])
i4 = st.file_uploader("Foto 1", type=['jpg','jpeg','png'])
i5 = st.file_uploader("Foto 2", type=['jpg','jpeg','png'])

if st.button("🚀 Generar reporte Word", type="primary"):
    d = {
      'tienda':tienda,'periodo':periodo,'n_encuestas':int(n_enc),'trafico':int(trafico),
      'edad':int(edad),'gen_h':int(gen_h),'gen_m':int(gen_m),'estrato':estrato,
      'ocupacion':{'empleado':int(oc_emp),'estudiante':int(oc_est),'independiente':int(oc_ind),'hogar':int(oc_hog),'desempleado':int(oc_des),'pensionado':int(oc_pen)},
      'origen':{'trabajo':int(o_t),'casa':int(o_c),'colegio':int(o_co),'universidad':int(o_u),'otro':int(o_o)},
      'destino':{'trabajo':int(d_t),'casa':int(d_c),'colegio':int(d_co),'universidad':int(d_u),'otro':int(d_o)},
      'motivo':mot,'medio':{'apie':int(m_apie),'moto':int(m_moto),'auto':int(m_auto),'otro':int(m_otro)},
      'percepcion_texto':percepcion,'radios_texto':radios_txt,
      'radios':{'m100':int(r1),'m200':int(r2),'m300':int(r3),'mas300':int(r4)},
      'alternativa':alt,'alt_nota':alt_nota,'insights':ins,
    }
    tmpdir=tempfile.mkdtemp(); imgs={}
    for up,name in [(i1,'image1.jpeg'),(i2,'image2.png'),(i3,'image3.png'),(i4,'image4.jpeg'),(i5,'image5.jpeg')]:
        if up is not None:
            p=os.path.join(tmpdir,name); open(p,'wb').write(up.read()); imgs[name]=p
    out=os.path.join(tmpdir, f"REPORTE_EOD_{tienda.replace(' ','_').upper()}.docx")
    construir_reporte(d, PLANTILLA, out, imagenes=imgs or None)
    with open(out,'rb') as f:
        st.success("Reporte generado ✅")
        st.download_button("⬇️ Descargar Word", f, file_name=os.path.basename(out),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
