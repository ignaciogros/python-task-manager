"""Pytest root configuration."""
import sys
from unittest.mock import MagicMock

# Inject a mock openai module when the real package is not yet installed,
# so provider tests can import and patch client classes without real API access.
if "openai" not in sys.modules:
    sys.modules["openai"] = MagicMock()
