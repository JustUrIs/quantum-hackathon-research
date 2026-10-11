# Bundled CABA signal sample

`caba_signals.json` is a small, reproducible aggregation built by `../../tools/build_ambulance_data.py`. It contains unique injury-crash events by 8×8 cell, year, night/day, and highest recorded injury severity. It is a proxy for one class of emergency, not a record of all 107 calls, ambulance dispatches, response times, or causal risk.

Sources and distinct licenses:

- Buenos Aires City, *Siniestros viales* (hechos), 2019–2025; last updated 14 July 2026; source file `siniestros_viales_hechos.csv`; CC BY (as listed in the source catalog): https://data.buenosaires.gob.ar/dataset/victimas-siniestros-viales and https://cdn.buenosaires.gob.ar/datosabiertos/datasets/transporte-y-obras-publicas/victimas-siniestros-viales/siniestros_viales_hechos.csv
- Buenos Aires City, *Información censal por radio*, cartography `CABA_rc.geojson` (2010), updated in catalog September 2026; CC-BY-2.5-AR: https://data.buenosaires.gob.ar/dataset/informacion-censal-por-radio and https://cdn.buenosaires.gob.ar/datosabiertos/datasets/informacion-censal-por-radio/CABA_rc.geojson

The 2010 geography defines the historic CABA boundary mask and approximate spatial strata only. The app labels that year. Census population counts are not used as current demand weights. Project source code is MIT; that code license does not replace either dataset's attribution terms. The acquisition script downloads source files only when a maintainer explicitly runs it. Qollab itself has no network dependency.
