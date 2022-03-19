import type { NextPage } from "next";

import { Hero, NavBar, Footer } from "../components";
import { Box, VStack } from "@chakra-ui/react";

const Home: NextPage = () => {
  return (
    <VStack width="100vw">
      <NavBar />
      <Box minH="100vh">
        <Hero />
      </Box>
      <Footer />
    </VStack>
  );
};

export default Home;
