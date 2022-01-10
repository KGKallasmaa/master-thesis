import {
  GetSessionStorageValue,
  RemoveSessionStorageValue,
  UpdateSessionStorageValue,
} from "./session";

export function getId(): string {
  const key = "id";
  const currentValue = GetSessionStorageValue(key);
  if (currentValue) {
    return currentValue;
  }
  const token: string = objectId();
  UpdateSessionStorageValue(key, token);
  return token;
}
export function removeId() {
  RemoveSessionStorageValue("id");
}

function objectId() {
  const timestamp = ((new Date().getTime() / 1000) | 0).toString(16);
  return (
    timestamp +
    "xxxxxxxxxxxxxxxx"
      .replace(/[x]/g, function () {
        return ((Math.random() * 16) | 0).toString(16);
      })
      .toLowerCase()
  );
}
