import os, signal

def shutdown_container():
    os.kill(os.getpid(), signal.SIGTERM)