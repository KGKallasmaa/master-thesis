export function http(path: string, payload: any) {
  return fetch(SERVER_URL + path, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export const SERVER_URL = "http://localhost:8000"
