import json

# Check the AI's JSON reply
def check_reply(data):
    if not isinstance(data, dict):
        return False
    reply=data.get("reply")
    if not isinstance(reply,str) or reply.strip()== "":
        return False
    if not isinstance(data.get("total_spent"), (int, float)):
        return False
    if not isinstance(data.get("totals"), dict):
        return False
    return True