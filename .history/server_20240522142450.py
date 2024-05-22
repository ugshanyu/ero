from flask import Flask, request, jsonify
from hubspot_api import HubSpotApi

app = Flask(__name__)

# Authentication callback for 2FA
def cb_auth() -> str:
    code = input('Enter 2FA code: ')
    return code

# Initialize HubSpot API
hs = HubSpotApi('ugshanyucolab@gmail.com', 'Thisisnewpassword123', cb_auth)

# Update agent state. Loop through all threads and count the number of threads assigned to each agent
@app.route('/update_agent_state', methods=['GET'])
def update_agent_state():
    threads = hs.conversations.get_threads()
    agents = hs.conversations.get_agents()

    # Filter and print thread details
    agent_thread_count = {}
    for t in threads:
        detail = t.read_details()
        print("detail", detail)
        if "assignedAgentId" in detail:
            agent_id = detail["assignedAgentId"]
            if agent_id in agent_thread_count:
                agent_thread_count[agent_id] += 1
            else:
                agent_thread_count[agent_id] = 1
    
    # Write to file
    with open("agent_thread_count.txt", "w") as f:
        for agent_id, thread_count in agent_thread_count.items():
            agent = agents.from_id(agent_id)
            f.write(f"{agent.full_name()}: {thread_count}\n")

    return jsonify(agent_thread_count)

@app.route('/get_contact_info/<full_name>', methods=['GET'])
def get_contact_info(full_name):
    first_name, last_name = full_name.split(' ', 1)

    threads = hs.conversations.get_threads()
    agents = hs.conversations.get_agents()

    for i in agents.list:
        print(i)
        print("i.agentState", i.agentState)

    # Filter and print thread details
    thread_details = []
    for t in threads:
        detail = t.read_details()
        if ("visitor" in detail and
            "firstName" in detail["visitor"] and
            "lastName" in detail["visitor"] and
            detail["visitor"]["firstName"] == first_name and
            detail["visitor"]["lastName"] == last_name):
            t.assign(agents.find('Uuganbayar Temuujin'))
            break

    return jsonify(thread_details)

if __name__ == '__main__':
    app.run(debug=True)
