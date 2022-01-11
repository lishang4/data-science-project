const version = 'v1';
const URL = `/api/${version}`;

/** Stocks */
function getStocks(searchParams) {
  const url = `${URL}/stocks`;
  // To avoid backend error,
  // give limitation when GET custom columns with undefined search params
  const params = (searchParams !== undefined) ? searchParams : {
    startdate: 20220111,
    enddate: 20220111,
    response: "json",
    type: "ALL",
  };
  return this.$reqGet(url, { params }).then(response => response.data);
}

function getStock(stockCode, searchParams) {
  const url = `${URL}/stock/${stockCode}`;
  // To avoid backend error,
  // give limitation when GET custom columns with undefined search params
  const params = (searchParams !== undefined) ? searchParams : {
    startdate: 20220111,
    enddate: 20220111,
    response: "json",
    type: "ALL",
  };
  return this.$reqGet(url, { params }).then(response => response.data);
}

function predictStockPrice(payload) {
  const url = `${URL}/stock/predict/price`;
  return this.$reqPost(url, payload);
}

export default {
  getStocks,
  getStock,
  predictStockPrice,
};
