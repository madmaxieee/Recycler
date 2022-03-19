import type { MapBoxContext } from "../models";
import React, {
  useEffect,
  useState,
  useContext,
  ReactNode,
  useRef,
} from "react";

import mapboxgl from "mapbox-gl";

const MapBoxContext = React.createContext<MapBoxContext | null>(null);

export const useMapBox = () => useContext(MapBoxContext);

export const MapBoxContextProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const mapBoxRef = useRef<mapboxgl.Map | null>(null);

  const [lng, setLng] = useState<number>(121.561);
  const [lat, setLat] = useState<number>(25.0434);
  const zoom = 16;

  const initMapBox = (
    mapContainerRef: React.MutableRefObject<HTMLDivElement | null>
  ) => {
    mapboxgl.accessToken =
      "pk.eyJ1IjoibWFkbWF4aWUiLCJhIjoiY2wweGRkeHc5MHFsbzNpam4yZG9qZWlmaiJ9.egfKHT6AjDyhiw7rX1mQbQ";

    mapBoxRef.current = new mapboxgl.Map({
      container: mapContainerRef.current as HTMLDivElement,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [lng, lat],
      zoom,
    });
  };

  const navigate = async (start: [number, number], end: [number, number]) => {
    // make a directions request using cycling profile
    // an arbitrary start will always be the same
    // only the end or destination will change
    const query = await fetch(
      `https://api.mapbox.com/directions/v5/mapbox/cycling/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
      { method: "GET" }
    );
    const json = await query.json();
    console.log(start, end);
    console.log(json);
    const data = json.routes[0];
    const route = data.geometry.coordinates;
    const geojson = {
      type: "Feature",
      properties: {},
      geometry: {
        type: "LineString",
        coordinates: route,
      },
    };
    // if the route already exists on the map, we'll reset it using setData
    if (mapBoxRef.current && mapBoxRef.current.getSource("route")) {
      mapBoxRef.current.getSource("route").setData(geojson);
    }
    // otherwise, we'll make a new request
    else {
      mapBoxRef.current &&
        mapBoxRef.current.addLayer({
          id: "route",
          type: "line",
          source: {
            type: "geojson",
            data: geojson,
          },
          layout: {
            "line-join": "round",
            "line-cap": "round",
          },
          paint: {
            "line-color": "#3887be",
            "line-width": 5,
            "line-opacity": 0.75,
          },
        });
    }
    // add turn instructions here at the end
  };

  const goto = (lng: number, lat: number) => {
    setLng(lng);
    setLat(lat);
  };

  return (
    <MapBoxContext.Provider
      value={{ mapBox: mapBoxRef.current, goto, navigate, initMapBox }}
    >
      {children}
    </MapBoxContext.Provider>
  );
};
