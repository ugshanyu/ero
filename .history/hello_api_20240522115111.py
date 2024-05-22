from hubspot_api import HubSpotApi

def cb_auth() -> str: # In case of 2FA, you'll need to return the code
    code = input('Enter 2FA code: ')
    return code

hs = HubSpotApi('ugshanyucolab@gmail.com', 'Thisisnewpassword123', cb_auth)

# You can also do hs.conversations.get_threads() to get all threads
threads = hs.conversations.get_threads(search_query="хүслэн")
# Needed for assigning threads to agents
agents = hs.conversations.get_agents()

print(f"Found {len(threads)} threads")

for t in threads:
    print('---------')
    print("thread", t.read_details())
    print("thread id", t.id)
    print("thread status", t.status)
    # print('---------\nSubject:',t.subject, t.timestamp)
    # msgs = t.read_messages()
    # email_msgs = [f"FROM: {msg.fromName}, AT: {msg.timestamp}, EMAIL TEXT:\n{msg.text}" for msg in msgs]
    # full_conversation = f'EMAIL SUBJECT: {t.subject}\n' + '\n\n'.join(email_msgs).lower()

    # # Do some smart LLM stuff here

    # if "api" in full_conversation or "code" in full_conversation:
    #     t.assign(agents.find('John Doe')) # Tech support
    # elif "shipping" in full_conversation:
    #     t.assign(agents.find('Erik The Red')) # Ops/shipping
    # elif "digital agency" in full_conversation:
    #     # They are trying to sell us something
    #     t.send_message("Thank you for your email, but we are not interested.")
    #     t.close()
    # elif "tiktok" in full_conversation:
    #     t.spam() # TikTok? Spam for sure
    # else:
    #     # Writing a comment (and tagging an agent) is also supported
    #     agent = agents.find('John Doe')
    #     t.comment(f'Hi {agent}, could you assign this to the best person?')