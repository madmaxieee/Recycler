import { useRouter } from "next/router";
import { Button, Typography } from "@mui/material";

export const NavLink = ({ href }: { href: string }) => {
  const router = useRouter();
  const handleNavLink = () => {
    router.push(href);
  };
  return (
    <Button onClick={handleNavLink} variant="text">
      <Typography>{href}</Typography>
    </Button>
  );
};
