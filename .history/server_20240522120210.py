from flask import Flask, jsonify
from hubspot_api import HubSpotApi

app = Flask(__name__)

# Authentication callback for 2FA
def cb_auth() -> str:
    code = input('Enter 2FA code: ')
    return code

# Initialize HubSpot API
hs = HubSpotApi('ugshanyucolab@gmail.com', 'Thisisnewpassword123', cb_auth)

@app.route('/get_threads', methods=['GET'])
def get_threads():
    threads = hs.conversations.get_threads()
    agents = hs.conversations.get_agents()
    
    # Print thread details
    thread_details = []
    for t in threads:
        details = {
            'details': t.read_details(),
            'id': t.id,
            'status': t.status
        }
        thread_details.append(details)
        print('---------')
        print("thread", t.read_details())
        print("thread id", t.id)
        print("thread status", t.status)
    
    return jsonify(thread_details)

if __name__ == '__main__':
    app.run(debug=True)
