# ChatGPT Teamspeak Bot
This is a simple ChatGPT Bot for TeamSpeak that will wait for messages in a specified
channel, send them to ChatGPT and post the answer back into the same channel.
It uses the [reverse engineered ChatGPT API](https://github.com/acheong08/ChatGPT).

## Setup
### Installation
`pip install -r requirements.txt`

### Configuration
Set values for the parameters at the top of the script for the ChatGPT and TeamSpeak
authentication, the id of the channel that should be used and customization like
the display name in the TeamSpeak chat or how a message needs to begin to be sent to 
ChatGPT (e.g. "!chatgpt ...").

## Usage
Well there is really not much to it but here you go:
1. Run the script.
2. Connect to the TeamSpeak server and move to the channel where you configured the bot to listen for messages.
3. Type your question with the specified prefix in the channel chat and wait for the answer.

# TODO
- [ ] Listen for messages in all channels not just one
- [ ] Create the bot as full client which can be seen as user in TeamSpeak instead of a ServerQuery bot