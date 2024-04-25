import time
from slack_bolt import App

from src.jbot import config
from src.jbot.openai.assistant import OpenAIAssistant

# Initialize your app with your bot token and signing secret
app = App(
    token=config.get_or_error("SLACK_BOT_TOKEN"),
    signing_secret=config.get_or_error("SLACK_SIGNING_SECRET"),
)

my_assistant = OpenAIAssistant()
assistant_id = "asst_64OUin9tDFmOPi0qkCZLs5Gu"  # wordbricks bot (code search)
my_assistant.create_or_load_assistant(assistant_id=assistant_id)


@app.command("/ask")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    print(command)

    message, citations = my_assistant.chat(command["text"])
    time.sleep(4)

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": command["text"]},
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": message},
        },
    ]

    if len(citations) > 0:
        blocks.append(
            {
                "type": "context",
                "elements": [{"type": "plain_text", "text": c} for c in citations],
            }
        )

    print(command["channel_name"] == "directmessage")
    response_type = (
        "in_channel" if command["channel_name"] == "directmessage" else "ephemeral"
    )
    respond(
        blocks=blocks,
        response_type=response_type,
    )


# Ready? Start your app!
if __name__ == "__main__":
    app.start(port=int(config.get_or_default("PORT", 9000)))
