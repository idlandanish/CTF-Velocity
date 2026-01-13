from src.core.classifier import Classifier

def test():
    c = Classifier()
    
    print("--- Testing Text Inputs ---")
    print(f"URL: {c.identify('http://example.com/login')} (Expected: web)")
    print(f"B64: {c.identify('ZuwbhdMNQDddJEi4DI/w8A==')} (Expected: crypto)")
    
    print("\n--- Testing File Inputs ---")
    # Create a dummy file to test
    with open("test.txt", "w") as f: f.write("Hello World")
    print(f"File: {c.identify('test.txt')} (Expected: crypto/misc)")

if __name__ == "__main__":
    test()