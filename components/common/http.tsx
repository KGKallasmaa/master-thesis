export function http(url: string, payload: any) {
  const baseUrl = "https://164.92.248.201:5000";
  return fetch(baseUrl + url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
