import React, { useState } from "react";
import { Chart } from "./components/Chart";
import { StockSelector } from "./components/StockSelector";

function App() {
  const [selectedStock, setSelectedStock] = useState("");
  return (
    <div>
      {/* <StockSelector /> */}
      <Chart />
    </div>
  );
}

export default App;
