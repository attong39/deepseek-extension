import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./en.json";
import vi from "./vi.json";

// Khởi tạo i18n cho runtime chuyển đổi ngôn ngữ
void i18n.use(initReactI18next).init({
  resources: {
    vi: { translation: vi },
    en: { translation: en },
  },
  lng: (localStorage.getItem("zeta_lang") as "vi" | "en") || "vi",
  fallbackLng: "vi",
  interpolation: { escapeValue: false },
});

export default i18n;
