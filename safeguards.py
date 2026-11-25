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

    # Check the summary has all the fields we asked for
def check_summary(data):
    if not isinstance(data, dict):
        return False
    text = data.get("summary")
    if not isinstance(text, str) or text.strip() =="":
        return False
    if not isinstance(data.get("breakdown"), dict):
        return False
    if not isinstance(data.get("total_spent"), (int, float)):
        return False
    tips = data.get("ways_to_save")
    return isinstance(tips, list) and len(tips) == 3