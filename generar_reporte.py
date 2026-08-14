# -*- coding: utf-8 -*-
"""Motor: rellena la plantilla EOD (v2, categorías flexibles) con los datos de una tienda."""
import zipfile, shutil, os, re
from docx import Document

def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def pct(n, total): return 0 if not total else round(int(n)/total*100)

def _borrar_filas_vacias(path):
    """Elimina filas vacías SOLO en las tablas de datos (Competidor/Motivo),
    nunca el encabezado ni deja la tabla sin filas."""
    doc=Document(path)
    for t in doc.tables:
        cab=' '.join(c.text for c in t.rows[0].cells) if t.rows else ''
        if not any(k in cab for k in ('Competidor','Motivo')):
            continue  # tabla de maquetación u otra: no tocar
        for row in list(t.rows[1:]):  # nunca el encabezado
            if ''.join(c.text for c in row.cells).strip()=='':
                row._element.getparent().remove(row._element)
    doc.save(path)

def construir_reporte(d, plantilla, salida, imagenes=None):
    N=int(d['n_encuestas'])
    def np(n): return f"{n} ({pct(n,N)}%)"
    alt=d['alternativa']                      # lista (label,count) de largo variable
    alt_p=[pct(c,N) for _,c in alt]; mx=max(alt_p) if alt_p else 1
    def bar(p): return '█'*max(1,round(p/mx*26)) if p else ''

    vals={
      'tienda':d['tienda'],'periodo':d['periodo'],'n_encuestas':N,'trafico':d['trafico'],
      'edad':d['edad'],'gen_h':d['gen_h'],'gen_m':d['gen_m'],'estrato':d['estrato'],
      'ocup_pct':f"{d['ocup_pct']}%",'ocup_label':d['ocup_label'],
      'o_trabajo':np(d['origen']['trabajo']),'o_otro':np(d['origen']['otro']),
      'o_casa':np(d['origen']['casa']),'o_univ':np(d['origen']['universidad']),
      'o_colegio':np(d['origen'].get('colegio',0)),
      'd_trabajo':np(d['destino']['trabajo']),'d_otro':np(d['destino']['otro']),
      'd_casa':np(d['destino']['casa']),'d_univ':np(d['destino']['universidad']),
      'd_colegio':np(d['destino'].get('colegio',0)),
      'medio_apie':d['medio']['apie'],'medio_moto':d['medio']['moto'],
      'medio_auto':d['medio']['auto'],'medio_otro':d['medio'].get('otro',0),
      'percepcion_texto':d['percepcion_texto'],'radios_texto':d['radios_texto'],
      'r100':d['radios']['m100'],'r200':d['radios']['m200'],'r300':d['radios']['m300'],'rmas':d['radios']['mas300'],
      'alt_nota':d['alt_nota'],
      'ins1_tit':d['insights'][0]['titulo'],'ins1_p1':d['insights'][0]['p1'],'ins1_p2':d['insights'][0].get('p2',''),
      'ins2_tit':d['insights'][1]['titulo'],'ins2_p1':d['insights'][1]['p1'],
      'ins3_tit':d['insights'][2]['titulo'],'ins3_p1':d['insights'][2]['p1'],
    }
    mot=d['motivo']
    for i in range(3):
        if i<len(mot) and mot[i][0]:
            l,c=mot[i]; vals[f'mot{i+1}_lbl']=l; vals[f'mot{i+1}_n']=c; vals[f'mot{i+1}_p']=f"{pct(c,N)}%"
        else:
            vals[f'mot{i+1}_lbl']='';vals[f'mot{i+1}_n']='';vals[f'mot{i+1}_p']=''
    for i in range(6):
        if i<len(alt) and alt[i][0]:
            l,c=alt[i]; p=pct(c,N)
            vals[f'alt{i+1}_lbl']=l;vals[f'alt{i+1}_n']=c;vals[f'alt{i+1}_p']=f"{p}%";vals[f'alt{i+1}_bar']=bar(p)
        else:
            for k in ('lbl','n','p','bar'): vals[f'alt{i+1}_{k}']=''

    # 1) rellenar tokens + (opcional) imágenes
    tmp=salida+'.tmp'
    with zipfile.ZipFile(plantilla,'r') as zin, zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            data=zin.read(item)
            if item=='word/document.xml':
                xml=data.decode('utf-8')
                for k,v in vals.items(): xml=xml.replace(f'⟦{k}⟧', esc(v))
                xml=re.sub(r'⟦[a-z0-9_]+⟧','',xml)
                data=xml.encode('utf-8')
            elif imagenes and item.startswith('word/media/'):
                fn=item.split('/')[-1]
                if imagenes.get(fn) and os.path.exists(imagenes[fn]): data=open(imagenes[fn],'rb').read()
            zout.writestr(item,data)
    os.replace(tmp,salida)
    # 2) borrar filas de tabla vacías (alternativa/motivo no usados)
    _borrar_filas_vacias(salida)
    return salida

HIPPIES={
 'tienda':'Hippies Cra 7','periodo':'Julio 2026','n_encuestas':318,'trafico':122,
 'edad':29,'gen_h':184,'gen_m':134,'estrato':3,'ocup_pct':57,'ocup_label':'Empleado',
 'origen':{'trabajo':142,'otro':69,'casa':56,'universidad':51,'colegio':8},
 'destino':{'trabajo':150,'otro':72,'casa':61,'universidad':35,'colegio':3},
 'motivo':[('Surtido',96),('Cercanía',77),('Precios',58)],
 'medio':{'apie':283,'moto':20,'auto':11,'otro':4},
 'percepcion_texto':'El 86% de los clientes percibe el servicio de manera muy positiva, valorando el servicio con la puntuación máxima de 5 estrellas.',
 'radios_texto':'La mayoría de los clientes están en los primeros tres anillos: 100m (27%), 200m (35%) y 300m (32%). Entre los tres, los primeros 300m reúnen el 93% de los encuestados; más allá quedan solo (7%). Lo más fuerte es la franja de 200–300m: además del que pasa caminando, llega gente desde las universidades cercanas, el Parque de los Hippies y las carreras 7 y 9. Con un 89% que llega a pie y una tienda que sirve de paso hacia el parque. ',
 'radios':{'m100':85,'m200':110,'m300':102,'mas300':21},
 'alternativa':[('Tienda de barrio',123),('D1',61),('Éxito',42),('Carulla',15)],
 'alt_nota':'El 20% de los encuestados afirma que no tiene una alternativa clara de compra frente a OXXO.',
 'insights':[
   {'titulo':'Cliente joven, de a pie y en tránsito universitario y laboral',
    'p1':'El cliente típico es un adulto de 29 años, estrato 3 y empleado, con leve mayoría masculina. El flujo dominante es laboral viene del trabajo (45%) y va hacia él (47%), pero se monta sobre un entorno universitario (La Salle, SENA, Politécnico Gran Colombiano) y el Parque de los Hippies, que suma un público joven que usa la tienda como punto de encuentro. Ese componente aparece en el 22% que llega "de otro"',
    'p2':'Origen: no es solo gente de paso al trabajo, también quien se reúne en la zona.'},
   {'titulo':'Compite contra la tienda de barrio, y pierde por surtido',
    'p1':'El competidor real es la tienda de barrio, muy por encima de D1 y Éxito. Y cuando el cliente contempla irse a otra opción, lo que más pesa es el surtido, por encima de la cercanía y el precio. Es decir: OXXO Hippies gana en ubicación y sostiene el precio, pero cede frente a quien ofrece más variedad. Aun así, hay margen a favor: el 20% no tiene una alternativa clara.'},
   {'titulo':'Consumo inmediato',
    'p1':'El perfil de paso rápido se refleja en lo que más rota: bebidas isotónicas y bebidas calientes, jaladas por su rol de punto de reunión estudiantil junto al parque. Es una tienda de consumo inmediato y encuentro, no de despensa.'},
 ],
}
if __name__=='__main__':
    construir_reporte(HIPPIES,'plantilla_v2.docx','/tmp/hip/prueba_v2.docx')
    print("Generado prueba_v2.docx")
