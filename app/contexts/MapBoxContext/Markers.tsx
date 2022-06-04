import mapboxgl from "mapbox-gl";
import { MarkerData } from "models";

class MarkersSingleton {
  markers: mapboxgl.Marker[] = [];
  markerData: MarkerData[] = [];
  _map?: mapboxgl.Map;

  constructor() {}

  attach(map: mapboxgl.Map) {
    this._map = map;

    return this;
  }

  setMarkers(markerData: MarkerData[]) {
    if (this._map) {
      this.markers = markerData.map((data) => {
        return new mapboxgl.Marker()
          .setLngLat([Number(data.lng), Number(data.lat)])
          .addTo(this._map as mapboxgl.Map);
      });
    }
    this.markerData = markerData;
    return this;
  }

  showMarkers() {
    this.markers.forEach((marker) => {
      this._map && marker.addTo(this._map);
    });
    return this;
  }

  hideMarkers() {
    this.markers.forEach((marker) => {
      marker.remove();
    });
    return this;
  }

  refreshMarkers() {
    this.hideMarkers();
    this.setMarkers(this.markerData);
    return this;
  }
}

export const Markers = new MarkersSingleton();
