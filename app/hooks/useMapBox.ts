import React, { useRef, useEffect, useState } from "react";

import mapboxgl from "mapbox-gl";

export const useMapBox = (
  mapContainerRef: React.MutableRefObject<HTMLDivElement | null>
) => {
  const mapBoxRef = useRef<mapboxgl.Map | null>(null);

  const [lng, setLng] = useState<number>(121.561);
  const [lat, setLat] = useState<number>(25.0434);
  const [zoom, setZoom] = useState<number>(16);

  useEffect(() => {
    if (mapBoxRef.current) return; // initialize map only once

    mapboxgl.accessToken =
      "pk.eyJ1IjoibWFkbWF4aWUiLCJhIjoiY2wweGRkeHc5MHFsbzNpam4yZG9qZWlmaiJ9.egfKHT6AjDyhiw7rX1mQbQ";

    mapBoxRef.current = new mapboxgl.Map({
      container: mapContainerRef.current as HTMLDivElement,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [lng, lat],
      zoom: zoom,
    });
  });

  const goto = (lng: number, lat: number) => {
    setLat(lat);
    setLng(lng);
  };

  return { mapBox: mapBoxRef.current, setZoom };
};
