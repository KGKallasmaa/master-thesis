export function http(path: string, payload: any) {
  return fetch(getBaseUrl() + path, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function getBaseUrl(){
  return "http://localhost:5000"
}
