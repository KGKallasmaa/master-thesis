export function http(url: string, payload: any) {
  const baseUrl = "http://157.245.16.208:5000";
  return fetch(baseUrl + url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
