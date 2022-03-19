import { Button, Stack } from "@mui/material";
import { BinTable } from "./BinTable";
import { AddBin } from "./AddBin";

import type { BinContext, MapBoxContext } from "models";
import { useBin, useMapBox } from "contexts";

export const BinControls = () => {
  const { bins, setSelectedBins, selectedBins } = useBin() as BinContext;
  const { navigate } = useMapBox() as MapBoxContext;
  const handleSelect = (selectionModel: string[]) => {
    setSelectedBins(selectionModel);
  };
  const handleNavigate = () => {
    const data = selectedBins.map((id) => bins[id]);
    const start = [data[0].lng, data[0].lat].map(Number) as [number, number];
    const end = [data[1].lng, data[1].lat].map(Number) as [number, number];
    navigate(start, end);
  };
  return (
    <Stack gap="1em">
      <AddBin />
      <BinTable data={Object.values(bins)} handleSelect={handleSelect} />
      <Button
        variant="contained"
        onClick={handleNavigate}
        sx={{ width: "40%", mx: "auto" }}
      >
        navigate
      </Button>
    </Stack>
  );
};
