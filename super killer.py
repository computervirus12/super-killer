import ctypes
import time
import random
import threading

# --- Windows API Setup ---
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
winmm = ctypes.windll.winmm
user32.SetProcessDPIAware()

SW = user32.GetSystemMetrics(0)
SH = user32.GetSystemMetrics(1)

# List of your specific uploaded sounds
# Make sure these files are in the same folder as this script
UPLOADED_SOUNDS = [
    "glitch-sounds-26212.mp3",
    "glitch-scream-305035.mp3",
    "glitch-sound-333220.mp3",
    "glitch-101494.mp3",
    "glitch-162763.mp3",
    "tv-glitch-6245.mp3",
    "glitch-collection-6018.mp3",
    "glitch-farm-001-55812.mp3",
    "glitch-farm-003-57853.mp3",
    "glitch-lazer-232465.mp3"
]

# --- Visual Freakout Functions ---

def effect_shake():
    """Violent screen shaking"""
    hdc = user32.GetDC(0)
    x = random.randint(-30, 30)
    y = random.randint(-30, 30)
    gdi32.BitBlt(hdc, x, y, SW, SH, hdc, 0, 0, 0xCC0020)
    user32.ReleaseDC(0, hdc)

def effect_invert():
    """Flash invert colors"""
    hdc = user32.GetDC(0)
    gdi32.PatBlt(hdc, 0, 0, SW, SH, 0x550009)
    user32.ReleaseDC(0, hdc)

def effect_glitch_rect():
    """Draws a random glitched rectangle of the desktop onto itself"""
    hdc = user32.GetDC(0)
    x1 = random.randint(0, SW)
    y1 = random.randint(0, SH)
    x2 = random.randint(0, SW)
    y2 = random.randint(0, SH)
    w = random.randint(100, 500)
    h = random.randint(100, 500)
    gdi32.BitBlt(hdc, x1, y1, w, h, hdc, x2, y2, 0xCC0020)
    user32.ReleaseDC(0, hdc)

# --- Sound & Sync Engine ---

def play_uploaded_sound(file_name):
    """Plays the specific MP3 and runs a visual freakout during its duration"""
    alias = f"glitch_{random.randint(1, 9999)}"
    
    # Open and Play the MP3 from the local directory
    winmm.mciSendStringW(f'open "{file_name}" type mpegvideo alias {alias}', None, 0, 0)
    winmm.mciSendStringW(f"play {alias}", None, 0, 0)
    
    # Freakout timing: Run visuals while the sound is active
    for _ in range(random.randint(10, 20)):
        effect_shake()
        if random.random() > 0.7:
            effect_glitch_rect()
        if random.random() > 0.9:
            effect_invert()
        time.sleep(0.02) # Fast, glitchy timing

    # Close the sound so it can be replayed
    winmm.mciSendStringW(f"stop {alias}", None, 0, 0)
    winmm.mciSendStringW(f"close {alias}", None, 0, 0)

def main_loop():
    print("Infinite Desktop Freakout Started.")
    print("Using your uploaded MP3 files.")
    
    try:
        while True:
            # Pick one of your 9+ uploaded sounds
            current_glitch = random.choice(UPLOADED_SOUNDS)
            
            # Start the sound and the perfectly timed effect
            # Threading ensures the loop stays infinite and smooth
            t = threading.Thread(target=play_uploaded_sound, args=(current_glitch,))
            t.start()
            
            # Delay between sound bursts to keep the loop going infinitely
            time.sleep(random.uniform(0.2, 0.8))
            
    except KeyboardInterrupt:
        # Refresh screen to normal on exit
        user32.InvalidateRect(0, 0, 1)

if __name__ == "__main__":
    main_loop()