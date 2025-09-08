import Permission from "Permission";
export type Permission = "screen" | "clipboard" | "automation" | "overlay";

export function isGranted(_p: Permission): boolean { 
  return true; 
}

export async function ensure(_p: Permission): Promise<boolean> { 
  return true; 
}

export function explain(_p: Permission): string { 
  return "granted"; 
}

export function hasPermission(_p: Permission): boolean {
  return true;
}
