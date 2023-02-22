import ts3
from revChatGPT.V1 import Chatbot
from ts3.definitions import TextMessageTargetMode
from ts3.query import TS3TimeoutError

# ------------------------------- Config -------------------------------
# ChatGPT authentication
CHATGPT = Chatbot(config={
    "email": "<OpenAI email>",
    "password": "<OpenAI password>"
})

# TeamSpeak ServerQuery connection
TS_QUERY_USERNAME = "<ServerQuery username>"
TS_QUERY_PASSWORD = "<ServerQuery password>"
TS_ADDRESS = "<TeamSpeak address>"
BOT_DISPLAY_NAME = "<Bot display name in the TeamSpeak chat>"

# ServerQuery connection type - Telnet or SSH ?
URI = f"ssh://{TS_QUERY_USERNAME}:{TS_QUERY_PASSWORD}@{TS_ADDRESS}:10022"
# URI = "telnet://{TS_QUERY_USERNAME}:{TS_QUERY_PASSWORD}@{TS_ADDRESS}:10011"

# The TeamSpeak channel to listen in (use 'channellist' command to get the IDs)
TS_CHANNEL_ID = 1

# Only send the message to ChatGPT if it starts with this prefix (e.g. !chatgpt)
MESSAGE_PREFIX = "<Message prefix>"


# ----------------------------------------------------------------------


def ts_chat_bot(ts3conn):
    ts3conn.exec_("clientupdate", client_nickname=BOT_DISPLAY_NAME)

    # Gather client id of own query connection
    own_client_id = ts3conn.exec_("whoami")[0]['client_id']

    # Change into the channel that should be listened for messages
    ts3conn.exec_("clientmove", clid=own_client_id, cid=TS_CHANNEL_ID)

    # Register to be notified about text events in current channel
    ts3conn.exec_("servernotifyregister", event="textchannel")

    while True:
        # Sends empty query to keep connection alive every 2 minutes if there was no event
        ts3conn.send_keepalive()
        try:
            event = ts3conn.wait_for_event(timeout=120)
        except TS3TimeoutError:
            continue

        # Do not react to self generated message events
        if event[0]["invokerid"] != own_client_id:
            message = event[0]["msg"]

            # Ignore messages that do not start with the specified prefix
            if not message.lower().startswith(MESSAGE_PREFIX.lower()):
                continue

            # Remove the prefix from the message before sending it
            message = message.lower().removeprefix(MESSAGE_PREFIX.lower())

            # Send message to ChatGPT and wait for response
            response = ""
            for data in CHATGPT.ask(
                message
            ):
                response = data["message"]

            # Paste ChatGPT response in TeamSpeak chat
            ts3conn.exec_("sendtextmessage", targetmode=TextMessageTargetMode.CHANNEL, msg=response)


if __name__ == "__main__":
    # Connect to the TeamSpeak ServerQuery and start the chatbot
    with ts3.query.TS3ServerConnection(URI) as ts3conn:
        ts3conn.exec_("use", sid=1)
        ts_chat_bot(ts3conn)
