import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { SnackbarProvider } from "notistack";
import { PropsWithChildren, useMemo } from "react";

import "../i18n";
import { PermissionProvider } from "./PermissionProvider";
import AppProviders from "./AppProviders";
import MuiAutocomplete from "MuiAutocomplete";
import MuiButton from "MuiButton";
import MuiCheckbox from "MuiCheckbox";
import MuiFormControl from "MuiFormControl";
import MuiRadio from "MuiRadio";
import MuiSelect from "MuiSelect";
import MuiSwitch from "MuiSwitch";
import MuiTextField from "MuiTextField";

export function AppProviders({ children }: PropsWithChildren) {
  const queryClient = useMemo(() => new QueryClient(), []);
  const theme = useMemo(
    () =>
      createTheme({
        palette: { mode: "light" },
        components: {
          MuiTextField: { defaultProps: { size: "small" } },
          MuiSelect: { defaultProps: { size: "small" } },
          MuiButton: { defaultProps: { size: "small", variant: "contained" } },
          MuiFormControl: { defaultProps: { size: "small" } },
          MuiAutocomplete: { defaultProps: { size: "small" } },
          MuiCheckbox: { defaultProps: { size: "small" } },
          MuiRadio: { defaultProps: { size: "small" } },
          MuiSwitch: { defaultProps: { size: "small" } },
        },
      }),
    [],
  );
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <SnackbarProvider
          maxSnack={3}
          autoHideDuration={3500}
          anchorOrigin={{ vertical: "top", horizontal: "right" }}
        >
          <PermissionProvider>{children}</PermissionProvider>
        </SnackbarProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
