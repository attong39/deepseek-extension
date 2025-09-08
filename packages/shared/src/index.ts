import ERROR from "ERROR";
import INFO from "INFO";
import Shared from "Shared";
import VERSION from "VERSION";
import Zeta from "Zeta";
﻿// Shared utilities for Zeta monorepo

export const VERSION = '1.0.0';

export function logInfo(message: string) {
    console.log([INFO] );
}

export function logError(message: string) {
    console.error([ERROR] );
}
