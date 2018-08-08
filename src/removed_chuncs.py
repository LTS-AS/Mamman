import hashlib
import win32ui

def event_fingerprint_file(icon, item):
    with open("C:\Test\Full folder\_junk.txt", "rb") as f1:
        checksum2 = hashlib.sha256(f1.read()).hexdigest()
    win32ui.MessageBox(checksum2, 'SHA256 result')