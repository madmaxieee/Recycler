import type { MapBoxContext, BinContext } from "models";
import React, {
  useState,
  useContext,
  ReactNode,
  useRef,
  useEffect,
} from "react";

import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

import { Markers } from "./Markers";

import { useBin } from "contexts";

const MapBoxContext = React.createContext<MapBoxContext | null>(null);

export const useMapBox = () => useContext(MapBoxContext);

export const MapBoxContextProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const mapBoxRef = useRef<mapboxgl.Map | null>(null);

  const { bins } = useBin() as BinContext;

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

    mapBoxRef.current.on("load", () => {
      console.log("load");
      console.log("bins", bins);
      mapBoxRef.current && Markers.attach(mapBoxRef.current).refreshMarkers();
    });
  };

  useEffect(() => {
    console.log("effect");
    console.log("bins", bins);
    Markers.setMarkers(
      Object.values(bins).map((bin) => ({
        loc: bin.loc,
        lng: bin.lng,
        lat: bin.lat,
      }))
    );
  }, [bins, mapBoxRef]);

  const navigate = async (points: [number, number][]) => {
    // make a directions request using cycling profile
    // an arbitrary start will always be the same
    // only the end or destination will change
    const pointsString = points.map((point) => String(point)).join(";");
    const query = await fetch(
      `https://api.mapbox.com/directions/v5/mapbox/cycling/${pointsString}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
      { method: "GET" }
    );
    const json = await query.json();
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
      // @ts-ignore
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
            // @ts-ignore
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
