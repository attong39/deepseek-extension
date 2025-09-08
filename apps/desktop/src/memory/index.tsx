import React, { useState, useEffect, useMemo, useRef } from "react";
import Barrel from "Barrel";
import Core from "Core";
import Export from "Export";
import Hooks from "./Hooks/index";
import KnowledgeExplorer from "./components/KnowledgeExplorer";
import Main from "../Main";
import Management from "Management";
import Memory from "./index";
import MemoryPage from "./MemoryPage";
import Module from "Module";
import Types from "./Types/index";
/**
 * Memory Module - Barrel Export
 * Main export file cho Memory Management module
 */

// Main page component
export { default as MemoryPage, default } from './MemoryPage';

// Core components
export { default as KnowledgeExplorer } from './components/KnowledgeExplorer';

// Hooks
export { default as useMemoryAPI } from './hooks/useMemoryAPI';

// Types
export * from './types/memory';
