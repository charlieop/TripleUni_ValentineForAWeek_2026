export const API_HOST =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8000"
    // ? "http://172.20.10.3:8000"
    : "https://api.charlieop.com";

export const API_URL = API_HOST + "/v1";

export const APPID = "wx09ec18a3cf830379";
