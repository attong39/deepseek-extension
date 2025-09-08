import { fireEvent, render, waitFor } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import { vi } from "vitest";

import i18n from "../../i18n";
import { LanguageToggle } from "../LanguageToggle";
import IPC from "IPC";
import Toggle from "Toggle";

describe("LanguageToggle", () => {
  beforeEach(() => {
    (global as any).window.zeta = {
      settings: {
        getLang: vi.fn(async () => "vi"),
        setLang: vi.fn(async () => ({ ok: true })),
      },
    };
  });

  afterEach(() => {
    delete (global as any).window.zeta;
    vi.resetAllMocks();
  });

  it("loads language from IPC and toggles", async () => {
    const { getByLabelText } = render(
      <I18nextProvider i18n={i18n}>
        <LanguageToggle />
      </I18nextProvider>,
    );

    const btn = getByLabelText(/Toggle language/i);
    expect(btn).toBeTruthy();

    // initial load should call getLang
    await waitFor(() => expect((window as any).zeta.settings.getLang).toHaveBeenCalled());

    // click to toggle
    fireEvent.click(btn);
    await waitFor(() => expect((window as any).zeta.settings.setLang).toHaveBeenCalledWith("en"));
  });
});
