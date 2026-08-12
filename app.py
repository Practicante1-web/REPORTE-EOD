# -*- coding: utf-8 -*-
"""App EOD — genera el reporte Word de una tienda desde los datos.
Correr con:  streamlit run app.py
"""
import streamlit as st, tempfile, os
from generar_reporte import construir_reporte, HIPPIES

st.set_page_config(page_title="Reporte EOD", page_icon="📍", layout="wide")
st.title("📍 Generador de Reporte EOD")
st.caption("Llena los datos de la tienda, sube los mapas/fotos y descarga el Word con el diseño de siempre.")

PLANTILLA = os.path.join(os.path.dirname(__file__), "plantilla_hippies.docx")
H = HIPPIES  # valores de ejemplo (Hippies) precargados

col1, col2 = st.columns(2)
with col1:
    st.subheader("Identificación")
    tienda   = st.text_input("Tienda", H['tienda'])
    periodo  = st.text_input("Periodo", H['periodo'])
    n_enc    = st.number_input("Nº de encuestas", value=H['n_encuestas'], step=1)
    trafico  = st.number_input("Tráfico 15/min", value=H['trafico'], step=1)

    st.subheader("Perfil del cliente")
    edad     = st.number_input("Edad promedio", value=H['edad'], step=1)
    gen_h    = st.number_input("Género H", value=H['gen_h'], step=1)
    gen_m    = st.number_input("Género M", value=H['gen_m'], step=1)
    estrato  = st.text_input("Estrato principal", str(H['estrato']))
    ocup_pct = st.number_input("Ocupación %", value=H['ocup_pct'], step=1)
    ocup_lbl = st.text_input("Ocupación principal", H['ocup_label'])

    st.subheader("Medio de llegada")
    m_apie = st.number_input("A pie", value=H['medio']['apie'], step=1)
    m_moto = st.number_input("Moto", value=H['medio']['moto'], step=1)
    m_auto = st.number_input("Automóvil", value=H['medio']['auto'], step=1)

with col2:
    st.subheader("Origen — De dónde viene")
    o_t = st.number_input("Origen · Trabajo", value=H['origen']['trabajo'], step=1)
    o_o = st.number_input("Origen · Otro", value=H['origen']['otro'], step=1)
    o_c = st.number_input("Origen · Casa", value=H['origen']['casa'], step=1)
    o_u = st.number_input("Origen · Universidad", value=H['origen']['universidad'], step=1)
    st.subheader("Destino — A dónde se dirige")
    d_t = st.number_input("Destino · Trabajo", value=H['destino']['trabajo'], step=1)
    d_o = st.number_input("Destino · Otro", value=H['destino']['otro'], step=1)
    d_c = st.number_input("Destino · Casa", value=H['destino']['casa'], step=1)
    d_u = st.number_input("Destino · Universidad", value=H['destino']['universidad'], step=1)
    st.subheader("Radios de influencia (conteos)")
    r1 = st.number_input("100m", value=H['radios']['m100'], step=1)
    r2 = st.number_input("200m", value=H['radios']['m200'], step=1)
    r3 = st.number_input("300m", value=H['radios']['m300'], step=1)
    r4 = st.number_input("+300m", value=H['radios']['mas300'], step=1)
    _sum = int(r1)+int(r2)+int(r3)+int(r4)
    if _sum:
        _p = lambda x: round(int(x)/_sum*100)
        st.caption(f"% sobre {_sum}: 100m {_p(r1)}% · 200m {_p(r2)}% · 300m {_p(r3)}% · +300m {_p(r4)}%")
        st.caption(f"Para la narrativa: 100m ({_p(r1)}%), 200m ({_p(r2)}%), 300m ({_p(r3)}%) y +300m ({_p(r4)}%)")
        if _sum != int(n_enc):
            st.warning(f"Ojo: los radios suman {_sum} y las encuestas son {int(n_enc)}. Normalmente deberían coincidir.")

st.divider()
c3, c4 = st.columns(2)
with c3:
    st.subheader("Principal motivo de compra (top 3)")
    mot=[]
    for i in range(3):
        l = st.text_input(f"Motivo {i+1}", H['motivo'][i][0] if i<len(H['motivo']) else "", key=f"ml{i}")
        c = st.number_input(f"Cant. {i+1}", value=H['motivo'][i][1] if i<len(H['motivo']) else 0, step=1, key=f"mc{i}")
        if l: mot.append((l,c))
with c4:
    st.subheader("Alternativa de compra (top 4)")
    alt=[]
    for i in range(4):
        l = st.text_input(f"Competidor {i+1}", H['alternativa'][i][0] if i<len(H['alternativa']) else "", key=f"al{i}")
        c = st.number_input(f"Respuestas {i+1}", value=H['alternativa'][i][1] if i<len(H['alternativa']) else 0, step=1, key=f"ac{i}")
        if l: alt.append((l,c))

st.divider()
st.subheader("Textos (los escribes tú)")
percepcion = st.text_area("Percepción del servicio", H['percepcion_texto'], height=80)
radios_txt = st.text_area("Narrativa de radios de influencia", H['radios_texto'], height=120)
alt_nota   = st.text_area("Nota alternativa de compra", H['alt_nota'], height=60)
st.markdown("**Insights clave**")
ins=[]
for i in range(3):
    t = st.text_input(f"Insight {i+1} · Título", H['insights'][i]['titulo'], key=f"it{i}")
    p1 = st.text_area(f"Insight {i+1} · Texto", H['insights'][i]['p1'], height=90, key=f"ip{i}")
    p2 = st.text_input(f"Insight {i+1} · Texto 2 (opcional)", H['insights'][i].get('p2',''), key=f"ip2{i}")
    ins.append({'titulo':t,'p1':p1,'p2':p2})

st.divider()
st.subheader("Imágenes (opcional — si no subes, quedan las de la plantilla)")
i1 = st.file_uploader("Foto de cabecera (fachada)", type=['jpg','jpeg','png'])
i2 = st.file_uploader("Mapa de radios (anillos)", type=['jpg','jpeg','png'])
i3 = st.file_uploader("Mapa de isócrona", type=['jpg','jpeg','png'])
i4 = st.file_uploader("Foto 1", type=['jpg','jpeg','png'])
i5 = st.file_uploader("Foto 2", type=['jpg','jpeg','png'])

if st.button("🚀 Generar reporte Word", type="primary"):
    d = {
      'tienda':tienda,'periodo':periodo,'n_encuestas':int(n_enc),'trafico':int(trafico),
      'edad':int(edad),'gen_h':int(gen_h),'gen_m':int(gen_m),'estrato':estrato,
      'ocup_pct':int(ocup_pct),'ocup_label':ocup_lbl,
      'origen':{'trabajo':int(o_t),'otro':int(o_o),'casa':int(o_c),'universidad':int(o_u)},
      'destino':{'trabajo':int(d_t),'otro':int(d_o),'casa':int(d_c),'universidad':int(d_u)},
      'motivo':mot,'medio':{'apie':int(m_apie),'moto':int(m_moto),'auto':int(m_auto)},
      'percepcion_texto':percepcion,'radios_texto':radios_txt,
      'radios':{'m100':int(r1),'m200':int(r2),'m300':int(r3),'mas300':int(r4)},
      'alternativa':alt,'alt_nota':alt_nota,'insights':ins,
    }
    imgs={}
    tmpdir=tempfile.mkdtemp()
    for up,name in [(i1,'image1.jpeg'),(i2,'image2.png'),(i3,'image3.png'),(i4,'image4.jpeg'),(i5,'image5.jpeg')]:
        if up is not None:
            p=os.path.join(tmpdir,name); open(p,'wb').write(up.read()); imgs[name]=p
    out=os.path.join(tmpdir, f"REPORTE_EOD_{tienda.replace(' ','_').upper()}.docx")
    construir_reporte(d, PLANTILLA, out, imagenes=imgs or None)
    with open(out,'rb') as f:
        st.success("Reporte generado ✅")
        st.download_button("⬇️ Descargar Word", f, file_name=os.path.basename(out),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
