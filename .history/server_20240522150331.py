from flask import Flask, request, jsonify
from hubspot_api import HubSpotApi

app = Flask(__name__)

# Authentication callback for 2FA
def cb_auth() -> str:
    code = input('Enter 2FA code: ')
    return code

# Initialize HubSpot API
hs = HubSpotApi('ugshanyucolab@gmail.com', 'Thisisnewpassword123', cb_auth)

@app.route('/assign-to-least-busy/<full_name>', methods=['GET'])
def get_contact_info(full_name):
    first_name, last_name = full_name.split(' ', 1)

    threads = hs.conversations.get_threads()
    agents = hs.conversations.get_agents()

    # Filter and print thread details
    thread_details = []
    assigned_agents_count = {}
    for t in threads:
        agent_id = t.assigned_agent
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

    for i in agents.list:
        if str(i.userId) == str(least_busy_agent_id):
            least_busy_agent = i

    for t in threads:
        detail = t.read_details()
        if ("visitor" in detail and
            "firstName" in detail["visitor"] and
            "lastName" in detail["visitor"] and
            detail["visitor"]["firstName"] == first_name and
            detail["visitor"]["lastName"] == last_name):
            t.assign(least_busy_agent)
            break

    return jsonify(thread_details)

if __name__ == '__main__':
    app.run(debug=True)
