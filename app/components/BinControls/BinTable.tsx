import * as React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";

import { BinData } from "models/api";

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 90 },
  {
    field: "location",
    headerName: "location",
    width: 100,
    editable: false,
  },
  {
    field: "coordinate",
    headerName: "coordinate",
    width: 120,
    editable: false,
  },
  {
    field: "status",
    headerName: "status",
    width: 70,
    editable: false,
  },
];

export const BinTable = ({ data }: { data: BinData[] }) => {
  const rows = data.map((data) => ({
    id: data.id,
    location: data.loc,
    coordinate: `${data.lat.slice(0, 6)}, ${data.lng.slice(0, 6)}`,
    status: `${
      Number(data.BoxFull === "0") +
      Number(data.BoxFull === "0") +
      Number(data.BoxFull === "0")
    }/3`,
  }));

  return (
    <div style={{ height: "40vh", width: "auto" }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={8}
        rowsPerPageOptions={[5]}
        checkboxSelection
      />
    </div>
  );
};
