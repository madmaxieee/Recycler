import * as React from "react";
import AppBar from "@mui/material/AppBar";

import { Logo } from "components";
import { NavLink } from "./NavLink";
import { Box, Toolbar } from "@mui/material";

const pages = [
  // "Home",
  "Dashboard"
];

export const NavBar = () => {
  return (
    <AppBar position="static" color="transparent">
      <Toolbar sx={{ minHeight: "6vh", width: "80vw", mx: "auto" }}>
        <Logo />
        <Box
          sx={{
            display: "flex",
            ml: "2vw",
            gap: "1vw",
          }}
        >
          {pages.map((page) => (
            <NavLink key={page} href={page} />
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};
