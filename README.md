
# BBBMsgr - BuiltByBit Bulk Messaging Tool

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
[![Discord](https://img.shields.io/discord/1225531121815781376?color=7289da&label=Discord&logo=discord&logoColor=ffffff)](https://discord.gg/XzDPRNsSYn)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)

BBBMsgr is a powerful tool designed to facilitate bulk messaging for BuiltByBit resource authors. It allows you to send personalized messages to all purchasers of your resource, making it easy to communicate important updates, gather feedback, or provide support.

## Features

- 🚀 Fast and efficient bulk messaging
- 🔒 Secure API authentication (thx bbb)
- 🎨 Colorful console output for easy status tracking
- 🔄 Automatic handling of rate limits (ish)
- 🛡️ Skips suspended and banned users
- ⚙️ Easy configuration via JSON file

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your_username/BBBMsgr.git
    ```
2. Navigate to the project directory:
    ```bash
    cd BBBMsgr
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `config.json` file in the project root with the following structure:

```json
{
    "API_TOKEN": "your_api_token_here",
    "RESOURCE_ID": "your_resource_id_here",
    "MESSAGE_TITLE": "Your Message Title",
    "MESSAGE_CONTENTS": "Your message contents here"
}
```

## Usage

Run the script with:
```bash
python app.py
```
The script will authenticate with the BuiltByBit API, fetch all purchasers of your resource, and send them the configured message.

## Safety Precautions

- Always test the script with a small subset of users before sending bulk messages.
- Be aware of BuiltByBit's terms of service regarding bulk messaging.
- Use this tool responsibly and respect users' preferences.
- As much as I have tried, the rate limit isn't known for BuiltByBit. Watch our for rate limiting. 

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, join our [Discord server](https://discord.gg/XzDPRNsSYn).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the BuiltByBit team for providing the API
- Shoutout to all the awesome resource creators in the BuiltByBit community!

Made with ❤️ by Lofi
