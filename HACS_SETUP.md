# HACS Setup Guide

This integration is compatible with HACS (Home Assistant Community Store). Follow these steps to make it available via HACS.

## Prerequisites

1. **GitHub Account**: You need a GitHub account
2. **Public Repository**: The integration must be in a public GitHub repository
3. **HACS Installed**: Users need HACS installed in their Home Assistant instance

## Setup Steps

### 1. Create GitHub Repository

1. Create a new public repository on GitHub (e.g., `indra-v2h-home-assistant`)
2. Push this code to the repository
3. Ensure the repository structure is:
   ```
   your-repo/
   ├── custom_components/
   │   └── indra_v2h/
   │       ├── __init__.py
   │       ├── manifest.json
   │       └── ... (all integration files)
   ├── hacs.json
   ├── README.md
   └── .github/
       └── workflows/
           ├── hacs.yml
           └── hassfest.yml
   ```

### 2. Update Repository URLs

Update these files with your actual GitHub repository URL:

**`custom_components/indra_v2h/manifest.json`:**
```json
{
  "documentation": "https://github.com/YOUR_USERNAME/YOUR_REPO"
}
```

**`custom_components/indra_v2h/manifest.json` - codeowners:**
```json
{
  "codeowners": ["@YOUR_GITHUB_USERNAME"]
}
```

### 3. Create GitHub Release

1. Go to your GitHub repository
2. Click **Releases** > **Create a new release**
3. Create a tag (e.g., `v1.0.0`)
4. Add release title and description
5. Click **Publish release**

**Important**: HACS requires a full GitHub release (not just a tag) to install the integration.

### 4. Verify HACS Validation

The GitHub Actions workflows will automatically validate your integration:

- **HACS Validation**: Checks HACS compatibility
- **Hassfest Validation**: Validates Home Assistant integration requirements

Check the **Actions** tab in your GitHub repository to ensure both workflows pass.

### 5. Test HACS Installation

**As a user (for testing):**

1. In Home Assistant, go to HACS
2. Click the three dots (⋮) > **Custom repositories**
3. Add your repository:
   - Repository: `https://github.com/YOUR_USERNAME/YOUR_REPO`
   - Category: **Integration**
4. Search for "Indra V2H" in HACS
5. Install and test

## HACS File Structure

### `hacs.json` (Root)

This file tells HACS about your integration:

```json
{
  "name": "Indra V2H",
  "domains": ["indra_v2h"],
  "iot_class": "Cloud Polling",
  "homeassistant": "2024.1.0"
}
```

### GitHub Workflows

**`.github/workflows/hacs.yml`**: Validates HACS compatibility
**`.github/workflows/hassfest.yml`**: Validates Home Assistant requirements

## Publishing to HACS Default Repository

To make your integration available in HACS by default (without users adding a custom repository):

1. Ensure your integration meets all HACS requirements
2. Submit it to the HACS default repository
3. Follow HACS submission guidelines: https://hacs.xyz/docs/publish/include/

## Updating the Integration

When you update the integration:

1. Make your changes
2. Update the version in `manifest.json`
3. Create a new GitHub release with the new version
4. HACS will notify users of the update

## Troubleshooting

### Integration Not Appearing in HACS

- Verify the repository is public
- Check that `hacs.json` exists in the root
- Ensure a GitHub release exists (not just a tag)
- Verify the repository structure is correct
- Check GitHub Actions for validation errors

### HACS Validation Failing

- Check the Actions tab for specific errors
- Ensure `manifest.json` is valid
- Verify all required files are present
- Check that the integration follows Home Assistant patterns

### Users Can't Install

- Verify the repository is public
- Check that a release exists (not just a tag)
- Ensure the `custom_components/indra_v2h/` structure is correct
- Verify `hacs.json` is in the repository root

## Notes

- HACS will automatically check for updates based on releases
- Users can install via HACS or manually
- The integration will appear in HACS after adding as a custom repository
- For default HACS inclusion, follow the official submission process

