import { useEffect, useState } from "react";

import { BinData } from "models/api";

export const useBin = () => {
  const [bins, setBins] = useState<BinData[]>([]);
  const refreshBins = async () => {
    const reponse = await fetch("/api/bins");
    setBins(await reponse.json());
  };
  useEffect(() => {
    refreshBins();
    setInterval(() => refreshBins(), 15000);
  }, []);
  return { bins };
};
