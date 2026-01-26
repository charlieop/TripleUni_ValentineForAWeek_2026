import { API_URL } from "./useConfigs";
import { useStore } from "./useStore";
import { useLoading } from "./useLoading";

export const useRequest = () => {
  const { getToken } = useStore();
  const { startLoading, stopLoading } = useLoading();

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

    startLoading();
    try {
      const response = await fetch(url, fetchOptions);
      return response;
    } finally {
      stopLoading();
    }
  };

  // Convenience methods for common HTTP verbs
  const get = (path: string, options?: RequestInit) =>
    request(path, { ...options, method: "GET" });

  const post = (path: string, body?: any, options?: RequestInit) => {
    const isFormData = body instanceof FormData;
    return request(path, {
      ...options,
      method: "POST",
      body: isFormData ? body : body ? JSON.stringify(body) : undefined,
      headers: isFormData
        ? {
            ...options?.headers,
          }
        : {
            "Content-Type": "application/json",
            ...options?.headers,
          },
    });
  };

  const put = (path: string, body?: any, options?: RequestInit) => {
    const isFormData = body instanceof FormData;
    return request(path, {
      ...options,
      method: "PUT",
      body: isFormData ? body : body ? JSON.stringify(body) : undefined,
      headers: isFormData
        ? {
            ...options?.headers,
          }
        : {
            "Content-Type": "application/json",
            ...options?.headers,
          },
    });
  };

  const patch = (path: string, body?: any, options?: RequestInit) => {
    const isFormData = body instanceof FormData;
    return request(path, {
      ...options,
      method: "PATCH",
      body: isFormData ? body : body ? JSON.stringify(body) : undefined,
      headers: isFormData
        ? {
            ...options?.headers,
          }
        : {
            "Content-Type": "application/json",
            ...options?.headers,
          },
    });
  };

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
