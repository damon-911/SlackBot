from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slash_secrets import SLACK_SIGNING_SECRET, SLACK_BOT_TOKEN

app = Flask(__name__)

slack_app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

handler = SlackRequestHandler(slack_app)


@app.route('/slack/commands', methods=["POST"])
def command():
    data = request.form

    if data['command'] == "/hello":
        message = f"안녕 <@{data['user_id']}>!"
    else:
        message = f"Invalid command: {data['command']}"

    return jsonify({"text": message})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
