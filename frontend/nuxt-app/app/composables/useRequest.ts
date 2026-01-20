import { API_HOST, API_URL } from "./useUtils";
import { useStore } from "./useStore";

export const useRequest = () => {
  const { getToken } = useStore();

  const request = async (
    path: string,
    options: RequestInit = {}
  ): Promise<Response> => {
    // Construct full URL
    const url = `${API_URL}/${path}`;

    const headers = new Headers(options.headers);
    headers.set("Authorization", getToken() || "");

    const fetchOptions: RequestInit = {
      ...options,
      headers,
    };

    return fetch(url, fetchOptions);
  };

  // Convenience methods for common HTTP verbs
  const get = (path: string, options?: RequestInit) =>
    request(path, { ...options, method: "GET" });

  const post = (path: string, body?: any, options?: RequestInit) =>
    request(path, {
      ...options,
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

  const put = (path: string, body?: any, options?: RequestInit) =>
    request(path, {
      ...options,
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

  const patch = (path: string, body?: any, options?: RequestInit) =>
    request(path, {
      ...options,
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

  const del = (path: string, options?: RequestInit) =>
    request(path, { ...options, method: "DELETE" });

  return {
    request,
    get,
    post,
    put,
    patch,
    del,
  };
};
