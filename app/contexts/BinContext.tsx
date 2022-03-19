import { BinData, BinContext } from "../models";
import React, { useEffect, useState, useContext, ReactNode } from "react";

const BinContext = React.createContext<BinContext | null>(null);

export const useBin = () => useContext(BinContext);

export const BinContextProvider = ({ children }: { children: ReactNode }) => {
  const [bins, setBins] = useState<{ [id: string]: BinData }>({});
  const [selectedBins, setSelectedBins] = useState<string[]>([]);

  const refreshBins = async () => {
    const reponse = await fetch("/api/bins");
    const dataArray: BinData[] = await reponse.json();
    const result: { [id: string]: BinData } = {};
    dataArray.forEach((data) => {
      result[data.id] = data;
    });
    setBins(result);
  };

  useEffect(() => {
    refreshBins();
    setInterval(() => refreshBins(), 15000);
  }, []);

  return (
    <BinContext.Provider value={{ bins, selectedBins, setSelectedBins }}>
      {children}
    </BinContext.Provider>
  );
};
