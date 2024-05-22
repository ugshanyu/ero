# from flask import Flask, request, jsonify
# from hubspot_api import HubSpotApi
# import os

# app = Flask(__name__)

# # Authentication callback for 2FA
# def cb_auth() -> str:
#     code = input('Enter 2FA code: ')
#     return code

# hs_username = os.getenv('HUBSPOT_USERNAME')
# hs_password = os.getenv('HUBSPOT_PASSWORD')
# mongol_gpt_id = os.getenv('MONGOL_GPT_ID')


# # Initialize HubSpot API
# hs = HubSpotApi(hs_username, hs_password, cb_auth)

# @app.route('/assign-to-least-busy/<full_name>', methods=['GET'])
# def assign_to_least_busy(full_name):
#     assigned = False
#     first_name, last_name = full_name.split(' ', 1)

#     threads = hs.conversations.get_threads()
#     agents = hs.conversations.get_agents()
#     thread_id = None

#     # Filter and print thread details
#     thread_details = []
#     assigned_agents_count = {}
#     for i in agents.list:
#         assigned_agents_count[str(i.userId)] = 0

#     for t in threads:
#         agent_id = t.assigned_agent
#         assigned_agents_count[agent_id] = assigned_agents_count.get(agent_id, 0) + 1
    
#     print("assigned_agents_count", assigned_agents_count)
#     # Find least busy agent
#     least_busy_agent_id = None
#     least_busy_agent_count = float('inf')
#     for agent_id, count in assigned_agents_count.items():
#         if count < least_busy_agent_count:
#             least_busy_agent_count = count
#             least_busy_agent_id = agent_id

#     least_busy_agent = None

#     for i in agents.list:
#         if str(i.userId) == str(least_busy_agent_id):
#             least_busy_agent = i

#     for t in threads:
#         detail = t.read_details()
#         if ("visitor" in detail and
#             "firstName" in detail["visitor"] and
#             "lastName" in detail["visitor"] and
#             detail["visitor"]["firstName"] == first_name and
#             detail["visitor"]["lastName"] == last_name):
#             t.assign(least_busy_agent)
#             thread_id = t.id
#             assigned = True
#             break

#     # name should be last name's first letter + full first name of the agent
#     if assigned:
#         # Check if lastName is not None and not an empty string
#         if least_busy_agent.lastName and least_busy_agent.lastName.strip():
#             name = least_busy_agent.lastName[0]+ "." + least_busy_agent.firstName
#         else:
#             # Handle the case where lastName is not available
#             name = least_busy_agent.firstName
#             # Optionally, log or handle the absence of a lastName
#     return jsonify({"result": assigned, "name": name, "thread_id": thread_id})

# if __name__ == '__main__':
#     # Run the server on port 6000
#     app.run(debug=True, port=6000)

from flask import Flask, request, jsonify
from hubspot_api import HubSpotApi
import os

app = Flask(__name__)

# Authentication callback for 2FA
def cb_auth() -> str:
    code = input('Enter 2FA code: ')
    return code

hs_username = os.getenv('HUBSPOT_USERNAME')
hs_password = os.getenv('HUBSPOT_PASSWORD')
mongol_gpt_id = os.getenv('MONGOL_GPT_ID')

# Initialize HubSpot API
hs = HubSpotApi(hs_username, hs_password, cb_auth)

@app.route('/assign-to-least-busy/<full_name>', methods=['GET'])
def assign_to_least_busy(full_name):
    assigned = False
    first_name, last_name = full_name.split(' ', 1)

    threads = hs.conversations.get_threads()
    agents = hs.conversations.get_agents()
    thread_id = None

    # Filter and print thread details
    assigned_agents_count = {}
    for agent in agents.list:
        if agent.userId != mongol_gpt_id:
            print("agent", agent.userId)
            print("mongol_gpt_id", mongol_gpt_id)
            print("str(agent.userId) != mongol_gpt_id", str(agent.userId) != mongol_gpt_id)
            assigned_agents_count[str(agent.userId)] = 0

    for t in threads:
        agent_id = t.assigned_agent
        if agent_id in assigned_agents_count:
            assigned_agents_count[agent_id] = assigned_agents_count.get(agent_id, 0) + 1
    
    print("assigned_agents_count", assigned_agents_count)
    # Find least busy agent
    least_busy_agent_id = None
    least_busy_agent_count = float('inf')
    for agent_id, count in assigned_agents_count.items():
        if count < least_busy_agent_count:
            least_busy_agent_count = count
            least_busy_agent_id = agent_id

    least_busy_agent = None
    for agent in agents.list:
        if str(agent.userId) == str(least_busy_agent_id):
            least_busy_agent = agent

    for t in threads:
        detail = t.read_details()
        if ("visitor" in detail and
            "firstName" in detail["visitor"] and
            "lastName" in detail["visitor"] and
            detail["visitor"]["firstName"] == first_name and
            detail["visitor"]["lastName"] == last_name):
            t.assign(least_busy_agent)
            thread_id = t.id
            assigned = True
            break

    if assigned:
        if least_busy_agent.lastName and least_busy_agent.lastName.strip():
            name = least_busy_agent.lastName[0]+ "." + least_busy_agent.firstName
        else:
            name = least_busy_agent.firstName

    return jsonify({"result": assigned, "name": name, "thread_id": thread_id})

if __name__ == '__main__':
    app.run(debug=True, port=6000)
