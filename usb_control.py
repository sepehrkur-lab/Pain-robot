# usb_control.py
# Placeholder for USB motor control. Real implementation needs Android USB Host API or serial bridge.
def send_command(cmd: str):
    # cmd is a string like "MOTOR LEFT FORWARD 100"
    # Implementation on Android: use pyjnius to access UsbManager, request permission, open device endpoint and write.
    print("[USB] send:", cmd)
    return False
