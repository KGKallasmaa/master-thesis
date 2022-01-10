export function GetSessionStorageValue(key: string): string {
  if (isSessionStorageSupported()) {
    return sessionStorage.getItem(key) as string;
  }
  return "";
}
export function RemoveSessionStorageValue(key: string): void {
  if (isSessionStorageSupported()) {
    sessionStorage.removeItem(key);
  }
}
export function UpdateSessionStorageValue(key: string, value: string): void {
  if (isSessionStorageSupported()) {
    sessionStorage.setItem(key, value);
  }
}
function isSessionStorageSupported(): boolean {
  try {
    const storage = window.sessionStorage;
    storage.setItem("test", "test");
    storage.removeItem("test");
    return true;
  } catch (e) {
    return false;
  }
}
