from fastapi import FastAPI
from pydantic import BaseModel
from pyproj import Transformer

app = FastAPI()

class CoordinateRequest(BaseModel):
    lat: float
    lon: float
    from_epsg: int
    to_epsg: int

def convert_coordinates(lat, lon, from_epsg, to_epsg):
    transformer = Transformer.from_crs(f"EPSG:{from_epsg}", f"EPSG:{to_epsg}", always_xy=True)
    new_lon, new_lat = transformer.transform(lon, lat)
    return new_lat, new_lon

@app.post("/convert/")
def convert_coords(request: CoordinateRequest):
    new_lat, new_lon = convert_coordinates(request.lat, request.lon, request.from_epsg, request.to_epsg)
    return {"new_lat": new_lat, "new_lon": new_lon}

# Run the API using: uvicorn geodesic_api:app --reload
