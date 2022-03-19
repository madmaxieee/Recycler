import type { NextPage } from "next";

import { VStack, Box } from "@chakra-ui/react";
import { NavBar, Footer, Map } from "../components";

const Dashboard: NextPage = () => {
  return (
    <VStack width="100vw">
      <NavBar />
      <Box minH="100vh">
        <Map />
      </Box>
      <Footer />
    </VStack>
  );
};

export default Dashboard;
