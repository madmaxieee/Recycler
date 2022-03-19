import { useRef } from "react";

import { useMapBox } from "../../hooks";

import styles from "./styles.module.css";

export const Map = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);

  const { mapBox } = useMapBox(mapContainerRef);

  return <div ref={mapContainerRef} className={styles.mapContainer} />;
};
