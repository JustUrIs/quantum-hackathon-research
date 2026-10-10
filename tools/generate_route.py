"""Reproduce WMM route fixture with pygeomag 1.1.0 (WMM2025).

Requires only during data generation: pip install pygeomag==1.1.0.
Runtime projects do not need this package or network.
"""

import json
import math
from pathlib import Path
from pygeomag import GeoMag

ROOT = Path(__file__).resolve().parents[1]
model = GeoMag()
# Independently published NOAA reference points, rounded to 0.1 nT.
# https://www.ncei.noaa.gov/sites/default/files/2025-02/WMM2025_TEST_VALUES.txt
for lat, lon, expected in [(80, 0, 55178.5), (0, 120, 41064.3), (-80, 240, 54698.2)]:
    check = model.calculate(glat=lat, glon=lon, alt=0, time=2025)
    if abs(check.f - expected) > 0.15:
        raise AssertionError(
            f"WMM reference mismatch at {lat},{lon}: {check.f} vs {expected}"
        )
points = []


# Spherical great-circle interpolation, EZE region to Ushuaia, altitude 10 km.
def vector(lat, lon):
    a, b = map(math.radians, (lat, lon))
    return [math.cos(a) * math.cos(b), math.cos(a) * math.sin(b), math.sin(a)]


start, end = vector(-34.6037, -58.3816), vector(-54.8019, -68.3030)
omega = math.acos(sum(a * b for a, b in zip(start, end)))
for step in range(41):
    t = step / 40
    v = [
        (math.sin((1 - t) * omega) * a + math.sin(t * omega) * b) / math.sin(omega)
        for a, b in zip(start, end)
    ]
    lat, lon = math.degrees(math.asin(v[2])), math.degrees(math.atan2(v[1], v[0]))
    r = model.calculate(glat=lat, glon=lon, alt=10, time=2026.775)
    points.append(
        {
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "distance_km": round(6371 * omega * t, 3),
            "field_ut": round(r.f / 1000, 5),
            "horizontal_ut": round(r.h / 1000, 5),
            "declination_deg": round(r.d, 5),
            "inclination_deg": round(r.i, 5),
        }
    )
data = {
    "model": "WMM2025",
    "generator": "pygeomag 1.1.0",
    "date_decimal": 2026.775,
    "altitude_km": 10,
    "source": "https://www.ncei.noaa.gov/products/world-magnetic-model",
    "doi": "https://doi.org/10.25921/aqfd-sd83",
    "route": "Buenos Aires to Ushuaia",
    "notice": "Derived from NOAA/BGS WMM2025. US government WMM material is public domain. Model outputs are not measured flight data. Route is illustrative and not for navigation.",
    "points": points,
}
out = ROOT / "lost-signal-qollab/data/route.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print(
    f"Generated {len(points)} route points: {points[0]['field_ut']} to {points[-1]['field_ut']} uT"
)
