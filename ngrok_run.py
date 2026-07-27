from pyngrok import ngrok, conf
import subprocess, time, os
from dotenv import load_dotenv
load_dotenv(override=True)

conf.get_default().auth_token = os.getenv("NGROK_AUTHTOKEN")

proc = subprocess.Popen(["streamlit", "run", "app.py",
                         "--server.port", "8501",
                         "--server.headless", "true"])
time.sleep(5)

tunnel = ngrok.connect(8501)
print(f"\n🌍 Share this link for your demo: {tunnel.public_url}\n")
input("Press Enter to stop the demo server...\n")
ngrok.kill()
proc.kill()