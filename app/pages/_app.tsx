import type { AppProps } from "next/app";
import "../styles/globals.css";
import "../styles/mapbox-controls.css";

import { BinContextProvider, MapBoxContextProvider } from "../contexts";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <MapBoxContextProvider>
      <BinContextProvider>
        <Component {...pageProps} />
      </BinContextProvider>
    </MapBoxContextProvider>
  );
}

export default MyApp;
