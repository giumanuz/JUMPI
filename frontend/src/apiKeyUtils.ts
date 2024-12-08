import axiosInstance from "./axiosInstance";

export function isApiKeySet(): boolean {
  return localStorage.getItem("apiKey") !== "";
}

export function setApiKey(key: string): void {
  localStorage.setItem("apiKey", key);
  axiosInstance.defaults.headers.common["X-API-KEY"] = key;
}

export function reloadApiKey(): void {
  const storedApiKey = localStorage.getItem("apiKey");
  if (storedApiKey) {
    axiosInstance.defaults.headers.common["X-API-KEY"] = storedApiKey;
  }
}

export async function validateApiKey(key: string): Promise<boolean> {
  try {
    await axiosInstance.get("/validate-api-key", {
      headers: { "X-API-KEY": key },
    });
    return true;
  } catch {
    return false;
  }
}
