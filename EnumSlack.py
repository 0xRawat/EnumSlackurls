#!/usr/bin/env python3
"""
Script to retrieve Slack workspace (team) information using a Slack incoming webhook URL and Slack API.
It extracts the team ID from the webhook URL, then calls the Slack API (team.info) with a provided token
to get the workspace (team) name, domain, and ID.
Token can be provided via an environment variable (SLACK_TOKEN) or a command-line option.
"""

from __future__ import print_function
import os
import sys
import argparse

# Try to import requests library, exit with error if not available
try:
    import requests
except ImportError:
    print("Error: The 'requests' library is required. Install it with 'pip install requests'.", file=sys.stderr)
    sys.exit(1)

# URL parsing compatibility for Python 2 and 3
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def parse_webhook_url(webhook_url):
    """
    Validate the Slack webhook URL and extract the Team ID.
    Slack webhook URLs are of the form: https://hooks.slack.com/services/T{TEAM_ID}/B{...}/...
    """
    try:
        parsed = urlparse(webhook_url)
    except Exception as e:
        raise ValueError("Invalid URL format") from e

    # Basic checks for Slack webhook URL
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must start with http:// or https://")
    host = parsed.netloc.lower()
    if not host.endswith("hooks.slack.com"):
        raise ValueError("URL does not appear to be a valid Slack webhook URL (domain mismatch)")
    path_parts = parsed.path.split('/')
    # path_parts example: ['', 'services', 'T12345678', 'B12345678', 'abcd1234']
    if len(path_parts) < 3 or path_parts[1] != "services" or not path_parts[2].startswith("T"):
        raise ValueError("URL does not have the expected Slack webhook format")
    team_id = path_parts[2]
    # Additional basic validation of team_id
    if len(team_id) < 2 or not team_id[1:].isalnum():
        raise ValueError("Extracted team ID '{}' seems invalid".format(team_id))
    return team_id

def get_team_info(token, team_id):
    """
    Calls Slack API 'team.info' with the given token and team_id to retrieve workspace information.
    """
    api_url = "https://slack.com/api/team.info"
    payload = {
        'token': token,
        'team': team_id
    }
    try:
        response = requests.post(api_url, data=payload, timeout=10)
    except requests.RequestException as e:
        raise RuntimeError("Failed to connect to Slack API: {}".format(e))
    if not response.ok:
        raise RuntimeError("Slack API request failed with status code {}".format(response.status_code))
    try:
        data = response.json()
    except ValueError:
        raise RuntimeError("Invalid response from Slack API (not valid JSON)")
    if not data.get('ok', False):
        error_msg = data.get('error', 'unknown_error')
        raise RuntimeError("Slack API returned an error: {}".format(error_msg))
    team_info = data.get('team')
    if not isinstance(team_info, dict):
        raise RuntimeError("Unexpected Slack API response structure")
    return team_info

def main():
    parser = argparse.ArgumentParser(description="Retrieve Slack workspace information using a webhook URL.")
    parser.add_argument('webhook_url', help='Slack incoming webhook URL (to extract team ID)')
    parser.add_argument('-t', '--token', help='Slack API token (can also be set via SLACK_TOKEN environment variable)')
    args = parser.parse_args()

    token = args.token or os.environ.get('SLACK_TOKEN')
    if not token:
        print("Error: Slack API token not provided. Use --token option or set the SLACK_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)

    webhook_url = args.webhook_url.strip()
    if not webhook_url:
        print("Error: Webhook URL is empty.", file=sys.stderr)
        sys.exit(1)

    try:
        team_id = parse_webhook_url(webhook_url)
    except ValueError as e:
        print("Error parsing webhook URL: {}".format(e), file=sys.stderr)
        sys.exit(1)

    try:
        team_info = get_team_info(token, team_id)
    except RuntimeError as e:
        print("Error retrieving team info: {}".format(e), file=sys.stderr)
        sys.exit(1)

    # Extract relevant fields from team_info
    name = team_info.get('name', '<no name>')
    domain = team_info.get('domain', '<no domain>')
    tid = team_info.get('id', '<no id>')
    # Print workspace information
    print("Workspace Name: {}".format(name))
    print("Workspace Domain: {}".format(domain))
    print("Workspace ID: {}".format(tid))

if __name__ == "__main__":
    main()
