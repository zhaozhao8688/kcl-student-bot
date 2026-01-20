"""
Quick setup verification script.
Run this before starting the Streamlit app to check configuration.
"""

import sys

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    try:
        import streamlit
        print("✅ Streamlit imported")

        import langgraph
        print("✅ LangGraph imported")

        import openai
        print("✅ OpenAI imported")

        import supabase
        print("✅ Supabase imported")

        import msal
        print("✅ MSAL imported")

        from serpapi import GoogleSearch
        print("✅ SerpAPI imported")

        import icalendar
        print("✅ iCalendar imported")

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_config():
    """Test that configuration loads correctly."""
    print("\nTesting configuration...")
    try:
        from config.settings import settings

        print(f"✅ Config loaded")
        print(f"   - OpenRouter API key: {'*' * 20}{settings.openrouter_api_key[-10:]}")
        print(f"   - Supabase URL: {settings.supabase_url}")
        print(f"   - SerpAPI key: {'*' * 20}{settings.serpapi_api_key[-10:]}")
        print(f"   - Firecrawl key: {'*' * 20}{settings.firecrawl_api_key[-10:]}")
        print(f"   - Default model: {settings.default_model}")

        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False


def test_services():
    """Test that services initialize correctly."""
    print("\nTesting services...")
    try:
        from services.llm_service import llm_service
        print("✅ LLM service initialized")

        from services.supabase_service import supabase_service
        print("✅ Supabase service initialized")

        return True
    except Exception as e:
        print(f"❌ Service error: {e}")
        return False


def test_tools():
    """Test that tools register correctly."""
    print("\nTesting tools...")
    try:
        from tools.tool_registry import tool_registry

        tools = tool_registry.get_all_tools()
        print(f"✅ Tool registry initialized with {len(tools)} tools:")
        for tool in tools:
            auth_required = "🔒" if tool.requires_auth() else "🔓"
            print(f"   {auth_required} {tool.get_name()}: {tool.get_description()}")

        return True
    except Exception as e:
        print(f"❌ Tool error: {e}")
        return False


def test_agent():
    """Test that agent graph compiles."""
    print("\nTesting agent graph...")
    try:
        from agents.graph import agent_graph
        print("✅ Agent graph compiled successfully")

        return True
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("KCL Student Bot - Setup Verification")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Services", test_services),
        ("Tools", test_tools),
        ("Agent Graph", test_agent)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the app.")
        print("\nNext step: Run the following command:")
        print("  streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Common issues:")
        print("  - Missing .env file or incomplete API keys")
        print("  - Python version incompatibility")
        print("  - Missing dependencies")

    return all_passed


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
