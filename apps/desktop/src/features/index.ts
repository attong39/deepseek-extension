import Architecture from "Architecture";
import Chat from "../pages/Chat";
import ChatInterface from "ChatInterface";
import Clean from "Clean";
import Dashboard from "./Dashboard/index";
import Features from "./index";
import Memory from "../Memory/index";
import MemoryBrowser from "MemoryBrowser";
import Module from "Module";
import OneClickDropzone from "OneClickDropzone";
import Settings from "../pages/Settings";
import SettingsPanel from "SettingsPanel";
import Training from "./Training/index";
/**
 * Features barrel file
 * Module-hoá tất cả features theo Clean Architecture
 */

// Dashboard feature
export { Dashboard } from "./dashboard";

// Training feature 
export { OneClickDropzone } from "./training";

// Chat feature (nếu có)
// export { ChatInterface } from "./chat";

// Memory feature (nếu có)  
// export { MemoryBrowser } from "./memory";

// Settings feature (nếu có)
// export { SettingsPanel } from "./settings";
