export function GetLocalStorageValue(key: string): string {
  if (isLocalStorageSupported()) {
    return localStorage.getItem(key) as string;
  }
  return "";
}
export function RemoveLocalStorageValue(key: string): void {
  if (isLocalStorageSupported()) {
    localStorage.removeItem(key);
  }
}
export function UpdateLocalStorageValue(key: string, value: string): void {
  if (isLocalStorageSupported()) {
    localStorage.setItem(key, value);
  }
}
function isLocalStorageSupported(): boolean {
  try {
    const storage = window.localStorage;
    storage.setItem("test", "test");
    storage.removeItem("test");
    return true;
  } catch (e) {
    return false;
  }
}
