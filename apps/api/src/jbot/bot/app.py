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

    respond({"response_type": "ephemeral", "text": message})


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "callback_id": "home_view",
                # body of the view
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home tab_* :tada:",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app.",
                        },
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {"type": "plain_text", "text": "Click me!"},
                            }
                        ],
                    },
                ],
            },
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


# Ready? Start your app!
if __name__ == "__main__":
    app.start(port=int(config.get_or_default("PORT", 9000)))
