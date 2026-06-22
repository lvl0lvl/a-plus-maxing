"""The single model boundary — every model-touching call routes through this package.

`scripts.model` is the system's one programmatic model boundary: the swappable no-train
model client (`client.ModelClient`) and the runtime key source (`key_source.resolve`). A
model-client import (`anthropic`/`openai`/`httpx`/`requests`) appears ONLY inside this
package (the default backend); the repo carries no API-key literal — the key is resolved
at runtime from an env var or the macOS keychain.
"""
