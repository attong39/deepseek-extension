// Test sample file để AI Agent optimize

export class TestClass {
  private data: string;
  
  constructor() {
    this.data = "test";
  }
  
  // Method without documentation
  public processData(input: string): string {
    if (input == null) { // should use ===
      return "";
    }
    
    // Unused variable
    let unusedVar = "not used";
    
    return input.toUpperCase();
  }
  
  // Method with potential optimization
  public findItems(items: string[], target: string): boolean {
    for (let i = 0; i < items.length; i++) {
      if (items[i] === target) {
        return true;
      }
    }
    return false;
  }
}
