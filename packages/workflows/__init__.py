"""
Workflows package for the Clinical HCC Extractor.
"""

# Import here to avoid circular imports
from packages.workflows.hcc_extractor.v0 import run_hcc_extractor_v0

# Alias the latest process to point to the most recent version
hcc_extractor_latest = run_hcc_extractor_v0

hcc_extractor = {
    "v0": run_hcc_extractor_v0,
    "latest": "v0",  # Remember to update when adding new versions
}
hcc_extractor["available_versions"] = list(filter(lambda k: k != "latest", hcc_extractor.keys()))

# Export everything
__all__ = [
    "hcc_extractor",
    "run_hcc_extractor_v0",
    "hcc_extractor_latest",
]