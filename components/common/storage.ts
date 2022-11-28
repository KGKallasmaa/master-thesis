import {
  GetLocalStorageValue,
  RemoveLocalStorageValue,
  UpdateLocalStorageValue,
} from "./local";

export function getId(): string {
  const key = "id";
  const currentValue = GetLocalStorageValue(key);
  if (currentValue) {
    return currentValue;
  }
  const token: string = objectId();
  UpdateLocalStorageValue(key, token);
  return token;
}
export function removeId() {
  RemoveLocalStorageValue("id");
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
