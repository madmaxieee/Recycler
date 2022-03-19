import { useRef, useState, useEffect } from "react";

export const Map = () => {
  const mapRef = useRef();
  // @ts-ignore
  return <div ref={mapRef}></div>;
};
