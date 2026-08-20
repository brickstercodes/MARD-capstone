#!/usr/bin/env python3
"""
Minimal test: verify Vertex AI authentication with GeminiClient.
Tests the patched GeminiClient with service-account JSON from .env.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Verify env vars are set
project = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
cred_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

if not project:
    print("ERROR: GOOGLE_CLOUD_PROJECT not set in .env")
    sys.exit(1)
if not cred_json:
    print("ERROR: GOOGLE_APPLICATION_CREDENTIALS_JSON not set in .env")
    sys.exit(1)

print(f"✓ GOOGLE_CLOUD_PROJECT={project}")
print(f"✓ GOOGLE_CLOUD_LOCATION={location or 'us-central1 (default)'}")
print(f"✓ GOOGLE_APPLICATION_CREDENTIALS_JSON={len(cred_json)} bytes")

# Import and test GeminiClient
try:
    from rlm.clients.gemini import GeminiClient
    print("✓ GeminiClient imported")
except ImportError as e:
    print(f"ERROR: Failed to import GeminiClient: {e}")
    sys.exit(1)

# Instantiate with Vertex backend
try:
    client = GeminiClient(
        model_name="gemini-3.6-flash",
        use_vertex=True,
        project=project,
        location="global",
    )
    print(f"✓ GeminiClient instantiated for Vertex (model={client.model_name}, use_vertex={client.use_vertex})")
except Exception as e:
    print(f"ERROR: Failed to instantiate GeminiClient: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Make a simple completion to test auth
try:
    prompt = "Say 'Vertex authentication successful' and stop."
    response = client.completion(prompt)
    print(f"✓ Completion call succeeded")
    print(f"  Response: {response[:100]}")

    usage = client.get_last_usage()
    print(f"✓ Token usage: {usage.total_input_tokens} input, {usage.total_output_tokens} output")
except Exception as e:
    print(f"ERROR: Completion call failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All Vertex authentication checks passed!")
