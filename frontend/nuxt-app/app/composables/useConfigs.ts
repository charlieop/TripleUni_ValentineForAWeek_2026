export const API_HOST =
  process.env.NODE_ENV === "development"
    ? "http://10.0.0.77:8000"
    : "https://api.charlieop.com";

export const API_URL = API_HOST + "/v1";

export const APPID = "wx09ec18a3cf830379";
