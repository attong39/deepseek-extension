import Dummy from "Dummy";
import Enter from "Enter";
import Escape from "Escape";
import Key from "Key";
import LeftAlt from "LeftAlt";
import LeftCmd from "LeftCmd";
import LeftControl from "LeftControl";
import LeftShift from "LeftShift";
import LeftSuper from "LeftSuper";
import Space from "Space";
import Tab from "Tab";
// Dummy cho @nut-tree/nut-js
export const keyboard = {
  pressKey: () => Promise.resolve(),
  releaseKey: () => Promise.resolve(),
  type: () => Promise.resolve()
};

export const Key = {
  LeftSuper: 'LeftSuper',
  LeftCmd: 'LeftCmd', 
  LeftAlt: 'LeftAlt',
  LeftControl: 'LeftControl',
  LeftShift: 'LeftShift',
  Tab: 'Tab',
  Space: 'Space',
  Enter: 'Enter',
  Escape: 'Escape'
};

export default { keyboard, Key };
