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
    const currentPos = [121.561, 25.0434] as [number, number];
    const data = selectedBins.map((id) => bins[id]);
    const points = [
      currentPos,
      ...data.map((data) => [data.lng, data.lat].map(Number)),
    ] as [number, number][];

    function sorter(a: any, b: any) {
      if (a[1] > b[1]) return 1;
      if (a[1] < b[1]) return -1;
      else return 0;
    }

    if (points.length > 1) navigate(points.sort(sorter));
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
