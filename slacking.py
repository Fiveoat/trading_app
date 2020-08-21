from slacker import Slacker


class SlackHandler:
    # TODO: INTEGRATE WITH OTHER CLASSES
    def __init__(self):
        self.slack_api_key = "xoxb-1255877854884-1249693000770-KBuGSqE5BVlswuReD4vrYg4A"
        self.slack = Slacker(self.slack_api_key)
        self.michael = "U017BLE2JSW"
        self.fiveoat = "U0181FNLQ00"
        self.jackson = ""
        self.team = [self.michael, self.fiveoat, self.jackson]

    def send_message(self, member, message):
        self.slack.chat.post_message(member, message, as_user=True)

    def send_team_message(self, message):
        return [self.send_message(member, message) for member in self.team if member]


if __name__ == '__main__':
    sh = SlackHandler()
