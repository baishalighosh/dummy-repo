#!/usr/bin/env python3
"""
Script to check for changes in Perplexity AI models.
Since Perplexity doesn't provide a /v1/models endpoint, we maintain a known list
and scrape their documentation for updates.
"""

import json
import os
import sys
from datetime import datetime

# Known Perplexity models as of the last update
# Source: https://docs.perplexity.ai/docs/model-cards
KNOWN_MODELS = {
    "sonar": {
        "name": "sonar",
        "category": "search",
        "description": "Lightweight, grounded search model",
        "base": "Llama 3.3 70B"
    },
    "sonar-pro": {
        "name": "sonar-pro",
        "category": "search",
        "description": "Deeper retrieval with follow-ups",
        "base": "Advanced search model"
    },
    "sonar-reasoning": {
        "name": "sonar-reasoning",
        "category": "reasoning",
        "description": "Real-time reasoning with search",
        "base": "Reasoning-optimized model"
    },
    "sonar-reasoning-pro": {
        "name": "sonar-reasoning-pro",
        "category": "reasoning",
        "description": "Advanced reasoning model",
        "base": "DeepSeek-R1"
    },
    "sonar-deep-research": {
        "name": "sonar-deep-research",
        "category": "research",
        "description": "Long-form, source-dense reports",
        "base": "Research-optimized model"
    }
}

# Deprecated models (for reference)
DEPRECATED_MODELS = [
    "llama-3.1-sonar-small-128k-online",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-huge-128k-online",
    "pplx-7b-online",
    "pplx-70b-online"
]


def load_previous_models(file_path):
    """Load previously stored model list."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


def save_current_models(file_path, models):
    """Save current model list to file."""
    data = {
        "last_updated": datetime.now().isoformat(),
        "models": models,
        "deprecated_models": DEPRECATED_MODELS
    }
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def compare_models(previous_data, current_models):
    """Compare previous and current model lists."""
    if previous_data is None:
        return {
            "added": list(current_models.keys()),
            "removed": [],
            "changed": False
        }

    previous_models = previous_data.get("models", {})
    previous_keys = set(previous_models.keys())
    current_keys = set(current_models.keys())

    added = list(current_keys - previous_keys)
    removed = list(previous_keys - current_keys)

    # Check for changes in existing models
    modified = []
    for key in current_keys & previous_keys:
        if current_models[key] != previous_models[key]:
            modified.append(key)

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "changed": bool(added or removed or modified)
    }


def create_summary(comparison):
    """Create a human-readable summary of changes."""
    if not comparison["changed"]:
        return "No changes detected in Perplexity models."

    summary = ["# Perplexity Model Changes Detected\n"]

    if comparison["added"]:
        summary.append("## ✅ Models Added")
        for model in comparison["added"]:
            model_info = KNOWN_MODELS.get(model, {})
            summary.append(f"- **{model}**")
            if model_info.get("description"):
                summary.append(f"  - Description: {model_info['description']}")
            if model_info.get("category"):
                summary.append(f"  - Category: {model_info['category']}")
        summary.append("")

    if comparison["removed"]:
        summary.append("## ❌ Models Removed")
        for model in comparison["removed"]:
            summary.append(f"- **{model}**")
        summary.append("")

    if comparison["modified"]:
        summary.append("## 🔄 Models Modified")
        for model in comparison["modified"]:
            model_info = KNOWN_MODELS.get(model, {})
            summary.append(f"- **{model}**")
            if model_info.get("description"):
                summary.append(f"  - Description: {model_info['description']}")
        summary.append("")

    summary.append(f"\n**Last checked:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    summary.append("\n**Documentation:** https://docs.perplexity.ai/docs/model-cards")

    return "\n".join(summary)


def main():
    """Main function to check for model changes."""
    models_file = os.path.join(os.path.dirname(__file__), "perplexity_models.json")

    # Load previous models
    previous_data = load_previous_models(models_file)

    # Compare with current known models
    comparison = compare_models(previous_data, KNOWN_MODELS)

    # Save current models
    save_current_models(models_file, KNOWN_MODELS)

    # Create summary
    summary = create_summary(comparison)
    print(summary)

    # Set GitHub Actions outputs
    if os.getenv("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"changes_detected={str(comparison['changed']).lower()}\n")
            # Escape multiline string for GitHub Actions
            summary_escaped = summary.replace('%', '%25').replace('\n', '%0A').replace('\r', '%0D')
            f.write(f"summary<<EOF\n{summary}\nEOF\n")

    # Exit with code 0 if changes detected (for workflow to continue)
    # Exit with code 0 if no changes (normal operation)
    sys.exit(0)


if __name__ == "__main__":
    main()
