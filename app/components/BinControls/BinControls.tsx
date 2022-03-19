import { Stack } from "@mui/material";
import { BinTable } from "./BinTable";
import { AddBin } from "./AddBin";
import { useBin } from "hooks";

export const BinControls = () => {
  const { bins } = useBin();
  return (
    <Stack gap="1em">
      <AddBin />
      <BinTable data={bins} />
    </Stack>
  );
};
