import g4f
import asyncio
import time
from datetime import datetime
import json

class G4FProviderTester:
    def __init__(self):
        self.results = {
            "text_providers": {},
            "image_providers": {},
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_message = "Hello, can you respond to this simple test message?"
        self.test_image_prompt = "A beautiful sunset over mountains"
        
    def get_all_providers(self):
        """Get all available providers from g4f"""
        # Get all provider classes from g4f.Provider
        all_providers = []
        for attr_name in dir(g4f.Provider):
            attr = getattr(g4f.Provider, attr_name)
            # Check if it's a provider class (has working attribute)
            if hasattr(attr, 'working') and not attr_name.startswith('__'):
                all_providers.append(attr)
        return all_providers
    
    def test_text_provider(self, provider):
        """Test a single text provider"""
        provider_name = provider.__name__
        print(f"Testing text provider: {provider_name}")
        
        start_time = time.time()
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": self.test_message}],
                provider=provider,
                timeout=30  # Shorter timeout for testing
            )
            elapsed_time = time.time() - start_time
            
            # Check if response is valid
            if response and isinstance(response, str) and len(response) > 5:
                return {
                    "status": "working",
                    "response_time": round(elapsed_time, 2),
                    "sample": response[:100] + "..." if len(response) > 100 else response
                }
            else:
                return {
                    "status": "invalid_response",
                    "response_time": round(elapsed_time, 2),
                    "error": "Empty or invalid response"
                }
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "status": "error",
                "response_time": round(elapsed_time, 2),
                "error": str(e)
            }
    
    def test_image_provider(self, provider):
        """Test a single image provider"""
        provider_name = provider.__name__
        print(f"Testing image provider: {provider_name}")
        
        start_time = time.time()
        try:
            response = g4f.ChatCompletion.create(
                model="image-model",
                messages=[{"role": "user", "content": self.test_image_prompt}],
                provider=provider,
                timeout=60  # Images may take longer
            )
            elapsed_time = time.time() - start_time
            
            # For image providers, we expect a URL or base64 image data
            from social_network.app.utils import extract_image_url
            image_url = extract_image_url(response)
            
            if image_url:
                return {
                    "status": "working",
                    "response_time": round(elapsed_time, 2),
                    "image_url": image_url
                }
            else:
                return {
                    "status": "invalid_response",
                    "response_time": round(elapsed_time, 2),
                    "error": "Could not extract image URL",
                    "raw_response": response[:200] if response else None
                }
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            return {
                "status": "error",
                "response_time": round(elapsed_time, 2),
                "error": str(e)
            }
    
    def run_tests(self):
        """Run tests on all providers"""
        providers = self.get_all_providers()
        
        # Test each provider
        for provider in providers:
            provider_name = provider.__name__
            
            # Skip abstract base classes or non-working providers
            if not hasattr(provider, 'working') or provider_name == 'BaseProvider':
                continue
                
            # Check if it's an image provider
            is_image_provider = False
            for attr_name in dir(provider):
                if attr_name == 'supports_image_generation' and getattr(provider, attr_name):
                    is_image_provider = True
                    break
            
            # Test the provider
            if is_image_provider:
                result = self.test_image_provider(provider)
                self.results["image_providers"][provider_name] = result
            else:
                result = self.test_text_provider(provider)
                self.results["text_providers"][provider_name] = result
        
        return self.results
    
    def save_results(self, filename="g4f_provider_test_results.json"):
        """Save test results to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {filename}")
        
    def print_summary(self):
        """Print a summary of the test results"""
        working_text = sum(1 for p, r in self.results["text_providers"].items() if r["status"] == "working")
        total_text = len(self.results["text_providers"])
        
        working_image = sum(1 for p, r in self.results["image_providers"].items() if r["status"] == "working")
        total_image = len(self.results["image_providers"])
        
        print("\n===== G4F PROVIDER TEST SUMMARY =====")
        print(f"Text Providers: {working_text}/{total_text} working")
        print(f"Image Providers: {working_image}/{total_image} working")
        print("=====================================\n")
        
        print("Working Text Providers:")
        for provider, result in self.results["text_providers"].items():
            if result["status"] == "working":
                print(f"  - {provider} ({result['response_time']}s)")
        
        print("\nWorking Image Providers:")
        for provider, result in self.results["image_providers"].items():
            if result["status"] == "working":
                print(f"  - {provider} ({result['response_time']}s)")


def main():
    """Main function to run the tests"""
    print("Starting G4F provider tests...")
    tester = G4FProviderTester()
    tester.run_tests()
    tester.print_summary()
    tester.save_results()
    print("Tests completed!")


if __name__ == "__main__":
    main()
