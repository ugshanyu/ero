from flask import Flask, request, jsonify
from hubspot_api import HubSpotApi

app = Flask(__name__)

# Authentication callback for 2FA
def cb_auth() -> str:
    code = input('Enter 2FA code: ')
    return code

# Initialize HubSpot API
hs = HubSpotApi('ugshanyucolab@gmail.com', 'Thisisnewpassword123', cb_auth)

@app.route('/get_contact_info/<full_name>', methods=['GET'])
def get_contact_info(full_name):
    first_name, last_name = full_name.split(' ', 1)

    threads = hs.conversations.get_threads()
    agents = hs.conversations.get_agents()

    for i in agents.list:
        print(i)

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