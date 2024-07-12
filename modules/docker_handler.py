import os, signal
import modules.discord as discord
def shutdown_container(error="None"):
    discord.send_webhook(name="Rock for People 2025 - Error", type="error", ig_id=f"Error", caption=f"Error:\n {error}", embed_color="ff0000")
    os.kill(os.getpid(), signal.SIGTERM)