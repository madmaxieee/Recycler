import { BinData, BinContext } from "../models";
import React, {
  useEffect,
  useState,
  useContext,
  useCallback,
  ReactNode,
} from "react";

import _ from "lodash";

const BinContext = React.createContext<BinContext | null>(null);

export const useBin = () => useContext(BinContext);

export const BinContextProvider = ({ children }: { children: ReactNode }) => {
  const [bins, setBins] = useState<{ [id: string]: BinData }>({});
  const [selectedBins, setSelectedBins] = useState<string[]>([]);

  const refreshBins = useCallback(async () => {
    const reponse = await fetch("/api/bins");
    const dataArray: BinData[] = await reponse.json();
    const result: { [id: string]: BinData } = {};
    dataArray.forEach((data) => {
      result[data.id] = data;
    });
    if (!_.isEqual(bins, result)) {
      setBins(result);
    }
  }, [bins]);

  useEffect(() => {
    refreshBins();
    const interval = setInterval(() => refreshBins(), 2000);
    return () => clearInterval(interval);
  }, [refreshBins]);

  useEffect(() => {
    console.log("bin refreshed", bins);
  }, [bins]);

  return (
    <BinContext.Provider value={{ bins, selectedBins, setSelectedBins }}>
      {children}
    </BinContext.Provider>
  );
};
