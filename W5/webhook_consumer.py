from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook-listener", methods=["POST"])
def receive_webhook():
    if request.is_json:
        data = request.get_json()
        event_type = data.get("event")
        event_data = data.get("data")

        print("Webhook Received!")
        print(f"Event Type: {event_type}")
        print(f"Data: {event_data}")
        
        return "Webhook received successfully!", 200
    
    return "Invalid request", 400

if __name__ == "__main__":
    app.run(debug=True, port=5002)