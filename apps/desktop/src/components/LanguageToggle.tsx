import LanguageIcon from "@mui/icons-material/Language";
import { IconButton, Tooltip } from "@mui/material";
import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import IPC from "IPC";
import Language from "Language";
import LanguageToggle from "./LanguageToggle";
import Toggle from "Toggle";

export function LanguageToggle() {
  const { i18n } = useTranslation();
  const [lang, setLang] = useState<"vi" | "en">(() => {
    // optimistic initial value; real value will be loaded from settings IPC on mount
    return "vi";
  });

  useEffect(() => {
    i18n.changeLanguage(lang).catch(() => {});
    // persist via IPC if available
    try {
      if ((window as any).zeta?.settings?.setLang) {
        (window as any).zeta.settings.setLang(lang);
      } else if (typeof localStorage !== "undefined") {
        localStorage.setItem("zeta_lang", lang);
      }
    } catch {
      // noop
    }
  }, [lang, i18n]);

  const toggle = useCallback(() => setLang((l: "vi" | "en") => (l === "vi" ? "en" : "vi")), []);
  useEffect(() => {
    // load persisted value from IPC
    let mounted = true;
    (async () => {
      try {
        if ((window as any).zeta?.settings?.getLang) {
          const remote = await (window as any).zeta.settings.getLang();
          if (mounted && (remote === "vi" || remote === "en")) setLang(remote);
        } else if (typeof localStorage !== "undefined") {
          const v = localStorage.getItem("zeta_lang");
          if (mounted && (v === "vi" || v === "en")) setLang(v);
        }
      } catch {}
    })();
    return () => {
      mounted = false;
    };
  }, []);
  return (
    <Tooltip
      title={i18n.t("common.language", {
        lng: lang,
        defaultValue: `Language: ${lang.toUpperCase()}`,
      })}
    >
      <IconButton
        size="small"
        onClick={toggle}
        aria-label={i18n.t("common.language_toggle", {
          defaultValue: "Toggle language",
        })}
      >
        <LanguageIcon fontSize="small" />
      </IconButton>
    </Tooltip>
  );
}
