import { useEffect, useRef } from "react";

import { useMapBox } from "contexts";

import { MapBoxContext } from "models";

import styles from "./styles.module.css";

export const Map = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);

  const { mapBox, initMapBox } = useMapBox() as MapBoxContext;

  useEffect(() => {
    mapBox || initMapBox(mapContainerRef);
  });

  return <div ref={mapContainerRef} className={styles.mapContainer} />;
};
