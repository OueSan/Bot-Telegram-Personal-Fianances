```markdown
# Telegram Chatbot for Google Sheets

## Overview

This Telegram chatbot is designed to interact with users on the Telegram platform and update a Google Sheet on Google Cloud. It serves as a simple financial tracker, allowing users to record inflows, outflows, and transfers.

## Features

- **Inflows Registration:** Users can register different types of inflows, including salary, freelance income, investment interest, and others.

- **Outflows Registration:** Users can register different types of outflows, including fixed, variable, and single expenses.

- **Transfers:** Users can initiate transfers between different accounts.

- **Reports:** Users can view summarized reports of total entries, total outs, and total transfers.

## Getting Started

### Prerequisites

- Python 3.x
- [Telegram Bot Token](https://core.telegram.org/bots#botfather)
- [Google Cloud Project](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
- [Google Sheets API Credentials](https://developers.google.com/sheets/api/quickstart)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OueSan/ChatBot-Telegram-Personal-Fianances.git

   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your credentials:
   - Copy your Telegram Bot Token to `personal_token.py` as `private_token`.
   - Download Google Sheets API credentials and save them as `credentials.json`.

4. Run the bot:

   ```bash
   python main.py
   ```

## Usage

1. Start the bot by sending `/start` in the Telegram chat.

2. Choose an option from the provided keyboard (Inflows, Outflows, Transfers, Reports).

3. Follow the bot's instructions to register entries, exits, or transfers.

4. View summarized reports by selecting the 'Reports' option.

## Contributing

Contributions are welcome! If you find a bug or have an enhancement in mind, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
