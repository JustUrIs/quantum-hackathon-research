"""Download published public sources; build the small offline CABA demo fixture.

This runs at development time. The Qollab project reads only its bundled JSON.
"""
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp" / "ambulance-source"
OUT = ROOT / "ambulancias-qollab" / "data" / "caba_signals.json"
TMP.mkdir(parents=True, exist_ok=True)
SOURCES = {
    "incidents.csv": "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/transporte-y-obras-publicas/victimas-siniestros-viales/siniestros_viales_hechos.csv",
    "radios.geojson": "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/informacion-censal-por-radio/CABA_rc.geojson",
}

def fetch(name, url):
    target = TMP / name
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "GuardiaGridHackathon/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response, target.open("wb") as out:
            out.write(response.read())
    return target

def polygons(geometry):
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"]]
    if geometry["type"] == "MultiPolygon":
        return geometry["coordinates"]
    return []

def ring_centroid(ring):
    area2 = cx = cy = 0.0
    for (x1,y1),(x2,y2) in zip(ring,ring[1:]):
        cross=x1*y2-x2*y1
        area2+=cross;cx+=(x1+x2)*cross;cy+=(y1+y2)*cross
    if abs(area2)<1e-12:
        points=ring[:-1] or ring
        return (sum(p[0] for p in points)/len(points),sum(p[1] for p in points)/len(points))
    return cx/(3*area2),cy/(3*area2)

def point_in_ring(x,y,ring):
    inside=False
    for (x1,y1),(x2,y2) in zip(ring,ring[1:]):
        if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1:
            inside=not inside
    return inside

def main():
    files={name:fetch(name,url) for name,url in SOURCES.items()}
    geo=json.loads(files["radios.geojson"].read_text(encoding="utf-8"))
    radios=[]; bounds=[math.inf,-math.inf,math.inf,-math.inf]
    for feature in geo["features"]:
        geom=feature["geometry"]
        for poly in polygons(geom):
            ring=poly[0]
            if len(ring)<4: continue
            b=(min(p[0] for p in ring),max(p[0] for p in ring),min(p[1] for p in ring),max(p[1] for p in ring))
            radios.append((ring,b,feature["properties"]))
            bounds=[min(bounds[0],b[0]),max(bounds[1],b[1]),min(bounds[2],b[2]),max(bounds[3],b[3])]
    west,east,south,north=bounds
    # Bounds are derived from the city's published census radios, not hand drawn.
    events={}
    with files["incidents.csv"].open(encoding="utf-8-sig",newline="") as source:
        rows=csv.DictReader(source,delimiter=";")
        for row in rows:
            try:
                lon=float(row["longitud_siniestro"]);lat=float(row["latitud_siniestro"])
                if not west<=lon<=east or not south<=lat<=north: continue
                if not any(b[0]<=lon<=b[1] and b[2]<=lat<=b[3] and point_in_ring(lon,lat,r) for r,b,_ in radios): continue
                key=row["id_siniestro"].strip()
                if not key: continue
                year=int(row["anio_siniestro"]);hour=int(row["hora_siniestro"].split(":",1)[0])
                severity=row["gravedad_siniestro"].strip().upper()
                grade={"LEVE":1,"GRAVE":2,"MORTAL":3,"FATAL":3}.get(severity,0)
                event=events.get(key)
                if event is None:
                    events[key]={"lon":lon,"lat":lat,"year":year,"night":int(hour>=19 or hour<7),"grade":grade}
                else:
                    event["grade"]=max(event["grade"],grade)
            except (KeyError,ValueError,TypeError):
                continue
    if not events: raise RuntimeError("No crash events survived CABA boundary filtering; inspect source schema.")
    nx=ny=8
    bins=[[{"events":0,"serious":0,"fatal":0,"night":0,"recent":0} for _ in range(nx)] for _ in range(ny)]
    for event in events.values():
        x=min(nx-1,max(0,int((event["lon"]-west)/(east-west)*nx)))
        y=min(ny-1,max(0,int((event["lat"]-south)/(north-south)*ny)))
        cell=bins[ny-1-y][x]
        cell["events"]+=1
        cell["serious"]+=int(event["grade"]>=2)
        cell["fatal"]+=int(event["grade"]==3)
        cell["night"]+=event["night"]
        cell["recent"]+=int(event["year"]==2025)
    # Eight representative public census-radio centroids describe scenario locations.
    # They are NOT verified lots, active ambulance bases, or operational suggestions.
    groups=defaultdict(list)
    for ring,b,properties in radios:
        lon,lat=ring_centroid(ring)
        col=min(3,max(0,int((lon-west)/(east-west)*4)))
        row=min(1,max(0,int((lat-south)/(north-south)*2)))
        population=float(properties.get("POBLACION") or 0)
        groups[(row,col)].append((population,lon,lat,properties.get("RADIO_ID")))
    sites=[]
    for row in range(2):
        for col in range(4):
            candidates=groups[(row,col)]
            if not candidates:
                continue
            pop,lon,lat,radio_id=max(candidates)
            sites.append({"id":f"R{row+1}{col+1}","lon":lon,"lat":lat,
                          "census_radio":radio_id,"site_type":"hypothetical census-radio representative"})
    mask=[]
    for j in range(32):
        lat=north-(j+0.5)*(north-south)/32
        for i in range(32):
            lon=west+(i+0.5)*(east-west)/32
            mask.append(int(any(b[0]<=lon<=b[1] and b[2]<=lat<=b[3] and point_in_ring(lon,lat,r) for r,b,_ in radios)))
    result={"schema":"guardia-grid/caba-signals-v1","source_period":[2019,2025],
            "source_event_rows_license":"CC BY (Buenos Aires City open data catalog)",
            "boundary":{"west":west,"east":east,"south":south,"north":north,"mask_side":32,"mask":mask,
                        "source":"CABA_rc census radio polygons, 2010; boundary/cartography only"},
            "demand_grid":{"columns":nx,"rows":ny,"cells":bins},"sites":sites,
            "counts":{"unique_injury_crash_events":len(events),
                      "serious_or_fatal_events":sum(c["serious"] for r in bins for c in r),
                      "fatal_events":sum(c["fatal"] for r in bins for c in r),
                      "geography":"Events point-in-polygon filtered to published CABA census radios."},
            "sources":[{"name":"Siniestros viales (hechos), 2019-2025","url":SOURCES["incidents.csv"],
                         "catalog":"https://data.buenosaires.gob.ar/dataset/victimas-siniestros-viales","updated":"2026-07-14","license":"CC BY"},
                        {"name":"Información censal por radio, CABA_rc.geojson","url":SOURCES["radios.geojson"],
                         "catalog":"https://data.buenosaires.gob.ar/dataset/informacion-censal-por-radio","updated":"2026-09-30","license":"CC-BY-2.5-AR"}]}
    OUT.write_text(json.dumps(result,separators=(",",":"),ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(OUT.relative_to(ROOT)),"bytes":OUT.stat().st_size,"counts":result["counts"],"sites":len(sites),"bounds":result["boundary"]|{"mask":"omitted"}},indent=2,ensure_ascii=False))

if __name__=="__main__": main()
