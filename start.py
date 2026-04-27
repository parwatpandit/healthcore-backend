import subprocess
import sys
import os
import signal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

processes = []

def stop_all(sig, frame):
    print("\nStopping all services...")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, stop_all)

def run(command):
    p = subprocess.Popen(
        command,
        shell=True,
        cwd=BASE_DIR,
    )
    processes.append(p)
    return p

print("Starting HealthCore backend services...")
print("=" * 40)

run("source venv/bin/activate && python manage.py runserver")
print("✓ Django server starting on http://127.0.0.1:8000")

run("source venv/bin/activate && celery -A healthcore worker --loglevel=info --pool=solo")
print("✓ Celery worker starting...")

run("source venv/bin/activate && celery -A healthcore beat --loglevel=info")
print("✓ Celery beat starting...")

print("=" * 40)
print("All services running! Press Ctrl+C to stop everything.")
print("=" * 40)

for p in processes:
    p.wait()