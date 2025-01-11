import paho.mqtt.client as mqtt
import duolingo
from datetime import datetime
import json

# This block gets the info
lingo  = duolingo.Duolingo('username', jwt='YOUR_JWT_TOKEN_FROM_BROWSER')
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

# This block prints the info nicely. Uncomment these 2 lines to debug & ensure the right info is returned.
#print(f"Site Streak: {site_streak}")
#print(f"Streak Extended Today: {streak_extended_today}")

# This block sets up MQTT
broker = "core-mosquitto"  # Replace with your MQTT broker's address
mqtt_user = "username"
mqtt_pass = "PASSWORD"
topic_site_streak = "duolingo/streak/site_streak"
topic_extended_today = "duolingo/streak/streak_extended_today"

# This block publishes to MQTT
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_pass)
client.connect(broker, 1883, 60)
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
# Disconnect from MQTT
client.disconnect()
