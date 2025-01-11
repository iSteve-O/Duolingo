import hassapi as hass
import paho.mqtt.client as mqtt
import duolingo
from datetime import datetime
import json

class DuolingoApp(hass.Hass):

    def initialize(self):
        # Runs the script immediately and then once every hour (adjust as needed)
        self.run_every(self.run_script, "now", 1800)
        # Listen for a custom event to trigger manually
        self.listen_event(self.manual_trigger, "MANUAL_DUOLINGO_TRIGGER")

    def run_script(self, kwargs):
        # Get the Duolingo info
        lingo = duolingo.Duolingo('username', jwt='YOUR_TOKEN_HERE')
        streak_info = lingo.get_streak_info()
        site_streak = streak_info.get('site_streak', 0)
        streak_extended_today = streak_info.get('streak_extended_today', False)

        # Prepare timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Ensure payloads are valid JSON
        payload_extended_today = json.dumps({
            "state": streak_extended_today,
            "timestamp": timestamp
        })

        # MQTT setup
        broker = "core-mosquitto"  # Replace with your MQTT broker's address
        mqtt_user = "username"
        mqtt_pass = "PASSWORD"

        # Create MQTT client
        client = mqtt.Client()
        client.username_pw_set(mqtt_user, mqtt_pass)
        client.connect(broker, 1883, 60)

        # Publish to MQTT topics
        client.publish(
            "duolingo/streak/site_streak",
            payload=f'{{"state": {site_streak}, "timestamp": "{timestamp}"}}',
            retain=True
        )
        client.publish(
            "duolingo/streak/streak_extended_today",
            payload=payload_extended_today,
            retain=True
        )

        client.disconnect()

# Method to trigger the script manually from HA automation
    def manual_trigger(self, event_name, data, kwargs):
        self.run_script({})
#        self.publish_streak_info()
