import type { NextPage } from "next";

import { Box, Stack } from "@mui/material";
import { NavBar, Map, BinControls } from "components";

const Dashboard: NextPage = () => {
  return (
    <Stack width="100vw">
      <NavBar />
      <Stack
        direction="row"
        gap="4vw"
        alignItems="start"
        sx={{ minHeight: "100vh", pt: "5em", mx: "auto" }}
      >
        <Map />
        <Box sx={{ width: "30vw" }}>
          <BinControls />
        </Box>
      </Stack>
    </Stack>
  );
};

export default Dashboard;
