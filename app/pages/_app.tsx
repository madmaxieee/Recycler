import type { AppProps } from "next/app";
import "../styles/globals.css";
import "../styles/mapbox-controls.css";

import { ChakraProvider } from "@chakra-ui/react";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
      <Component {...pageProps} />
    </ChakraProvider>
  );
}

export default MyApp;
