# tile-cover-docker

[MapBox Tile-Cover](https://github.com/mapbox/tile-cover)<br/>
[MapBox Supermercado](https://github.com/mapbox/supermercado)

```
.
├── COMMAND
├── Dockerfile
├── LICENSE
├── README.md
├── analysis_params.json
├── docker-compose.yml
├── initial_data
│   └── uk_official.geojson
├── received_data
│   ├── geoid_qtid.csv
│   ├── intermediate.json
│   └── qtid_geoid.csv
├── requirements.txt
├── tile_cover.js
├── tile_cover.py
├── tile_cover.sh
└── tilecover_params.json.example
```

```bash
docker-compose build analysis && docker-compose up -d db && docker-compose run analysis
docker-compose exec db psql postgresql://analysis:analysis@localhost:5432/analysis
#docker-compose down
```

`analysis_params.json`

```json
{
    "conn": "postgresql://analysis:analysis@db:5432/analysis",
    "start": 9200,
    "end": 9205,
    "geoid": "RMSect",
    "min": 1,
    "max": 14,
    "input": "opt/initial_data/uk_official.geojson",
    "output": "opt/received_data/intermediate.json",
    "tablename": "res"
}
```