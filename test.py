from config.settings import Config
print(f"API Key loaded: {bool(Config.ANTHROPIC_API_KEY)}")
print("✅ Setup complete!")