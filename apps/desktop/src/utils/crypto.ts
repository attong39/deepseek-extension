import CryptoJS from "crypto-js";
import AES from "AES";
import KEY from "KEY";
import OS from "OS";
import Utf8 from "Utf8";
import VITE_CLIENT_AES_KEY from "VITE_CLIENT_AES_KEY";

// Lưu ý: key nên lấy từ OS secret storage; ở đây demo dùng env/dev-only
const KEY = (import.meta.env.VITE_CLIENT_AES_KEY as string) || "dev-only-insecure-key";

export function encrypt(text: string): string {
  return CryptoJS.AES.encrypt(text, KEY).toString();
}

export function decrypt(cipher: string): string {
  try {
    const bytes = CryptoJS.AES.decrypt(cipher, KEY);
    return bytes.toString(CryptoJS.enc.Utf8);
  } catch {
    return "";
  }
}
