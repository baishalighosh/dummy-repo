# Perplexity Model Monitor Workflow

## Overview

This workflow monitors Perplexity AI models for changes and automatically notifies when models are added, removed, or modified.

## How It Works

### Background

Perplexity AI does not provide a `/v1/models` API endpoint like OpenAI. Instead, they maintain their model documentation at https://docs.perplexity.ai/docs/model-cards. This workflow works by:

1. Maintaining a known list of Perplexity models in `check_perplexity_models.py`
2. Comparing the current list with the previously stored version
3. Detecting additions, removals, or modifications
4. Creating notifications when changes are detected

### Components

#### Workflow File: `perplexity-model-monitor.yml`

- **Schedule**: Runs daily at 9 AM UTC
- **Manual Trigger**: Can be triggered manually via workflow_dispatch
- **Permissions**: Requires `contents: write` and `issues: write`

#### Python Script: `check_perplexity_models.py`

Located at `.github/scripts/check_perplexity_models.py`, this script:

- Maintains a list of known Perplexity models
- Stores the current model list in `perplexity_models.json`
- Compares with previous versions to detect changes
- Generates a human-readable summary of changes

## Current Perplexity Models

As of the last update, Perplexity provides these model families:

### Search Models
- **sonar**: Lightweight, grounded search (based on Llama 3.3 70B)
- **sonar-pro**: Deeper retrieval with follow-ups

### Reasoning Models
- **sonar-reasoning**: Real-time reasoning with search
- **sonar-reasoning-pro**: Advanced reasoning (powered by DeepSeek-R1)

### Research Models
- **sonar-deep-research**: Long-form, source-dense reports

### Deprecated Models
- `llama-3.1-sonar-*-128k-online` series
- `pplx-*` series

## Notifications

When changes are detected, the workflow:

1. **Commits Changes**: Updates `perplexity_models.json` with the new model list
2. **Creates GitHub Issue**: Opens an issue with details of the changes
3. **Sends Slack Notification** (optional): If `SLACK_WEBHOOK_URL` is configured

## Setup

### Required Permissions

Ensure the workflow has these permissions:
- `contents: write` - To commit model list updates
- `issues: write` - To create notification issues

### Optional: Slack Notifications

To enable Slack notifications:

1. Create a Slack webhook URL
2. Add it as a repository variable named `SLACK_WEBHOOK_URL`
3. Go to: Settings → Secrets and variables → Actions → Variables

## Manual Execution

To manually trigger the workflow:

1. Go to Actions tab
2. Select "Perplexity Model Monitor"
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Updating the Model List

To update the known model list when Perplexity releases new models:

1. Edit `.github/scripts/check_perplexity_models.py`
2. Update the `KNOWN_MODELS` dictionary with new model information
3. Source: https://docs.perplexity.ai/docs/model-cards
4. Commit and push the changes

## Troubleshooting

### Workflow Not Creating Issues

Check that:
- The workflow has `issues: write` permission
- The repository allows issue creation
- The workflow is enabled in the Actions tab

### False Positives

If you're getting notifications for models that haven't changed:
- Check the `KNOWN_MODELS` dictionary in the Python script
- Ensure model definitions match the current Perplexity documentation

## References

- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Perplexity Model Cards](https://docs.perplexity.ai/docs/model-cards)
- [Perplexity API Platform](https://www.perplexity.ai/api-platform)
