import type { NextPage } from "next";

import { NavBar } from "components";
import { Box, Stack } from "@mui/material";

const Home: NextPage = () => {
  return (
    <Stack width="100vw">
      <NavBar />
      <Box sx={{ minHeight: "100vh" }}></Box>
      {/* <Footer /> */}
    </Stack>
  );
};

export default Home;
