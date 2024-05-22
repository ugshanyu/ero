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
assistant_id = os.getenv('ASSISTANT_ID')

# Initialize HubSpot API
hs = HubSpotApi(hs_username, hs_password, cb_auth)

@app.route('/assign-to-least-busy/<full_name>', methods=['GET'])
def assign_to_least_busy(full_name):
    assigned = False
    first_name, last_name = full_name.split(' ', 1)

    threads = hs.conversations.get_threads()
    agents = hs.conversations.get_agents()

    # Filter and print thread details
    thread_details = []
    assigned_agents_count = {}
    for i in agents.list:
        assigned_agents_count[str(i.userId)] = 0

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
            assigned = True
            break

    # name should be last name's first letter + full first name of the agent
    if assigned:
        # Check if lastName is not None and not an empty string
        if least_busy_agent.lastName and least_busy_agent.lastName.strip():
            name = least_busy_agent.lastName[0]+ "." + least_busy_agent.firstName
        else:
            # Handle the case where lastName is not available
            name = least_busy_agent.firstName
            # Optionally, log or handle the absence of a lastName
    return jsonify({"result": assigned, "name": name})

@app.route('/hubspot-webhook', methods=['POST'])
def hubspot_webhook():
    data = request.json
    print('Received webhook data:', data)
    try:
        if data and isinstance(data, list):
            for event in data:
                if event.get('subscriptionType') == 'conversation.propertyChange' and event.get('changeFlag') == 'PROPERTY_CHANGE':
                    # Handle property change event
                    property_name = event.get('propertyName')
                    property_value = event.get('propertyValue')
                    thread_id = event.get('objectId')
                    if(property_value == "A-66918313"):
                        thread_status[thread_id] = True
                    print(f'Property {property_name} changed to {property_value} for object {event.get("objectId")}')
    except Exception as e:
        print("===> !!!Error!!!", e)
        return jsonify(status='success', result=True), 200    
            
    return jsonify(status='success', result=True), 200

if __name__ == '__main__':
    app.run(debug=True)
