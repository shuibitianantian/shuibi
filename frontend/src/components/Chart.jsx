import React, { useEffect } from "react";
import { getHistoricalData } from "../apis";

export const Chart = () => {
  useEffect(() => {
    const getData = async () => {
      const data = await getHistoricalData("aapl");
      console.log(data);
    };
    getData();
  }, []);

  return <></>;
};
