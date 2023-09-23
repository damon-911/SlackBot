import asyncio
import gspread
import oauth2client.service_account
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from custom_secrets import SLACK_SIGNING_SECRET, SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_BOT_JSON, GOOGLE_SHEET_URL, GOOGLE_SHEET_NAME

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
json = SLACK_BOT_JSON
credentials = oauth2client.service_account.ServiceAccountCredentials.from_json_keyfile_name(
    json, scope)
gc = gspread.authorize(credentials)
sheet_url = GOOGLE_SHEET_URL
doc = gc.open_by_url(sheet_url)
worksheet = doc.worksheet(GOOGLE_SHEET_NAME)
data = worksheet.col_values(9)

app = AsyncApp(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)


@app.event("message")  # 앱이 설치된 채널에 메세지가 올라올 때
async def handle_message_events(event, message, say):
    list = message.get('text').split(' ')

    length = len(list)

    command = list[0]

    if (command == '!등록'):
        if (length <= 2):
            await say("입력 형식에 맞지 않습니다.")
            return

        user = list[length - 1]

        phone = ''
        for i in range(1, length - 1):
            phone += list[i] + ' '
        phone = phone[0:len(phone)-1]

        for i in range(0, len(data)):
            if (data[i].lower() == phone.lower()):
                cellPos = 'L' + str(i + 1)
                if (worksheet.acell(cellPos).value == None):
                    worksheet.update_acell(cellPos, user)
                    await say("등록이 완료되었습니다.")
                else:
                    await say("소유자가 이미 등록되어 있습니다.")
                return

        await say(phone + "은(는) 존재하지 않습니다.")
        return
    elif (command == '!해제'):
        if (length <= 1):
            await say("입력 형식에 맞지 않습니다.")
            return

        phone = ''
        for i in range(1, length):
            phone += list[i] + ' '
        phone = phone[0:len(phone)-1]

        for i in range(0, len(data)):
            if (data[i].lower() == phone.lower()):
                cellPos = 'L' + str(i + 1)
                if (worksheet.acell(cellPos).value != None):
                    worksheet.update_acell(cellPos, "")
                    await say("해제가 완료되었습니다.")
                else:
                    await say("소유자가 등록되어 있지 않습니다.")
                return

        await say(phone + "은(는) 존재하지 않습니다.")
        return
    elif (command[0] != '!'):
        return
    else:
        await say("등록되어 있는 명령어가 아닙니다.")
        return


async def main():
    handler = AsyncSocketModeHandler(
        app, app_token=SLACK_APP_TOKEN)
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())
