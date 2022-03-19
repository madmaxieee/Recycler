import { useState } from "react";

import { Stack, TextField, Button } from "@mui/material";

export const AddBin = () => {
  const [newBinName, setNewBinName] = useState<string>("");
  const [lat, setLat] = useState(121);
  const [lng, setLng] = useState(25);

  const handleNameChange: React.ChangeEventHandler<
    HTMLInputElement | HTMLTextAreaElement
  > = (e) => {
    setNewBinName(e.target.value);
  };

  return (
    <Stack direction="row" gap="1em" alignItems="center">
      <TextField
        autoFocus
        size="small"
        margin="dense"
        label="id"
        variant="outlined"
        value={newBinName}
        onChange={handleNameChange}
      />
      <TextField
        size="small"
        margin="dense"
        label="location"
        variant="outlined"
        value={newBinName}
        onChange={handleNameChange}
      />
      <TextField
        size="small"
        margin="dense"
        label="latitude"
        variant="outlined"
        value={lat}
        onChange={(e) =>
          setLat(isNaN(Number(e.target.value)) ? 0 : Number(e.target.value))
        }
      />
      <TextField
        size="small"
        margin="dense"
        label="longitude"
        variant="outlined"
        value={lng}
        onChange={(e) =>
          setLng(isNaN(Number(e.target.value)) ? 0 : Number(e.target.value))
        }
      />
      <Button size="small" variant="text" sx={{ height: "2.5em" }}>
        Add
      </Button>
    </Stack>
  );
};
