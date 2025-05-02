# EnumSlackurls

A simple CLI tool that scans Slack webhook URL and extracts detailed information including:

- **Workspace domain**
- **Workspace ID**
- **Webhook ID**
- **Slack API hostname (hooks.slack.com)**

This tool is designed for security researchers, bug bounty hunters, or developers who want to analyze Slack webhook URLs for potential exposure or misconfiguration.

---

****Important****: You need a Slack OAuth User Token with team:read privs to enumerate a workspace name. 


# Installation & Usage

1. Install the requests pypi library
   
        pip install requests

2. Clone the Tool

        git clone https://github.com/0xRawat/EnumSlackurls.git

# 🧪 Usage
        python3 EnumSlack.py  --token <Token_here> https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

# 🧾 Output
The script will display:

[+] Webhook URL: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

    Domain     : hooks.slack.com    
    Workspace ID : T00000000
    Channel/Service ID : B00000000
    Webhook Token : XXXXXXXXXXXXXXXXXXXXXXXX

# Generate a Slack User OAuth Token

1. Login to any Slack workspace (or create a new one) in the browser and visit https://api.slack.com/apps.
2. Click `Create New App`. Select `From scratch`. Name it and associate it with a workspace.
3. Click `OAuth and Permissions` under `Features`.
4. Under `Scopes` > `User Token Scopes`, add the `team:read` permission.
5. Scroll up. Under `OAuth Tokens` for Your Workspace`, click `Install to Workspace`.
6. Copy your `User OAuth Token`.

Do not misuse Slack webhooks. This tool is intended for educational, auditing, and bug bounty use only.

# Reference
 https://github.com/trufflesecurity/WhoAmISlack

# 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.
