# neodb-get-access-token

A utility script to help you obtain an access token for the NeoDB API through OAuth2 PKCE authentication flow.

## What This Script Does

1. Initiates OAuth2 PKCE (Proof Key for Code Exchange) flow to securely obtain a NeoDB API access token
2. Opens your default browser to complete the authentication process
3. Returns the access token that can be used with NeoDB's API

## Setup

1. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies using uv:
```bash
uv pip install .
```

## How to Run

```bash
python main.py
```

## Customization

You can modify both the base URL and redirect URL according to your needs:

- **Base URL**: Can be changed to:
  - `https://neodb.social` (default NeoDB instance)
  - Your self-hosted NeoDB instance URL
  
- **Redirect URL**: Can be any URL that:
  - You've configured in your NeoDB application settings
  - Is accessible on your system (e.g., `http://localhost:8000`)

### How to Run

```bash
python main.py <BASE_URL> <REDIRECT_URL>
```

For example:
```bash
python main.py https://neodb.social http://localhost:8000
```

Make sure the redirect URL matches what you've configured in your NeoDB application settings.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 