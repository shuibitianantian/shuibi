import { companyInfo } from "./contants";

const buildQueryString = (symbol) => {
  return `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?metrics=high?&interval=1d&range=max`;
};

export const getCompanyInfo = async () => {
  const headers = new Headers();

  headers.append("Content-Type", "application/json");

  const data = await fetch(companyInfo, {
    method: "GET",
    headers,
  });

  return await data.json();
};

export const getHistoricalData = async (symbol) => {
  const queryString = buildQueryString(symbol);
  const data = await fetch(queryString);
  return data.json();
};
