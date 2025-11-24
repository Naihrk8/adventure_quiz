import tkinter as tk
from tkinter import font as tkfont
import textwrap
import time
import os
from pathlib import Path
import json
from datetime import datetime

# AUDIO 
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    pygame = None
    PYGAME_AVAILABLE = False

# Images (Pillow)
try:
    from PIL import Image, ImageTk, ImageSequence
    PIL_AVAILABLE = True
except Exception:
    Image = None
    ImageTk = None
    ImageSequence = None
    PIL_AVAILABLE = False

def make_transparent(pil_img, white_thresh=240):
    """
    Return a copy of pil_img converted to RGBA with near-white pixels made transparent.
    white_thresh: 0-255 threshold; default 240 means R,G,B > 240 considered white.
    """
    if pil_img is None:
        return None
    try:
        im = pil_img.convert("RGBA")
        datas = list(im.getdata())
        new_data = []
        t = int(white_thresh)
        for item in datas:
            r,g,b,a = item
            if r >= t and g >= t and b >= t:
                new_data.append((255,255,255,0))
            else:
                new_data.append((r,g,b,a))
        im.putdata(new_data)
        return im
    except Exception as e:
        print("make_transparent error:", e)
        try:
            return pil_img.convert("RGBA")
        except Exception:
            return pil_img

# PATHS
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except Exception:
    SCRIPT_DIR = Path.cwd()

ASSETS_DIR = (SCRIPT_DIR / "assets") if (SCRIPT_DIR / "assets").exists() else SCRIPT_DIR

# Audio paths (adjust if needed)
CLICK_SOUND_PATH   = Path(r"C:\Python_Adventure_Project") / "Button_Effects.mp3"
BG_MUSIC_PATH      = Path(r"C:\Python_Adventure_Project") / "Bg_music.mp3"
TYPING_SOUND_PATH  = Path(r"C:\Python_Adventure_Project") / "typing.mp3"
LOADING_JINGLE     = Path(r"C:\Python_Adventure_Project") / "loading.mp3"
LOADING_GIF        = Path("loading.gif")
STORY_MUSIC_PATH   = Path(r"C:\Python_Adventure_Project") / "pystory_bg.MP3"
STORY_TYPING_PATH  = Path(r"C:\Python_Adventure_Project") / "txt_bg.MP3"

DOOR_BG_PATH = SCRIPT_DIR / "bg_door.png"
ENDING_GIF_PATH = SCRIPT_DIR / "end_1s.gif"

# Image hints
IMG_S1_HINT = "character_s1"
IMG_S2_HINT = "character_s2"
IMG_S3_HINT = "character_s3"
IMG_S4_HINT = "character_s4"
IMG_S5_HINT = "black_s5"
IMG_S6_HINT = "character_s6"
IMG_S7_HINT = "character_s7"
IMG_S8_HINT = "character_s8"
IMG_S9_HINT = "character_s9"

CHAR_SPRITE_HINT = "final_walk.gif"
DOOR_CLOSED_HINT = "door_close"
DOOR_OPEN_HINT   = "door_open"

IMG_S_CRY_HINT   = "cry_boy"
IMG_S_HAPPY_HINT = "happy_boy"

# search dirs order
SEARCH_DIRS = [Path.cwd(), ASSETS_DIR, SCRIPT_DIR, Path("/mnt/data")]

# file extensions to try
COMMON_EXTS = [".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4"]

def find_file_by_hint(hint):
    if not hint:
        return None
    cand = Path(hint)
    if cand.exists() and cand.is_file():
        return cand.resolve()
    
    if cand.suffix:
        for d in SEARCH_DIRS:
            try:
                p = (d / cand.name)
                if p.exists() and p.is_file():
                    return p.resolve()
            except Exception:
                pass
 
    for d in SEARCH_DIRS:
        for ext in COMMON_EXTS:
            try:
                p = d / (hint + ext)
                if p.exists() and p.is_file():
                    return p.resolve()
            except Exception:
                pass

    for d in SEARCH_DIRS:
        try:
            if not d.exists(): continue
            for p in d.iterdir():
                if p.is_file() and p.stem.lower().startswith(hint.lower()):
                    return p.resolve()
        except Exception:
            pass
    return None

# Resolve paths
IMG_S1 = find_file_by_hint(IMG_S1_HINT)
IMG_S2 = find_file_by_hint(IMG_S2_HINT)
IMG_S3 = find_file_by_hint(IMG_S3_HINT)
IMG_S4 = find_file_by_hint(IMG_S4_HINT)
IMG_S5 = find_file_by_hint(IMG_S5_HINT) or find_file_by_hint("character_s5")
IMG_S6 = find_file_by_hint(IMG_S6_HINT)
IMG_S7 = find_file_by_hint(IMG_S7_HINT)
IMG_S8 = find_file_by_hint(IMG_S8_HINT)
IMG_S9 = find_file_by_hint(IMG_S9_HINT)

CHAR_SPRITE_PATH = find_file_by_hint(CHAR_SPRITE_HINT)
DOOR_CLOSED_PATH = find_file_by_hint(DOOR_CLOSED_HINT)
DOOR_OPEN_PATH   = find_file_by_hint(DOOR_OPEN_HINT)
# Medal image files 
GOLD_MEDAL_PATH   = SCRIPT_DIR / "gold_medal.png"
SILVER_MEDAL_PATH = SCRIPT_DIR / "silver_medal.png"
BRONZE_MEDAL_PATH = SCRIPT_DIR / "bronze_medal.png"

IMG_S_CRY = find_file_by_hint(IMG_S_CRY_HINT)
IMG_S_HAPPY = find_file_by_hint(IMG_S_HAPPY_HINT)

try:
    walk_candidate = Path("/mnt/data/walk_vid.mp4")
    if walk_candidate.exists() and walk_candidate.is_file():
        CHAR_SPRITE_PATH = walk_candidate.resolve()
except Exception:
    pass

# Leaderboard file
LEADERBOARD_PATH = SCRIPT_DIR / "leaderboard.json"
MAX_LEADERBOARD_ENTRIES = 200

# UI constants
WIDTH, HEIGHT = 1370, 730
BUTTON_W, BUTTON_H = 400, 80
PANEL_MARGIN = 12

WHITE = "#FFFFFF"
ORANGE = "#FFAA00"
HOVER_YELLOW = "#FFD166"
DARK_ORANGE = "#C86400"
BORDER = "#643200"
BLACK = "#000000"

BG_SCROLL_SPEED = 0.6
BG_SCROLL_DIRECTION = "left"

# Typewriter timing 
CHAR_DELAY = 4        
PUNCT_DELAY = 60     
NEWLINE_DELAY = 40  

# Game data 
questions = [
    {
        "story": "You step into a dim chamber. A plaque reads: 'Talk like the developers.'",
        "question": "Which symbol is used for comments in Python?",
        "answer": "b",
        "options": ["//", "#", "*", "--"]
    },
    {
        "story": "A luminous pedestal displays a simple arithmetic riddle.",
        "question": "What will print(2 + 3) show?",
        "answer": "b",
        "options": ["23", "5", "2+3", "Error"]
    },
    {
        "story": "You enter a room with gears turning. It asks about repetition.",
        "question": "Which loop repeats code a number of times?",
        "answer": "c",
        "options": ["if loop", "repeat loop", "for loop", "check loop"]
    },
    {
        "story": "A friendly terminal offers a challenge about interaction.",
        "question": "Which function lets the user enter something?",
        "answer": "a",
        "options": ["input()", "enter()", "ask()", "type()"]
    },
    {
        "story": "A final door asks about file types used by Python programmers.",
        "question": "What file extension is commonly used for Python files?",
        "answer": "a",
        "options": [".py", ".pt", ".exe", ".txt"]
    }
]

instructions_text = """Welcome to Python Adventure Quiz!

>> Answer Python questions to collect keys.
>> Each correct answer unlocks the next stage.
>> Wrong answers reduce your lives.
>> Lose all lives = GAME OVER.

Goal: Reach the end with all keys!

Tips:
- Some questions are tricky, think carefully!
- Read the whole question before answering.
- Eliminate obviously wrong choices first.
- Try tiny test cases in your head.
- Watch your lives, don't rush."""

about_text = """Project Overview:
An interactive story-based Python quiz game.

Description:
Players collect keys by answering questions.
Correct answers unlock stages, wrong ones reduce lives.

Objectives:
- Make quizzes fun & interactive
- Engage students through storytelling
- Reinforce learning with gamification

Features:
- Storyline Integration
- Question Challenges
- Life System
- Leaderboards

Credits:
Developed by our awesome team:
1. Baniqued, Zyron Dheniel - Project Manager
2. Ocampo, Rhian Kate - Programmer
3. Frias, Justine Andrei - UI/UX Designer
4. Pascual, Shaqckane - Document Writer
5. Ducusin, Katherina - Researcher"""

PROLOGUE_SCENES_TEMPLATE = [
    (IMG_S1, "It was late at night in the computer lab.\nOnly the soft clicking of keys filled the room."),
    (IMG_S2, "Arthan stayed behind,\ntrying to practice Python one last time."),
    (IMG_S3, "But then his screen flickered...\nthe code on it started to move...\nand a sudden flash surrounded him!"),
    (IMG_S4, ""),
    (IMG_S5, "When Arthan opened his eyes,\nhe was no longer in the lab."),
    (IMG_S6, "Instead, he stood in a world\nmade of floating text and glowing symbols."),
    (IMG_S7, "A calm, robotic voice spoke:\n\n\"Welcome, Arthan.\nYou are inside the Python Adventure Quiz.\""),
    (IMG_S8, "A glowing door appeared ahead,\nwaiting for him to take the first step."),
    (IMG_S9, "Arthan took a deep breath.\nIf he wanted to go home,\nhe had to face the quiz.")
]

def safe_load_image(path: Path, target_w=None, target_h=None):
    if not PIL_AVAILABLE:
        return None
    try:
        if path is None:
            return None
        p = Path(path)
        try:
            p_abs = p.resolve(strict=False)
        except Exception:
            p_abs = p
        if not p_abs.is_file():
            return None
        pil = Image.open(str(p_abs)).convert("RGBA")
        if target_w and target_h:
            iw, ih = pil.size
            ratio_src = iw / ih
            ratio_target = target_w / target_h
            if ratio_src > ratio_target:
                new_h = target_h
                new_w = int(ratio_src * new_h)
            else:
                new_w = target_w
                new_h = int(new_w / ratio_src)
            pil = pil.resize((new_w, new_h), Image.LANCZOS)
            left = max(0, (pil.width - target_w) // 2)
            upper = max(0, (pil.height - target_h) // 2)
            pil = pil.crop((left, upper, left + target_w, upper + target_h))
        return pil
    except Exception as e:
        print("safe_load_image error:", e)
        return None

def load_gif_frames(path):
    """
    Load GIF frames as RGBA PIL.Image objects and return (frames_list, durations_list_ms).
    More robust: supports single-frame GIFs and missing 'duration' info.
    """
    frames = []
    durations = []
    try:
        img = Image.open(str(path))
    except Exception as e:
        print("load_gif_frames: cannot open:", e)
        return frames, durations

    try:
        it = ImageSequence.Iterator(img)
        got_any = False
        for f in it:
            got_any = True
            fr = f.convert("RGBA").copy()
            dur = int(f.info.get("duration", 80))
            if dur <= 0: dur = 80
            frames.append(fr)
            durations.append(dur)
        if not got_any:
            # fallback single frame
            fr = img.convert("RGBA").copy()
            frames.append(fr); durations.append(120)
    except Exception as e:
        try:
            fr = img.convert("RGBA").copy()
            frames.append(fr); durations.append(120)
        except Exception as e2:
            print("load_gif_frames fallback failed:", e, e2)
    return frames, durations

# Video loader
def load_video_frames(path, max_frames=60, target_w=None, target_h=None, frame_step=1):
    """
    Attempts to extract frames from a video file and convert them to PIL RGBA images.
    Tries imageio first, then cv2. Returns (frames_list, durations_list_ms).
    - max_frames: maximum number of frames to extract
    - frame_step: sample every Nth frame (1 = every frame)
    - target_w, target_h: if provided, frames will be resized (preserving aspect) and center-cropped
    """
    frames = []
    durations = []
    p = Path(path)
    if not p.exists():
        return frames, durations

    # Try imageio
    try:
        import imageio
        reader = None
        try:
            reader = imageio.get_reader(str(p))
            meta = reader.get_meta_data()
            fps = meta.get("fps", 24)
        except Exception:
            fps = 24
        frame_duration = int(1000 / max(1, int(fps)))
        extracted = 0
        for i, im in enumerate(reader):
            if i % frame_step != 0:
                continue
            if extracted >= max_frames:
                break
            try:
                from PIL import Image as _PIL_Image
                pil = _PIL_Image.fromarray(im).convert("RGBA")
            except Exception:
                try:
                    import numpy as _np
                    from PIL import Image as _PIL_Image
                    pil = _PIL_Image.fromarray(_np.asarray(im)).convert("RGBA")
                except Exception:
                    continue
            if target_w and target_h:
                iw, ih = pil.size
                ratio_src = iw / ih
                ratio_target = target_w / target_h
                if ratio_src > ratio_target:
                    new_h = target_h
                    new_w = int(ratio_src * new_h)
                else:
                    new_w = target_w
                    new_h = int(new_w / ratio_src)
                pil = pil.resize((max(1,new_w), max(1,new_h)), _PIL_Image.LANCZOS)
                left = max(0, (pil.width - target_w) // 2)
                upper = max(0, (pil.height - target_h) // 2)
                pil = pil.crop((left, upper, left + target_w, upper + target_h))
            frames.append(pil)
            durations.append(frame_duration)
            extracted += 1
        try:
            if reader is not None:
                reader.close()
        except Exception:
            pass
        if frames:
            return frames, durations
    except Exception:
        pass

    # Fallback
    try:
        import cv2
        cap = cv2.VideoCapture(str(p))
        fps = cap.get(cv2.CAP_PROP_FPS) or 24
        frame_duration = int(1000 / max(1, int(fps)))
        idx = 0; extracted = 0
        while cap.isOpened() and extracted < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            if idx % frame_step != 0:
                idx += 1; continue
            try:
                import numpy as _np
                from PIL import Image as _PIL_Image
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil = _PIL_Image.fromarray(rgb).convert("RGBA")
            except Exception:
                idx += 1; continue
            if target_w and target_h:
                iw, ih = pil.size
                ratio_src = iw / ih
                ratio_target = target_w / target_h
                if ratio_src > ratio_target:
                    new_h = target_h
                    new_w = int(ratio_src * new_h)
                else:
                    new_w = target_w
                    new_h = int(new_w / ratio_src)
                pil = pil.resize((max(1,new_w), max(1,new_h)), _PIL_Image.LANCZOS)
                left = max(0, (pil.width - target_w) // 2)
                upper = max(0, (pil.height - target_h) // 2)
                pil = pil.crop((left, upper, left + target_w, upper + target_h))
            frames.append(pil)
            durations.append(frame_duration)
            extracted += 1
            idx += 1
        try:
            cap.release()
        except Exception:
            pass
        if frames:
            return frames, durations
    except Exception:
        pass

    return [], []

# Audio init
pygame_available = False
click_sound = None
typing_sound = None
story_typing = None
bg_music_loaded = False

if PYGAME_AVAILABLE:
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame_available = True
    except Exception as e:
        print("pygame.mixer.init failed:", e)
        pygame_available = False

if pygame_available:
    try:
        if CLICK_SOUND_PATH.exists():
            click_sound = pygame.mixer.Sound(str(CLICK_SOUND_PATH)); click_sound.set_volume(0.9)
    except Exception:
        click_sound = None
    try:
        if STORY_TYPING_PATH.exists():
            story_typing = pygame.mixer.Sound(str(STORY_TYPING_PATH)); story_typing.set_volume(0.95)
    except Exception:
        story_typing = None
    try:
        if TYPING_SOUND_PATH.exists():
            typing_sound = pygame.mixer.Sound(str(TYPING_SOUND_PATH)); typing_sound.set_volume(0.75)
    except Exception:
        typing_sound = None
    try:
        if BG_MUSIC_PATH.exists():
            pygame.mixer.music.load(str(BG_MUSIC_PATH)); pygame.mixer.music.set_volume(0.25); pygame.mixer.music.play(-1, fade_ms=800); bg_music_loaded = True
    except Exception:
        bg_music_loaded = False

def play_click():
    if click_sound and pygame_available:
        try: click_sound.play()
        except: pass

def play_typing_generic():
    if typing_sound and pygame_available:
        try:
            typing_sound.stop(); typing_sound.play()
        except Exception:
            pass

# Leaderboard helpers
def load_leaderboard():
    try:
        if LEADERBOARD_PATH.exists():
            with open(LEADERBOARD_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception as e:
        print("load_leaderboard error:", e)
    return []

def save_leaderboard(entries):
    try:
        LEADERBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
            json.dump(entries[:MAX_LEADERBOARD_ENTRIES], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("save_leaderboard error:", e)

def add_score_to_leaderboard(name, keys, lives):
    try:
        name = (name or "Unknown").strip()[:32]
        score = (int(keys) * 100) + (int(lives) * 10)
    except Exception:
        score = 0
    entry = {"name": name or "Unknown", "keys": int(keys), "lives": int(lives), "score": score, "ts": datetime.utcnow().isoformat()+"Z"}
    entries = load_leaderboard()
    entries.append(entry)
    entries.sort(key=lambda e: (e.get("score",0), e.get("ts","")), reverse=True)
    save_leaderboard(entries)
    return entry

def clear_leaderboard_file():
    try:
        if LEADERBOARD_PATH.exists():
            LEADERBOARD_PATH.unlink()
        save_leaderboard([])
    except Exception as e:
        print("clear_leaderboard_file error:", e)

# Font helper
def pick_pixel_like_font(root, preferred_names=None, body_size=18, title_size=36):
    if preferred_names is None:
        preferred_names = ["Press Start 2P"]
    available = list(tkfont.families(root))
    chosen = None
    for name in preferred_names:
        for fam in available:
            if fam.lower() == name.lower() or name.lower() in fam.lower():
                chosen = fam; break
        if chosen: break
    if not chosen:
        monos = [f for f in available if "mono" in f.lower() or "courier" in f.lower()]
        chosen = monos[0] if monos else "Arial"
    body_font  = tkfont.Font(family=chosen, size=16)
    title_font = tkfont.Font(family=chosen, size=28, weight="bold")
    return body_font, title_font, chosen

def wrap_text_to_lines(tk_font, text, max_width):
    lines_out = []
    for para in text.split("\n"):
        words = para.split(" ")
        if not words:
            lines_out.append("")
            continue
        cur = ""
        for w in words:
            test = (cur + " " + w).strip() if cur else w
            if tk_font.measure(test) <= max_width:
                cur = test
            else:
                if cur: lines_out.append(cur)
                if tk_font.measure(w) > max_width:
                    chunk = ""
                    for ch in w:
                        if tk_font.measure(chunk + ch) <= max_width:
                            chunk += ch
                        else:
                            if chunk: lines_out.append(chunk)
                            chunk = ch
                    cur = chunk if chunk else ""
                else:
                    cur = w
        if cur != "": lines_out.append(cur)
        if para == "": lines_out.append("")
    return lines_out

class LoadingScreen(tk.Toplevel):
    def __init__(self, master, duration=2.5, gif_path=LOADING_GIF, jingle_path=LOADING_JINGLE):
        super().__init__(master)
        self.duration = duration
        self.overrideredirect(True)
        self.configure(bg="black")
        master.update_idletasks()
        master_x = master.winfo_rootx(); master_y = master.winfo_rooty()
        master_w = master.winfo_width(); master_h = master.winfo_height()
        if master_w <= 1 or master_h <= 1:
            try:
                geom = master.geometry()
                w_str, h_str = geom.split("+")[0].split("x")
                master_w, master_h = int(w_str), int(h_str)
                parts = geom.split("+")
                if len(parts) >= 3:
                    master_x, master_y = int(parts[1]), int(parts[2])
            except Exception:
                master_w, master_h = WIDTH, HEIGHT
                master_x = int((self.winfo_screenwidth() - master_w) / 2)
                master_y = int((self.winfo_screenheight() - master_h) / 2)
        self.geometry(f"{master_w}x{master_h}+{master_x}+{master_y}")
        self.transient(master); self.attributes("-topmost", True)
        self.canvas = tk.Canvas(self, width=master_w, height=master_h, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.start_time = None; self._after_id = None
        sw, sh = master_w, master_h
        self.canvas.create_text(sw//2, int(sh*0.15), text="LOADING...", font=("Press Start 2P", 22)
, fill=ORANGE)
        self.percent_text_id = self.canvas.create_text(sw//2, int(sh*0.28), text="0%", font=("Consolas", 22), fill=WHITE)
        bar_w = int(sw * 0.6); bar_h = max(16, int(sh * 0.04))
        self.bar_left = (sw - bar_w) // 2; self.bar_top = int(sh * 0.45)
        self.bar_right = self.bar_left + bar_w; self.bar_bottom = self.bar_top + bar_h
        self.canvas.create_rectangle(self.bar_left-4, self.bar_top-4, self.bar_right+4, self.bar_bottom+4, outline=WHITE, width=3)
        self.fill_id = self.canvas.create_rectangle(self.bar_left, self.bar_top, self.bar_left, self.bar_bottom, fill=ORANGE, outline="")
        self.hint_id = self.canvas.create_text(sw//2, int(sh*0.62), text="", font=("Consolas", 12), fill=WHITE)

    def start(self):
        try:
            if pygame_available and bg_music_loaded:
                pygame.mixer.music.stop()
        except Exception:
            pass
        try:
            if pygame_available and LOADING_JINGLE.exists():
                pygame.mixer.music.load(str(LOADING_JINGLE)); pygame.mixer.music.set_volume(0.9); pygame.mixer.music.play()
        except Exception:
            pass
        self.start_time = time.time(); self._animate()

    def _animate(self):
        elapsed = time.time() - self.start_time
        progress = min(1.0, elapsed / self.duration)
        percent = int(progress * 100)
        self.canvas.itemconfigure(self.percent_text_id, text=f"{percent}%")
        cur_right = self.bar_left + int((self.bar_right - self.bar_left) * progress)
        self.canvas.coords(self.fill_id, self.bar_left, self.bar_top, cur_right, self.bar_bottom)
        hints = ["Sharpening your wits...", "Lighting the torches...", "Opening the ancient door..."]
        self.canvas.itemconfigure(self.hint_id, text=hints[int((elapsed*2) % len(hints))])
        if elapsed >= self.duration:
            try:
                if pygame_available and BG_MUSIC_PATH.exists():
                    pygame.mixer.music.stop(); pygame.mixer.music.load(str(BG_MUSIC_PATH)); pygame.mixer.music.set_volume(0.25); pygame.mixer.music.play(-1, fade_ms=800)
            except Exception:
                pass
            return self.destroy()
        else:
            self._after_id = self.after(33, self._animate)

    def destroy(self):
        try:
            if self._after_id: self.after_cancel(self._after_id)
        except: pass
        super().destroy()

class AdventureQuiz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Adventure Quiz")
        x = (self.winfo_screenwidth() - WIDTH)//2; y = (self.winfo_screenheight() - HEIGHT)//2
        self.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        self.resizable(False, False)

        # background tiling 
        self.bg_loaded = False
        self._bg_pil = None
        self._bg_tile_width = 0
        self._bg_tk_images = []
        self.bg_scroll_x = 0.0
        for d in SEARCH_DIRS:
            if not d.exists(): continue
            for fname in ("bg.gif","bg.png","bg.jpg"):
                cand = d / fname
                if cand.exists():
                    try:
                        if PIL_AVAILABLE:
                            pil_img = Image.open(str(cand)).convert("RGBA")
                            target_h = HEIGHT
                            aspect = pil_img.width / max(1, pil_img.height)
                            target_w = max(1,int(aspect*target_h))
                            pil_img = pil_img.resize((target_w, target_h), Image.LANCZOS)
                            self._bg_pil = pil_img; self._bg_tile_width = target_w
                            tiles_needed = (WIDTH // self._bg_tile_width) + 3
                            for _ in range(tiles_needed):
                                self._bg_tk_images.append(ImageTk.PhotoImage(self._bg_pil))
                            self.bg_loaded = True
                    except Exception as e:
                        print("BG prep fail:", e)
                    break
            if self.bg_loaded: break

        self.small_font, self.title_font, _ = pick_pixel_like_font(self)
        self.button_font = self.small_font

        self.state = "menu"
        self.scroll_offset = 0
        self.player_name = ""
        self.answer_input = ""
        self.lives = 3
        self.keys_collected = 0
        self.cursor_visible = True

        self.completed = set()
        self.unlocked = {5}
        self.auto_next_door = None  
        self._score_saved = False
        self.hero_img = None; self.hero_frames = None; self.hero_frame_durations = []; self.hero_frame_idx = 0; self.hero_is_animated = False

        if PIL_AVAILABLE and CHAR_SPRITE_PATH:
            try:
                p = Path(CHAR_SPRITE_PATH)
                if p.suffix.lower() in (".mp4", ".mov", ".avi", ".mkv", ".webm"):
                    # extract frames from video
                    frames, durations = load_video_frames(str(p), max_frames=48, target_w=220, target_h=340, frame_step=1)
                    if frames:
                        self.hero_frames = frames
                        self.hero_frame_durations = durations or [100]*len(frames)
                        self.hero_img = self.hero_frames[0]
                        self.hero_is_animated = len(self.hero_frames) > 1
                else:
                    img = Image.open(str(p))
                    frames=[]; durations=[]
                    try:
                        iterator = ImageSequence.Iterator(img)
                        for f in iterator:
                            fr = f.convert("RGBA").copy(); frames.append(fr); durations.append(int(f.info.get("duration",100)))
                    except Exception:
                        frames=[img.convert("RGBA")]; durations=[100]
                    if len(frames)==0:
                        frames=[img.convert("RGBA")]; durations=[100]
                    self.hero_frames = frames; self.hero_frame_durations = durations; self.hero_img = self.hero_frames[0]; self.hero_is_animated = len(self.hero_frames)>1
            except Exception as e:
                print("Hero image/video load failed:", e)

        if self.hero_is_animated:
            self._schedule_hero_frame()

        self.door_closed_img = None
        if PIL_AVAILABLE and DOOR_CLOSED_PATH:
            try: self.door_closed_img = Image.open(str(DOOR_CLOSED_PATH)).convert("RGBA")
            except Exception: self.door_closed_img = None
        self.door_open_img = None
        if PIL_AVAILABLE and DOOR_OPEN_PATH:
            try: self.door_open_img = Image.open(str(DOOR_OPEN_PATH)).convert("RGBA")
            except Exception: self.door_open_img = None

        # medals
        self._medal_pils = {}
        try:
            if PIL_AVAILABLE and GOLD_MEDAL_PATH.exists():
                pil = Image.open(str(GOLD_MEDAL_PATH))
                pil = make_transparent(pil, white_thresh=240)
                self._medal_pils["gold"] = pil
        except Exception:
            self._medal_pils["gold"] = None

        try:
            if PIL_AVAILABLE and SILVER_MEDAL_PATH.exists():
                pil = Image.open(str(SILVER_MEDAL_PATH))
                pil = make_transparent(pil, white_thresh=240)
                self._medal_pils["silver"] = pil
        except Exception:
            self._medal_pils["silver"] = None

        try:
            if PIL_AVAILABLE and BRONZE_MEDAL_PATH.exists():
                pil = Image.open(str(BRONZE_MEDAL_PATH))
                pil = make_transparent(pil, white_thresh=240)
                self._medal_pils["bronze"] = pil
        except Exception:
            self._medal_pils["bronze"] = None

        for k in ("gold", "silver", "bronze"):
            pil = self._medal_pils.get(k)

            if pil is None:
                print(f"[init] medal {k} pil missing")
            else:
                try:
                    print(f"[init] medal {k} loaded size={pil.size} mode={pil.mode}")
                except Exception:
                    print(f"[init] medal {k} loaded (couldn't read size)")

        # preloaded help images
        self._cry_pil = None
        self._happy_pil = None
        try:
            if PIL_AVAILABLE and IMG_S_CRY:
                self._cry_pil = Image.open(str(IMG_S_CRY)).convert("RGBA")
        except Exception:
            pass

        try:
            if PIL_AVAILABLE and IMG_S_HAPPY:
                self._happy_pil = Image.open(str(IMG_S_HAPPY)).convert("RGBA")
        except Exception:
            pass

        # Animated cry_boy GIF
        self.cry_frames = []
        self.cry_durations = []
        self.cry_frame_index = 0
        try:
            if PIL_AVAILABLE and IMG_S_CRY:
                self.cry_frames, self.cry_durations = load_gif_frames(str(IMG_S_CRY))
        except Exception as e:
            print("Failed loading cry gif:", e)

        # Animated happy_boy GIF
        self.happy_frames = []
        self.happy_durations = []
        self.happy_frame_index = 0
        try:
            if PIL_AVAILABLE and IMG_S_HAPPY:
                self.happy_frames, self.happy_durations = load_gif_frames(str(IMG_S_HAPPY))
        except Exception as e:
            print("Failed loading happy gif:", e)

        # animate gifs loop
        def animate_gifs():
            # advance cry
            try:
                if self.cry_frames:
                    self.cry_frame_index = (self.cry_frame_index + 1) % len(self.cry_frames)
                    cry_delay = self.cry_durations[self.cry_frame_index] if self.cry_durations and len(self.cry_durations) > 0 else 80
                else:
                    cry_delay = 120
            except Exception:
                cry_delay = 120
            # advance happy
            try:
                if self.happy_frames:
                    self.happy_frame_index = (self.happy_frame_index + 1) % len(self.happy_frames)
                    happy_delay = self.happy_durations[self.happy_frame_index] if self.happy_durations and len(self.happy_durations) > 0 else 80
                else:
                    happy_delay = 120
            except Exception:
                happy_delay = 120
            next_delay = min(max(20, cry_delay), max(20, happy_delay))
            try:
                self.after(next_delay, animate_gifs)
            except Exception:
                pass
        animate_gifs()

        # end
        self.ending_frames = []
        self.ending_durations = []
        self.ending_frame_index = 0
        try:
            if PIL_AVAILABLE and ENDING_GIF_PATH.exists():
                self.ending_frames, self.ending_durations = load_gif_frames(str(ENDING_GIF_PATH))
        except Exception as e:
            print("Failed loading ending gif:", e)

        def animate_ending():
            try:
                if self.ending_frames:
                    self.ending_frame_index = (self.ending_frame_index + 1) % len(self.ending_frames)
                    dur = self.ending_durations[self.ending_frame_index] if self.ending_durations else 80
                    self.after(max(20, dur), animate_ending)
                else:
                    self.after(250, animate_ending)
            except Exception as e:
                print("animate_ending error:", e)
                try:
                    self.after(250, animate_ending)
                except Exception:
                    pass
        animate_ending()

        self._img_cache = {}
        self._tk_image_cache = {}
        self._medal_tks = {}


    # Hero size 
        self.hero_w, self.hero_h = 180, 280
        self.hero_x = WIDTH - 200
        self.hero_y = HEIGHT - 180
        self.hero_speed = 6      
        self._walk_delay = 24    
        self.animating = False; self.anim_target_door = None; self.door_opening = None; self.door_geo = {}

        # visibility & fade
        self.hero_visible = False
        self.hero_opacity = 0.0
        self.hero_fade_steps = 6    
        self.hero_w, self.hero_h = 180, 280


        # canvas and input
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()
             
        try:
            panel_w = WIDTH - 2 * PANEL_MARGIN
            panel_h = HEIGHT - 2 * PANEL_MARGIN

            self._door_bg_tk = None

            if DOOR_BG_PATH and DOOR_BG_PATH.exists():

                try:
                    tkimg = self._get_tk_image_for_panel(DOOR_BG_PATH, panel_w, panel_h)
                    if tkimg:
                        self._door_bg_tk = tkimg
                except Exception as e:
                    print("preload: _get_tk_image_for_panel failed:", e)

                if self._door_bg_tk is None and PIL_AVAILABLE:
                    try:
                        pil_bg = safe_load_image(
                            DOOR_BG_PATH,
                            target_w=panel_w,
                            target_h=panel_h
                        )
                        if pil_bg:
                            try:
                                self._door_bg_tk = ImageTk.PhotoImage(pil_bg)
                            except Exception as e:
                                print("preload: ImageTk.PhotoImage failed:", e)
                    except Exception as e:
                        print("preload: safe_load_image failed:", e)

                if self._door_bg_tk is None:
                    try:
                        tkimg2 = tk.PhotoImage(file=str(DOOR_BG_PATH))
                        self._door_bg_tk = tkimg2
                    except Exception as e:
                        print("preload: tk.PhotoImage fallback failed:", e)

                if self._door_bg_tk is None:
                    print("preload: could not create PhotoImage for", DOOR_BG_PATH)
                else:
                    setattr(self, "_door_bg_tk", self._door_bg_tk)

            else:
                print("preload: DOOR_BG_PATH missing:", DOOR_BG_PATH)

        except Exception as e:
            print("preload door bg error:", e)


        self.bind("<Key>", self.on_key)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        self.bind_all("<MouseWheel>", self.on_mousewheel_windows)
        self.bind_all("<Button-4>", self.on_mousewheel_linux); self.bind_all("<Button-5>", self.on_mousewheel_linux)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.mouse_x = -9999; self.mouse_y = -9999

        self.click_areas = {}
        self.story_text = ""


        # prologue
        self.prologue_scenes = []; self.scene_index = 0; self.scene_text_full = ""; self.scene_text_shown = ""; self.scene_char_idx = 0; self.scene_done = False; self._type_after_id = None
        self.help_choice_visible = False; self.help_happy_shown = False
        self.help_text_full = ""; self.help_text_shown = ""; self.help_char_idx = 0; self.help_done = False; self._help_after_id = None

        self._last_time = time.time()
        self._tick(); self.redraw(); self._blink_loop()

        
        self._door_bg_path = DOOR_BG_PATH if DOOR_BG_PATH.exists() else None
        

    def _schedule_hero_frame(self):
        if not self.hero_is_animated or not self.hero_frames: return
        dur = 100
        try: dur = int(self.hero_frame_durations[self.hero_frame_idx])
        except Exception: dur = 100
        self.after(max(40,dur), self._advance_hero_frame)

    def _advance_hero_frame(self):
        if not self.hero_is_animated or not self.hero_frames: return
        self.hero_frame_idx = (self.hero_frame_idx + 1) % len(self.hero_frames)
        self.hero_img = self.hero_frames[self.hero_frame_idx]
        keys_to_remove = [k for k in self._img_cache.keys() if isinstance(k, tuple) and k[0] in ("hero","hero_resized")]
        for k in keys_to_remove:
            try: del self._img_cache[k]
            except: pass
        tk_keys = [k for k in self._tk_image_cache.keys() if str(k).find("hero")!=-1]
        for k in tk_keys:
            try: del self._tk_image_cache[k]
            except: pass
        self._schedule_hero_frame()

    def _get_resized_photo(self, pil_img, key_id, w, h):
        if pil_img is None: return None
        ck = (key_id, int(w), int(h))
        if ck in self._img_cache: return self._img_cache[ck]
        try:
            resized = pil_img.resize((int(w), int(h)), Image.LANCZOS)
            tkimg = ImageTk.PhotoImage(resized); self._img_cache[ck] = tkimg; return tkimg
        except Exception as e:
            print("resize fail:", e); return None

    def _get_tk_image_for_panel(self, path, w, h):
        key = (str(path), int(w), int(h))
        if key in self._tk_image_cache: return self._tk_image_cache[key]
        if PIL_AVAILABLE:
            pil = safe_load_image(Path(path), target_w=w, target_h=h)
            if pil is not None:
                try:
                    tkimg = ImageTk.PhotoImage(pil); self._tk_image_cache[key] = tkimg; return tkimg
                except Exception as e:
                    print("_get_tk_image_for_panel: ImageTk failed:", e)
        try:
            p = Path(path)
            if p.exists():
                try:
                    tkimg = tk.PhotoImage(file=str(p)); self._tk_image_cache[key] = tkimg; return tkimg
                except Exception as e:
                    print("_get_tk_image_for_panel: tk.PhotoImage failed:", e)
        except Exception as e:
            print("_get_tk_image_for_panel fallback error:", e)
        return None

    # drawing helpers
    def draw_mc_button(self, text, x, y, w, h, tag):
        mx, my = getattr(self, "mouse_x", -9999), getattr(self, "mouse_y", -9999)
        hovered = (x <= mx <= x + w) and (y <= my <= y + h)
        border_color = DARK_ORANGE if hovered else BORDER
        inner_fill = BLACK
        text_color = HOVER_YELLOW if hovered else WHITE
        self.canvas.create_rectangle(x-4, y-4, x+w+4, y+h+4, fill=border_color, outline=border_color)
        self.canvas.create_rectangle(x, y, x+w, y+h, fill=inner_fill, outline=WHITE, width=2)
        max_w = w - 20
        lines = wrap_text_to_lines(self.small_font, text or "", max_w)
        total_h = len(lines) * (self.small_font.metrics("linespace") + 4)
        start_y = y + (h - total_h) // 2
        for i, ln in enumerate(lines):
            self.canvas.create_text(x + w//2, start_y + i*(self.small_font.metrics("linespace")+4), text=ln, font=self.small_font, fill=text_color)
        self.click_areas[tag] = (x, y, x + w, y + h)

    def _update_bg_offset(self, dt):
        if not self.bg_loaded or self._bg_tile_width == 0: return
        delta = BG_SCROLL_SPEED * (dt * 60.0)
        self.bg_scroll_x = (self.bg_scroll_x + (delta if BG_SCROLL_DIRECTION=="left" else -delta)) % float(self._bg_tile_width)

    def _draw_background(self):
        if not self.bg_loaded:
            self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#202830", outline=""); return
        offset = self.bg_scroll_x; tw = self._bg_tile_width; x = -offset - tw; tile_idx = 0
        while x < WIDTH + tw:
            img = self._bg_tk_images[tile_idx % len(self._bg_tk_images)]
            self.canvas.create_image(int(x), 0, image=img, anchor="nw")
            x += tw; tile_idx += 1

    def _tick(self):
        now = time.time(); dt = now - getattr(self, "_last_time", now); self._last_time = now
        self._update_bg_offset(dt); self.after(16, self._tick)

    def clear(self):
        self.canvas.delete("all"); self.click_areas = {}

    def draw_button(self, text, y, tag, x=None, w=BUTTON_W, h=BUTTON_H):
        """
        Draw a nicely padded button and register click area.
        Center text exactly in the button and shrink font if necessary to avoid overflow.
        """
        if x is None:
            x = WIDTH // 2 - w // 2

        mx, my = getattr(self, "mouse_x", -9999), getattr(self, "mouse_y", -9999)
        hovered = (x <= mx <= x + w) and (y <= my <= y + h)
        border_color = DARK_ORANGE if hovered else BORDER
        inner_fill = BLACK
        text_color = HOVER_YELLOW if hovered else ORANGE

        # draw button rectangles
        self.canvas.create_rectangle(x-3, y-3, x+w+3, y+h+3, fill=border_color, outline=border_color)
        self.canvas.create_rectangle(x, y, x+w, y+h, fill=inner_fill, outline=inner_fill)

        # determine font size
        try:
            base_family = self.button_font.cget("family")
            base_size = max(12, int(self.button_font.cget("size")))
            btn_font = tkfont.Font(family=base_family, size=base_size)
        except Exception:
            btn_font = self.small_font

        # shrink font 
        text_w = btn_font.measure(text)
        padding = 28 
        if text_w + padding > w:
            ratio = (w - padding) / max(1, text_w)
            new_size = max(9, int(max(8, btn_font.cget("size")) * ratio))
            btn_font = tkfont.Font(family=btn_font.cget("family"), size=new_size)

        # draw text
        self.canvas.create_text(x + w//2, y + h//2, text=text, fill=text_color, font=btn_font, anchor="center")

        # click area
        self.click_areas[tag] = (x, y, x + w, y + h)


    def draw_boxed_text(self, title, content, offset_pixels):
        box_x, box_y, box_w, box_h = 100, 100, WIDTH-200, HEIGHT-200
        inner_x = box_x + 20; inner_w = box_w - 40; inner_top = box_y + 80; inner_h = box_h - 140
        self.canvas.create_rectangle(box_x-6, box_y-6, box_x+box_w+6, box_y+box_h+6, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(box_x, box_y, box_x+box_w, box_y+box_h, fill=BLACK, outline=BLACK)
        self.canvas.create_text(WIDTH//2, box_y+40, text=title, font=self.title_font, fill=ORANGE)
        lines = wrap_text_to_lines(self.small_font, content, inner_w - 40)
        line_height = self.small_font.metrics("linespace") + 6
        max_scroll = max(0, len(lines) * line_height - inner_h)
        offset_pixels = max(-max_scroll, min(0, offset_pixels)); self.scroll_offset = offset_pixels
        first_line_idx = max(0, int(-offset_pixels // line_height)); intra_pixel_offset = int(-offset_pixels % line_height)
        yy = inner_top - intra_pixel_offset; idx = first_line_idx
        while yy < inner_top + inner_h and idx < len(lines):
            self.canvas.create_text(inner_x+20, yy, anchor="nw", text=lines[idx], font=self.small_font, fill=WHITE)
            yy += line_height; idx += 1
        self.draw_button("BACK TO MENU", HEIGHT-120, "back_to_menu", w=300, h=60)

    # Menu
    def draw_menu(self):
        box_w, box_h = 900, 120; box_x, box_y = WIDTH//2 - box_w//2, 60
        self.canvas.create_rectangle(box_x-6, box_y-6, box_x+box_w+6, box_y+box_h+6, fill=BORDER)
        self.canvas.create_rectangle(box_x, box_y, box_x+box_w, box_y+box_h, fill=BLACK)
        self.canvas.create_text(WIDTH//2, box_y+box_h//2, text="PYTHON ADVENTURE QUIZ", font=self.title_font, fill=ORANGE)
        self.draw_button("PLAY", 270, "play"); self.draw_button("INSTRUCTIONS", 370, "instructions")
        self.draw_button("LEADERBOARDS", 470, "leaderboards"); self.draw_button("ABOUT US", 570, "about")

    def draw_enter_name(self):
        box_w, box_h = 800, 198; LIFT_UP = 40
        box_x, box_y = WIDTH//2 - box_w//2, HEIGHT//2 - box_h//2 - LIFT_UP
        # outer frame
        self.canvas.create_rectangle(box_x-6, box_y-6, box_x+box_w+6, box_y+box_h+6, fill=BORDER)
        self.canvas.create_rectangle(box_x, box_y, box_x+box_w, box_y+box_h, fill=BLACK)
        self.canvas.create_text(WIDTH//2, box_y+40, text="ENTER YOUR NAME", font=self.title_font, fill=ORANGE)

        # input box 
        input_box = (box_x+20, box_y+80, box_x+box_w-20, box_y+120)
        self.canvas.create_rectangle(*input_box, outline=WHITE)
        padding_x = 10
        available_width = (input_box[2] - input_box[0]) - (padding_x * 2)
        current_text = self.player_name
        if self.small_font.measure(current_text) > available_width:
            while current_text and self.small_font.measure(current_text) > available_width:
                current_text = current_text[1:]
        self.canvas.create_text(input_box[0] + padding_x, input_box[1] + 8, text=current_text, anchor="nw", fill=WHITE, font=self.small_font)

        # cursor
        if self.cursor_visible:
            cursor_x = input_box[0] + padding_x + self.small_font.measure(current_text)
            if cursor_x < input_box[2] - padding_x:
                self.canvas.create_line(cursor_x, input_box[1] + 4, cursor_x, input_box[3] - 4, fill=WHITE, width=2)

        # SUBMIT button
        submit_w, submit_h = 155, 48
        submit_x = box_x + (box_w - submit_w)//2
        submit_y = box_y + 130
        self.draw_button("SUBMIT", submit_y, "submit_name", x=submit_x, w=submit_w, h=submit_h)

        # BACK button 
        BACK_GAP = 28
        back_w, back_h = 300, 60
        back_x = box_x + (box_w - back_w) // 2
        back_y = box_x + box_h + BACK_GAP  
        # ensure back button fits on screen
        if back_y + back_h > HEIGHT - 8:
            back_y = HEIGHT - back_h - 12
        self.draw_button("BACK TO MENU", back_y, "back_to_menu", x=back_x, w=back_w, h=back_h)

        # store for input handling
        self._enter_name_input_box = input_box
        self._enter_name_available_width = available_width
        self._enter_name_padding_x = padding_x

    # Prologue
    def start_prologue(self, player_name):
        self.player_name = player_name.strip() if player_name.strip() else "Arthan"
        self.prologue_scenes = []
        for imgpath, text in PROLOGUE_SCENES_TEMPLATE:
            text_sub = text.replace("{name}", self.player_name)
            self.prologue_scenes.append({'img': imgpath, 'text': text_sub})
        self.scene_index = 0; self.scene_char_idx = 0
        self.scene_text_full = self.prologue_scenes[0]['text'] if self.prologue_scenes else ""
        self.scene_text_shown = ""
        self.scene_done = (len(self.scene_text_full) == 0); self.state = "prologue"
        self.help_choice_visible = False; self.help_happy_shown = False
        self.help_text_full = ""; self.help_text_shown = ""; self.help_char_idx = 0; self.help_done = False
        self._score_saved = False
        try:
            if pygame_available:
                try: pygame.mixer.music.fadeout(600)
                except Exception: pass
                if STORY_MUSIC_PATH.exists():
                    pygame.mixer.music.load(str(STORY_MUSIC_PATH)); pygame.mixer.music.set_volume(0.38); pygame.mixer.music.play(-1, fade_ms=800)
        except Exception as e:
            print("Failed to switch to story music:", e)
        panel_w, panel_h = WIDTH - 2*PANEL_MARGIN, HEIGHT - 2*PANEL_MARGIN
        for s in self.prologue_scenes:
            try: self._get_tk_image_for_panel(s['img'], panel_w, panel_h)
            except Exception as e: print("preload image failed for", s['img'], e)
        if not self.scene_done and self.scene_text_full:
            self._schedule_type_step(0)

    def _schedule_type_step(self, delay_ms):
        if self._type_after_id:
            try: self.after_cancel(self._type_after_id)
            except Exception: pass
        self._type_after_id = self.after(delay_ms, self._typewriter_step)

    def _typewriter_step(self):
        self._type_after_id = None
        if self.state != "prologue": return
        text = self.scene_text_full
        if self.scene_char_idx >= len(text):
            self.scene_done = True
            if pygame_available and story_typing:
                try: story_typing.stop()
                except Exception: pass
            return
        ch = text[self.scene_char_idx]; self.scene_text_shown += ch; self.scene_char_idx += 1
        if ch.strip() and pygame_available:
            try:
                if story_typing:
                    story_typing.stop(); story_typing.play()
                elif typing_sound:
                    typing_sound.stop(); typing_sound.play()
            except Exception:
                pass
        delay = CHAR_DELAY
        if ch in ".!?": delay = PUNCT_DELAY
        elif ch == "\n": delay = NEWLINE_DELAY
        self._schedule_type_step(delay)

    def _advance_scene(self):
        if self.scene_index + 1 >= len(self.prologue_scenes):
            if pygame_available:
                try:
                    pygame.mixer.music.fadeout(800); self.after(850, self._restore_bg_music)
                except Exception:
                    self._restore_bg_music()
            self.state = "help_choice"; self.help_choice_visible = True
            try: self.start_help_typing()
            except Exception: pass
            return
        self.scene_index += 1; self.scene_char_idx = 0
        self.scene_text_full = self.prologue_scenes[self.scene_index]['text']; self.scene_text_shown = ""
        self.scene_done = (len(self.scene_text_full) == 0)
        if not self.scene_done and self.scene_text_full:
            self._schedule_type_step(200)
        else:
            self.scene_done = True

    def _restore_bg_music(self):
        if pygame_available:
            try:
                if BG_MUSIC_PATH.exists():
                    pygame.mixer.music.stop(); pygame.mixer.music.load(str(BG_MUSIC_PATH)); pygame.mixer.music.set_volume(0.25); pygame.mixer.music.play(-1, fade_ms=800)
            except Exception:
                pass

    def draw_prologue(self):
        panel_x, panel_y = PANEL_MARGIN, PANEL_MARGIN
        panel_w, panel_h = WIDTH - 2*PANEL_MARGIN, HEIGHT - 2*PANEL_MARGIN
        self.canvas.create_rectangle(panel_x, panel_y, panel_x+panel_w, panel_y+panel_h, fill=BLACK, outline=BORDER, width=6)
        if not self.prologue_scenes: return
        cur = self.prologue_scenes[self.scene_index]; img_path = cur['img']
        tkimg = self._get_tk_image_for_panel(img_path, panel_w, panel_h)
        if tkimg:
            try: self.canvas.create_image(panel_x, panel_y, image=tkimg, anchor="nw")
            except Exception as e:
                print("draw_prologue create_image failed:", e); self.canvas.create_rectangle(panel_x, panel_y, panel_x+panel_w, panel_y+panel_h, fill="#001020")
        else:
            self.canvas.create_rectangle(panel_x, panel_y, panel_x+panel_w, panel_y+panel_h, fill="#001020")
            debug_msg = "[no image]" if img_path is None else f"[missing: {str(img_path)}]"
            self.canvas.create_text(panel_x + 40, panel_y + 40, anchor="nw", text=debug_msg, font=self.small_font, fill=HOVER_YELLOW)
        skip_text = "skip >>"; skip_w = self.small_font.measure(skip_text)
        skip_x = panel_x + panel_w - skip_w - 40; skip_y = panel_y + 30
        self.canvas.create_text(skip_x, skip_y, anchor="nw", text=skip_text, font=self.small_font, fill=HOVER_YELLOW)
        self.click_areas["prologue_skip"] = (skip_x - 6, skip_y - 6, skip_x + skip_w + 6, skip_y + 26)

        text_pad_x = 80; text_pad_y = panel_y + panel_h - 180; max_text_w = panel_w - text_pad_x*2
        lines = wrap_text_to_lines(self.small_font, self.scene_text_shown, max_text_w)
        line_h = self.small_font.metrics("linespace") + 8
        visible_lines = max(1, min(6, (180 // line_h)))
        for i, ln in enumerate(lines[-visible_lines:]):
            tx = panel_x + text_pad_x; ty = text_pad_y + i*line_h
            self.canvas.create_text(tx+2, ty+2, anchor="nw", text=ln, font=self.small_font, fill="#000000")
            self.canvas.create_text(tx, ty, anchor="nw", text=ln, font=self.small_font, fill=WHITE)

        cont_text = ">> continue" if self.scene_done else "..."
        cont_w = self.small_font.measure(cont_text)
        cont_x = panel_x + panel_w - cont_w - 60; cont_y = panel_y + panel_h - 60
        cont_color = HOVER_YELLOW if self.scene_done else "#444"
        self.canvas.create_text(cont_x, cont_y, anchor="nw", text=cont_text, font=self.small_font, fill=cont_color)
        if self.scene_done:
            line_h = self.small_font.metrics("linespace") + 8
            self.click_areas["prologue_continue"] = (cont_x - 8, cont_y - 4, cont_x + cont_w + 8, cont_y + line_h + 4)
        else:
            if "prologue_continue" in self.click_areas:
                del self.click_areas["prologue_continue"]

    def start_help_typing(self, player=None):
        player = player or self.player_name or "(name)"
        self.help_text_full = (
            f"\"H-hello...? Are you really here?\nPlease... I need someone...\nAre you the one named {player}?\n\n"
            f"I’ve been stuck inside this place for so long.\nMy keys are lost somewhere in the Python code,\nand the door won’t open without them...\nCan you... help me?\""
        )
        self.help_text_shown = ""
        self.help_char_idx = 0
        self.help_done = False
        self._schedule_help_type_step(0)

    def start_help_happy(self, player=None):
        player = player or self.player_name or "(name)"
        self.help_text_full = (
            f"Y-you’re willing to help me, {player}?\nThank you! Really, thank you!\nI don’t feel alone anymore.\n\n"
            f"With your help, I know we can solve\nevery challenge inside this world.\nLet’s unlock that door together!"
        )
        self.help_text_shown = ""; self.help_char_idx = 0; self.help_done = False
        self._schedule_help_type_step(0)

    def _schedule_help_type_step(self, delay_ms):
        if getattr(self, "_help_after_id", None):
            try: self.after_cancel(self._help_after_id)
            except Exception: pass
        self._help_after_id = self.after(delay_ms, self._help_type_step)

    def _help_type_step(self):
        self._help_after_id = None
        if self.state not in ("help_choice", "help_happy"): return
        text = getattr(self, "help_text_full", "")
        if self.help_char_idx >= len(text):
            self.help_done = True
            if pygame_available and story_typing:
                try: story_typing.stop()
                except Exception: pass
            return
        ch = text[self.help_char_idx]; self.help_text_shown += ch; self.help_char_idx += 1
        if ch.strip() and pygame_available:
            try:
                if story_typing:
                    story_typing.stop(); story_typing.play()
                elif typing_sound:
                    typing_sound.stop(); typing_sound.play()
            except Exception:
                pass
        delay = CHAR_DELAY
        if ch in ".!?": delay = PUNCT_DELAY
        elif ch == "\n": delay = NEWLINE_DELAY
        self._schedule_help_type_step(delay)

    def draw_help_choice(self):
        MARGIN, BORDER_W = 8, 6; PAD = 20; GAP_BETWEEN = 60
        panel_x, panel_y = MARGIN, MARGIN; panel_w, panel_h = WIDTH - 2*MARGIN, HEIGHT - 2*MARGIN
        center_y = panel_y + panel_h // 2
        self.canvas.create_rectangle(panel_x, panel_y, panel_x + panel_w, panel_y + panel_h, fill=BLACK, outline=BORDER, width=BORDER_W)
        char_box_w, char_box_h = 300, 360; char_x = panel_x + PAD + 12; char_y = center_y - (char_box_h // 2)
        self.canvas.create_rectangle(char_x - 6, char_y - 6, char_x + char_box_w + 6, char_y + char_box_h + 6, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(char_x, char_y, char_x + char_box_w, char_y + char_box_h, fill=WHITE, outline=ORANGE, width=3)

        # animated cry image
        if PIL_AVAILABLE and getattr(self, "cry_frames", None):
            try:
                frame = self.cry_frames[self.cry_frame_index]
                max_w, max_h = char_box_w - 24, char_box_h - 24
                iw, ih = frame.size
                if iw <= 0 or ih <= 0: iw, ih = 1, 1
                scale = min(max_w / iw, max_h / ih)
                nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
                resized = frame.resize((nw, nh), Image.LANCZOS)
                self._cry_tk = ImageTk.PhotoImage(resized)
                cx = char_x + char_box_w // 2; cy = char_y + char_box_h // 2
                self.canvas.create_image(cx, cy, image=self._cry_tk, anchor="center")
            except Exception:
                try:
                    if getattr(self, "_cry_pil", None):
                        self._cry_tk = self._get_resized_photo(self._cry_pil, "cry_resized", char_box_w - 24, char_box_h - 24)
                        if getattr(self, "_cry_tk", None):
                            cx = char_x + char_box_w // 2; cy = char_y + char_box_h // 2
                            self.canvas.create_image(cx, cy, image=self._cry_tk, anchor="center")
                except Exception:
                    pass
        elif getattr(self, "_cry_pil", None):
            try:
                max_w, max_h = char_box_w - 24, char_box_h - 24; iw, ih = self._cry_pil.size; iw, ih = (iw or 1, ih or 1)
                scale = min(max_w / iw, max_h / ih); nw, nh = max(1,int(iw*scale)), max(1,int(ih*scale))
                self._cry_tk = self._get_resized_photo(self._cry_pil, "cry_resized", nw, nh)
                if getattr(self, "_cry_tk", None):
                    cx = char_x + char_box_w // 2; cy = char_y + char_box_h // 2; self.canvas.create_image(cx, cy, image=self._cry_tk, anchor="center")
            except Exception:
                pass
        elif self.hero_img is not None and PIL_AVAILABLE:
            hero_tk = self._get_resized_photo(self.hero_img, "hero_small", 180, 240)
            if hero_tk: self.canvas.create_image(char_x + char_box_w//2, char_y + char_box_h // 2, image=hero_tk, anchor="center")
        else:
            self.canvas.create_text(char_x + char_box_w // 2, char_y + char_box_h // 2, text="(no sprite)", fill=ORANGE)

        # dialog panel 
        text_box_w = 880; text_box_h = 520; text_x = char_x + char_box_w + GAP_BETWEEN; text_y = center_y - (text_box_h // 2) - 10
        self.canvas.create_rectangle(text_x - 8, text_y - 8, text_x + text_box_w + 8, text_y + text_box_h + 8, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(text_x, text_y, text_x + text_box_w, text_y + text_box_h, fill=BLACK, outline=ORANGE, width=4)
        dialog_pad_x, dialog_pad_y = 40, 40; effective_width = text_box_w - (dialog_pad_x * 2)

        typed = getattr(self, "help_text_shown", None)
        if typed is None or typed == "":
            player = self.player_name or "(name)"; full_dialog = (
                f"\"H-hello...? Are you really here?\nPlease... I need someone...\nAre you the one named {player}?\n\n"
                f"I’ve been stuck inside this place for so long.\nMy keys are lost somewhere in the Python code,\nand the door won’t open without them...\nCan you... help me?\""
            )
            lines = wrap_text_to_lines(self.small_font, full_dialog, effective_width)
        else:
            lines = wrap_text_to_lines(self.small_font, typed, effective_width)

        line_h = self.small_font.metrics("linespace") + 9; max_lines_fit = max(1, (text_box_h - (dialog_pad_y * 2)) // line_h)
        lines = lines[:max_lines_fit]
        tx = text_x + dialog_pad_x; ty = text_y + dialog_pad_y
        for ln in lines:
            self.canvas.create_text(tx+2, ty+2, anchor="nw", text=ln, font=self.small_font, fill="#000000")
            self.canvas.create_text(tx, ty, anchor="nw", text=ln, font=self.small_font, fill=WHITE)
            ty += line_h

        # yes btn
        btn_w = 120; btn_h = 45
        by = text_y + text_box_h - btn_h - 13
        left_btn_x  = text_x + 80
        right_btn_x = text_x + text_box_w - btn_w - 80

        if "help_yes" in self.click_areas and not self.help_done:
            try: del self.click_areas["help_yes"]
            except: pass
            
        if getattr(self, "help_done", False):
            self.draw_button("YES", by, "help_yes", x=right_btn_x, w=btn_w, h=btn_h)

    def draw_help_happy(self):
        MARGIN, BORDER_W = 8, 6; PAD = 20; GAP_BETWEEN = 60
        panel_x, panel_y = MARGIN, MARGIN; panel_w, panel_h = WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN
        center_y = panel_y + panel_h // 2
        self.canvas.create_rectangle(panel_x, panel_y, panel_x + panel_w, panel_y + panel_h, fill=BLACK, outline=BORDER, width=BORDER_W)
        char_box_w, char_box_h = 300, 360; char_x = panel_x + PAD + 12; char_y = center_y - (char_box_h // 2)
        self.canvas.create_rectangle(char_x - 6, char_y - 6, char_x + char_box_w + 6, char_y + char_box_h + 6, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(char_x, char_y, char_x + char_box_w, char_y + char_box_h, fill=WHITE, outline=ORANGE, width=3)

        # Animated happy gif
        if PIL_AVAILABLE and getattr(self, "happy_frames", None):
            try:
                frame = self.happy_frames[self.happy_frame_index]
                max_w, max_h = char_box_w - 24, char_box_h - 24
                iw, ih = frame.size
                if iw <= 0 or ih <= 0: iw, ih = 1, 1
                scale = min(max_w / iw, max_h / ih)
                nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
                resized = frame.resize((nw, nh), Image.LANCZOS)
                self._happy_tk = ImageTk.PhotoImage(resized)
                cx = char_x + char_box_w // 2; cy = char_y + char_box_h // 2
                self.canvas.create_image(cx, cy, image=self._happy_tk, anchor="center")
            except Exception:
                # fallback 
                try:
                    if getattr(self, "_happy_pil", None):
                        self._happy_tk = self._get_resized_photo(self._happy_pil, "happy_resized", char_box_w - 24, char_box_h - 24)
                        if getattr(self, "_happy_tk", None):
                            cx = char_x + char_box_w // 2; cy = char_y + char_box_h // 2
                            self.canvas.create_image(cx, cy, image=self._happy_tk, anchor="center")
                except Exception:
                    pass
        elif getattr(self, "_happy_pil", None):
            try:
                max_w, max_h = char_box_w - 24, char_box_h - 24; iw, ih = self._happy_pil.size; iw, ih = (iw or 1, ih or 1)
                scale = min(max_w / iw, max_h / ih); nw, nh = max(1,int(iw*scale)), max(1,int(ih*scale))
                self._happy_tk = self._get_resized_photo(self._happy_pil, "happy_resized", nw, nh)
                if getattr(self, "_happy_tk", None):
                    cx = char_x + char_box_w // 2; cy = char_y + char_box_h // 2; self.canvas.create_image(cx, cy, image=self._happy_tk, anchor="center")
            except Exception:
                pass
        elif self.hero_img is not None and PIL_AVAILABLE:
            hero_tk = self._get_resized_photo(self.hero_img, "hero_small2", 180, 240)
            if hero_tk: self.canvas.create_image(char_x + char_box_w//2, char_y + char_box_h//2, image=hero_tk, anchor="center")
        else:
            self.canvas.create_text(char_x + char_box_w//2, char_y + char_box_h//2, text="(no sprite)", fill=ORANGE)

        text_box_w = 880; text_box_h = 520; text_x = char_x + char_box_w + GAP_BETWEEN; text_y = center_y - (text_box_h // 2) - 10
        self.canvas.create_rectangle(text_x - 8, text_y - 8, text_x + text_box_w + 8, text_y + text_box_h + 8, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(text_x, text_y, text_x + text_box_w, text_y + text_box_h, fill=BLACK, outline=ORANGE, width=4)
        dialog_pad_x, dialog_pad_y = 40, 40; effective_width = text_box_w - (dialog_pad_x * 2)
        # happy dialog
        typed = getattr(self, "help_text_shown", "")
        if typed is None or typed == "":
            lines = []
        else:
            lines = wrap_text_to_lines(self.small_font, typed, effective_width)
        line_h = self.small_font.metrics("linespace") + 9; max_lines_fit = max(1, (text_box_h - (dialog_pad_y * 2)) // line_h); lines = lines[:max_lines_fit]
        tx = text_x + dialog_pad_x; ty = text_y + dialog_pad_y
        for ln in lines:
            self.canvas.create_text(tx+2, ty+2, anchor="nw", text=ln, font=self.small_font, fill="#000000")
            self.canvas.create_text(tx, ty, anchor="nw", text=ln, font=self.small_font, fill=WHITE); ty += line_h

        btn_w, btn_h = 220, 64; by = text_y + text_box_h - btn_h - 28
        left_btn_x = text_x + 60; right_btn_x = text_x + text_box_w - btn_w - 60
        self.draw_button("START GAME", by, "start_game", x=left_btn_x, w=btn_w, h=btn_h)
        self.draw_button("BACK", by, "intro_back", x=right_btn_x, w=btn_w, h=btn_h)

    def draw_story_intro(self, _text_ignored):
        MARGIN, BORDER_W = 8, 6; PAD = 20; GAP_BETWEEN = 60
        panel_x, panel_y = MARGIN, MARGIN; panel_w, panel_h = WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN
        center_y = panel_y + panel_h // 2
        self.canvas.create_rectangle(panel_x, panel_y, panel_x + panel_w, panel_y + panel_h, fill=BLACK, outline=BORDER, width=BORDER_W)
        char_box_w, char_box_h = 300, 360; char_x = panel_x + PAD + 12; char_y = center_y - (char_box_h // 2)
        self.canvas.create_rectangle(char_x - 6, char_y - 6, char_x + char_box_w + 6, char_y + char_box_h + 6, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(char_x, char_y, char_x + char_box_w, char_y + char_box_h, fill=WHITE, outline=ORANGE, width=3)
        if self.hero_img is not None and PIL_AVAILABLE:
            max_w, max_h = char_box_w - 24, char_box_h - 24; iw, ih = self.hero_img.size
            if iw <= 0 or ih <= 0: iw, ih = 1, 1
            scale = min(max_w / iw, max_h / ih); nw, nh = max(1,int(iw*scale)), max(1,int(ih*scale))
            self.hero_intro_tk = self._get_resized_photo(self.hero_img, "hero_resized_intro", nw, nh)
            if getattr(self, "hero_intro_tk", None):
                cx = char_x + char_box_w // 2; cy = char_y + char_box_h // 2; self.canvas.create_image(cx, cy, image=self.hero_intro_tk, anchor="center")
        else:
            self.canvas.create_text(char_x + char_box_w//2, char_y + char_box_h//2, text="(no sprite)", fill=ORANGE)

        text_box_w = 880; text_box_h = 520; text_x = char_x + char_box_w + GAP_BETWEEN; text_y = center_y - (text_box_h // 2) - 10
        self.canvas.create_rectangle(text_x - 8, text_y - 8, text_x + text_box_w + 8, text_y + text_box_h + 8, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(text_x, text_y, text_x + text_box_w, text_y + text_box_h, fill=BLACK, outline=ORANGE, width=4)
        dialog_pad_x, dialog_pad_y = 40, 40; effective_width = text_box_w - (dialog_pad_x * 2)
        player = self.player_name or "(name)"
        dialog = (f"\"H-hello...? Are you really here?\nPlease... I need someone...\nAre you the one named {player}?\n\n"
                  f"I’ve been stuck inside this place for so long.\nMy keys are lost somewhere in the Python code,\nand the door won’t open without them...\nCan you... help me?\"")
        lines = wrap_text_to_lines(self.small_font, dialog, effective_width); line_h = self.small_font.metrics("linespace") + 9
        max_lines_fit = max(1, (text_box_h - (dialog_pad_y * 2)) // line_h); lines = lines[:max_lines_fit]
        tx = text_x + dialog_pad_x; ty = text_y + dialog_pad_y
        for ln in lines:
            self.canvas.create_text(tx+2, ty+2, anchor="nw", text=ln, font=self.small_font, fill="#000000")
            self.canvas.create_text(tx, ty, anchor="nw", text=ln, font=self.small_font, fill=WHITE); ty += line_h

        btn_w = 160; btn_h = 54; center_x = text_x + (text_box_w // 2); by = text_y + text_box_h - btn_h - 32
        self.draw_button("START  GAME", by, "start_game", x=center_x - btn_w - 30, w=btn_w, h=btn_h)
        self.draw_button("BACK", by, "intro_back", x=center_x + 30, w=btn_w, h=btn_h)

    def draw_hallway(self):
        MARGIN, BORDER_W = 8, 6
        panel_x, panel_y = MARGIN, MARGIN
        panel_w, panel_h = WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN

        try:
            if getattr(self, "_door_bg_tk", None):
                # Draw the preloaded background image
                self.canvas.create_image(
                    panel_x,
                    panel_y,
                    image=self._door_bg_tk,
                    anchor="nw"
                )
            else:
                self.canvas.create_rectangle(
                    panel_x,
                    panel_y,
                    panel_x + panel_w,
                    panel_y + panel_h,
                    fill="#000000",
                    outline=BORDER,
                    width=BORDER_W
                )
                print("draw_hallway: _door_bg_tk is missing. Background not loaded.")

        except Exception as e:
            print("draw_hallway error:", e)
            try:
                self.canvas.create_rectangle(
                    panel_x, panel_y,
                    panel_x + panel_w, panel_y + panel_h,
                    fill="#000000", outline=BORDER, width=BORDER_W
                )
            except Exception:
                pass

        # dynamic layout 
        num_doors = 5
        door_w = 180
        door_h = 360
        total_width = num_doors * door_w + (num_doors - 1) * 48 
        start_x = panel_x + max(40, (panel_w - total_width) // 2)
        dy = panel_y + 120
        self.door_geo = {}
        for i in range(num_doors):
            idx = i + 1
            x = start_x + i * (door_w + 48)
            self.door_geo[idx] = (x, dy, door_w, door_h)

        def door_img(which, completed=False, locked=False):
            x,y,w,h = self.door_geo[which]; img = None

            if PIL_AVAILABLE:
                if getattr(self, "door_opening", None) == which and self.door_open_img is not None:
                    img = self._get_resized_photo(self.door_open_img, f"opening{which}", w, h)
                elif completed and self.door_open_img is not None:
                    img = self._get_resized_photo(self.door_open_img, f"open{which}", w, h)
                elif self.door_closed_img is not None:
                    img = self._get_resized_photo(self.door_closed_img, f"closed{which}", w, h)
            if img is not None:
                self.canvas.create_image(x + w//2, y + h//2, image=img)
            else:
                self.canvas.create_rectangle(x-4, y-4, x+w+4, y+h+4, fill=BORDER, outline=BORDER)
                self.canvas.create_rectangle(x, y, x+w, y+h, fill=BLACK, outline=ORANGE, width=3)
                ax, ay = x+int(w*0.2), y+int(h*0.15); ax2, ay2 = x+int(w*0.8), y+int(h*0.85)
                self.canvas.create_arc(ax, ay, ax2, ay2, start=0, extent=180, style="arc", outline=ORANGE, width=3)

            try:
                door_label_font = tkfont.Font(family=self.small_font.cget("family"),
                                             size=max(14, int(self.small_font.cget("size")) + 0),
                                             weight="bold")
            except Exception:
                door_label_font = self.small_font

            label = f"Quiz #{which}"
            label_x = x + w // 2
            label_y = y + h // 2 - int(h * 0.55)

            if completed:
                label_color = HOVER_YELLOW
            elif locked:
                label_color = ORANGE
            else:
                label_color = WHITE


            if completed:
                self.canvas.create_text(x+w//2, y+h+24, text="COMPLETED", fill=HOVER_YELLOW, font=self.small_font)
            elif locked:
                self.canvas.create_text(x+w//2, y+h+24, text="LOCKED", fill=ORANGE, font=self.small_font)
            else:
                self.canvas.create_text(x+w//2, y+h+24, text="ENTER", fill=WHITE, font=self.small_font)
            if not locked and not self.animating:
                self.click_areas[f"door{which}"] = (x, y, x+w, y+h)


        # draw each door
        for i in range(1, 6):
            completed = (i in self.completed)
            locked = (i not in self.unlocked)
            door_img(i, completed=completed, locked=locked)
        if 1 in self.door_geo:
            x, y, w, h = self.door_geo[1]
            # hero feet aligned
            self.hero_y = y + h - (self.hero_h // 2) + 20


        # hero drawing 
        if self.hero_visible and self.hero_img is not None and PIL_AVAILABLE and self.hero_opacity > 0.0:
           
            try:
                
                panel_bottom = panel_y + panel_h
                door_bottoms = [self.door_geo[i][1] + self.door_geo[i][3] for i in self.door_geo]
                baseline_bottom = max(door_bottoms) if door_bottoms else (panel_bottom - 20)
                hero_bottom_y = min(baseline_bottom + 6, panel_bottom - 8)
            except Exception:
                hero_bottom_y = panel_y + panel_h - 8

        
            pil_with_op = self._apply_opacity(self.hero_img, self.hero_opacity)
            hero_key = f"hero_op_{int(self.hero_opacity*100)}"
            hero_w = min(self.hero_w, int(door_w * 1.05))
            hero_h = min(self.hero_h, int(door_h * 1.15))
            hero_tk = self._get_resized_photo(pil_with_op, hero_key, hero_w, hero_h)
            if hero_tk:
                self.canvas.create_image(self.hero_x, hero_bottom_y, image=hero_tk, anchor="s")
        else:
            pass


        self.draw_button("EXIT", panel_y + panel_h - 100, "exit_game", x=panel_x + panel_w - 220, w=200, h=60)

    def draw_stage(self, stage_idx, user_input):
        q = questions[stage_idx]
        self.canvas.create_rectangle(47, 47, WIDTH-47, 247, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(50, 50, WIDTH-50, 250, fill=BLACK)
        y = 70
        for line in q["story"].split("\n"):
            self.canvas.create_text(70, y, anchor="nw", text=line, fill=WHITE, font=self.small_font); y += 40
        card_top = 270; card_h = 170; card_left = 70; card_right = WIDTH - 70
        self.canvas.create_rectangle(card_left-6, card_top-6, card_right+6, card_top+card_h+6, fill=BORDER, outline=BORDER)
        self.canvas.create_rectangle(card_left, card_top, card_right, card_top+card_h, fill=BLACK, outline=ORANGE, width=4)
        qpad_x = 36; qpad_y = 20; question_text = "Question: " + q["question"]
        max_width = (card_right - card_left) - (qpad_x * 2)
        lines = wrap_text_to_lines(self.small_font, question_text, max_width)
        line_h = self.small_font.metrics("linespace") + 6; start_y = card_top + qpad_y
        for i, ln in enumerate(lines):
            self.canvas.create_text((card_left + card_right)//2, start_y + i*line_h, text=ln, font=self.small_font, fill=WHITE, anchor="n")
        opt_area_top = card_top + card_h + 24; opt_w = (WIDTH - 140 - 40) // 2; opt_h = 72; opt_gap_x = 20; opt_gap_y = 20
        left_col_x = 70; right_col_x = left_col_x + opt_w + opt_gap_x
        opts = q.get("options")
        if not opts or len(opts) < 4:
            correct = q.get("answer",""); opts = [correct,"","",""]
        positions = [
            (left_col_x, opt_area_top, opt_w, opt_h, "option1"),
            (right_col_x, opt_area_top, opt_w, opt_h, "option2"),
            (left_col_x, opt_area_top + opt_h + opt_gap_y, opt_w, opt_h, "option3"),
            (right_col_x, opt_area_top + opt_h + opt_gap_y, opt_w, opt_h, "option4"),
        ]
        for i, pos in enumerate(positions):
            x, y, w, h, tag = pos; label = opts[i] if i < len(opts) else ""
            self.draw_mc_button(label, x, y, w, h, tag)
        status = f"Lives: {'♥'*self.lives}   Keys: {'🔑'*self.keys_collected}"
        self.canvas.create_text(70, opt_area_top + opt_h*2 + opt_gap_y + 16, anchor="nw", text=status, fill=ORANGE, font=self.small_font)

    def draw_ending(self):
        """
        GAME OVER screen showing only the animated fullscreen GIF
        and two buttons at the bottom.

        - If player collected all keys -> left: EXIT, right: DONE (DONE uses existing 'back_to_menu' tag).
        - Otherwise -> left: PLAY AGAIN, right: EXIT (same as before).
        """
       # animated full screen gif
        try:
            if self.ending_frames:
                frame = self.ending_frames[self.ending_frame_index]
                iw, ih = frame.size

                scale = max(WIDTH / max(1, iw), HEIGHT / max(1, ih))
                new_w = int(iw * scale)
                new_h = int(ih * scale)

                resized = frame.resize((new_w, new_h), Image.LANCZOS)

                left = max(0, (new_w - WIDTH) // 2)
                top = max(0, (new_h - HEIGHT) // 2)
                cropped = resized.crop((left, top, left + WIDTH, top + HEIGHT))

                self._ending_tk = ImageTk.PhotoImage(cropped)
                self.canvas.create_image(0, 0, image=self._ending_tk, anchor="nw")
            else:
                self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black")
        except Exception:
            self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black")

        # buttond
        btn_w = 200
        btn_h = 60
        btn_y = HEIGHT - btn_h - 40  
        left_margin = 80
        right_margin = 80

        # player collecter keys
        total_keys_needed = len(questions)
        has_all_keys = (getattr(self, "keys_collected", 0) >= total_keys_needed) or (len(self.completed) >= total_keys_needed)

        if has_all_keys:
            left_x = left_margin
            right_x = WIDTH - btn_w - right_margin
            self.draw_button("EXIT", btn_y, "exit_game", x=left_x, w=btn_w, h=btn_h)
            self.draw_button("PLAY AGAIN", btn_y, "back_to_menu", x=right_x, w=btn_w, h=btn_h)
        else:
            
            total_buttons_w = btn_w * 2 + 60 
            start_x = (WIDTH - total_buttons_w) // 2
            gap = 60
            self.draw_button("PLAY AGAIN", btn_y, "play_again", x=start_x, w=btn_w, h=btn_h)
            self.draw_button("EXIT", btn_y, "exit_game", x=start_x + btn_w + gap, w=btn_w, h=btn_h)



    def draw_leaderboards(self):
        box_x, box_y, box_w, box_h = 80, 60, WIDTH - 160, HEIGHT - 140
        self.canvas.create_rectangle(box_x-6, box_y-6, box_x+box_w+6, box_y+box_h+6, fill=BORDER)
        self.canvas.create_rectangle(box_x, box_y, box_x+box_w, box_y+box_h, fill=BLACK)
        self.canvas.create_text(WIDTH//2, box_y+40, text="LEADERBOARDS", font=self.title_font, fill=ORANGE)

        header_font = tkfont.Font(family=self.small_font.cget("family"),
                                  size=max(18, int(self.small_font.cget("size")) + 2),
                                  weight="bold")
        body_font = tkfont.Font(family=self.small_font.cget("family"),
                                size=self.small_font.cget("size"))

        entries = load_leaderboard() or []

       
        entries = sorted(entries, key=lambda e: (-int(e.get("score", 0)), e.get("ts", "")))

        # ranks
        ranks = []
        prev_score = None
        prev_rank = 0
        for e in entries:
            sc = int(e.get("score", 0))
            if prev_score is None:
                rank = 1
            elif sc == prev_score:
                rank = prev_rank
            else:
                rank = prev_rank + 1
            ranks.append(rank)
            prev_score = sc
            prev_rank = rank

        # combine entries with ranks
        ranked_entries = []
        for e, r in zip(entries, ranks):
            e_copy = dict(e)
            e_copy["_rank"] = r
            ranked_entries.append(e_copy)

        # Only show top N rows 
        TOP_N = 10
        visible = ranked_entries[:TOP_N]

        headers = ["#", "Name", "Lives", "Keys"]
        header_y = box_y + 100

        left_margin = box_x + 36
        right_margin = box_x + box_w - 36
        line_h = body_font.metrics("linespace") + 10

        # measure column widths dynamically
        rank_w = max(header_font.measure("#"), body_font.measure("999.")) + 12
        # approximate numeric columns width
        keys_w = max(header_font.measure("Keys"), max((body_font.measure(str(e.get("keys",0))) for e in visible), default=body_font.measure("0"))) + 18
        lives_w = max(header_font.measure("Lives"), max((body_font.measure(str(e.get("lives",0))) for e in visible), default=body_font.measure("0"))) + 18

        # gap between numeric columns and name area
        gap_between_numeric = 120
        numeric_total = keys_w + lives_w + gap_between_numeric

        # available width for name column 
        available_for_name = (box_x + box_w - 40) - (left_margin + rank_w + numeric_total)
        min_name_space = 120
        allowed_name_w = max(min_name_space, available_for_name)

        # compute X positions
        rank_x = left_margin
        name_x = rank_x + rank_w + 180
        keys_right = box_x + box_w - 100
        lives_right = keys_right - keys_w - (gap_between_numeric // 1)

        # draw headers
        self.canvas.create_text(rank_x, header_y, anchor="w", text=headers[0], font=header_font, fill=HOVER_YELLOW)
        self.canvas.create_text(name_x, header_y, anchor="w", text=headers[1], font=header_font, fill=HOVER_YELLOW)
        self.canvas.create_text(keys_right, header_y, anchor="e", text=headers[3], font=header_font, fill=HOVER_YELLOW)
        self.canvas.create_text(lives_right, header_y, anchor="e", text=headers[2], font=header_font, fill=HOVER_YELLOW)

        # ordinal helper
        def ordinal(n):
            if 10 <= (n % 100) <= 20:
                suf = "th"
            else:
                suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
            return f"{n}{suf}"

        # draw visible rows
        start_y = header_y + 36
        for i, e in enumerate(visible):
            y = start_y + i * line_h
            rank_num = e.get("_rank", i+1)
            rank_text = ordinal(rank_num)
            raw_name = e.get("name", "Unknown")
            keys_text = str(e.get("keys", 0))
            lives_text = str(e.get("lives", 0))

            # truncate name to allowed width
            name_disp = raw_name
            if body_font.measure(name_disp) > allowed_name_w:
                while name_disp and body_font.measure(name_disp + "...") > allowed_name_w:
                    name_disp = name_disp[:-1]
                name_disp = name_disp + "..."

            # draw rank and name
            self.canvas.create_text(rank_x, y, anchor="w", text=rank_text, font=body_font, fill=WHITE)
            self.canvas.create_text(name_x, y, anchor="w", text=name_disp, font=body_font, fill=WHITE)

            # draw medals based on numeric rank
            medal_size = max(50, int(line_h * 0.85))
            medal_map = {1: "gold", 2: "silver", 3: "bronze"}
            med = medal_map.get(rank_num)
            if med:
                pil_medal = self._medal_pils.get(med)
                if pil_medal:
                    # place medal right after the name text
                    name_width_px = body_font.measure(name_disp)
                    medal_x = name_x + name_width_px + 35
                    try:
                        medal_tk = self._get_resized_photo(pil_medal, f"medal_{med}_{i}_{medal_size}", medal_size, medal_size)
                        if medal_tk:
                            self._medal_tks[(med, i)] = medal_tk
                            self.canvas.create_image(medal_x, y - (medal_size//6), image=medal_tk, anchor="w")
                    except Exception:
                        pass

            # numeric columns 
            self.canvas.create_text(lives_right, y, anchor="e", text=lives_text, font=body_font, fill=WHITE)
            self.canvas.create_text(keys_right, y, anchor="e", text=keys_text, font=body_font, fill=WHITE)

        if not entries:
            self.canvas.create_text(WIDTH//2, box_y + box_h//2, text="No scores yet.", font=self.small_font, fill=WHITE)

        # buttons at bottom
        btn_w = 360
        btn_h = 55
        gap = 28
        total_w = btn_w * 2 + gap
        start_x = box_x + max(20, (box_w - total_w) // 2)
        btn_y = box_y + box_h - 70

        if start_x + total_w > box_x + box_w - 20:
            avail = box_w - 80 - gap
            btn_w = max(140, int(avail // 2))
            total_w = btn_w * 2 + gap
            start_x = box_x + (box_w - total_w) // 2

        clear_x = start_x
        back_x = start_x + btn_w + gap

        self.draw_button("CLEAR LEADERBOARD", btn_y, "clear_leaderboard", x=clear_x, w=btn_w, h=btn_h)
        self.draw_button("BACK TO MENU", btn_y, "back_to_menu", x=back_x, w=btn_w, h=btn_h)


    def redraw(self):
        self.clear(); self._draw_background()
        if self.state == "menu": self.draw_menu()
        elif self.state == "instructions": self.draw_boxed_text("INSTRUCTIONS", instructions_text, self.scroll_offset)
        elif self.state == "about": self.draw_boxed_text("ABOUT US", about_text, self.scroll_offset)
        elif self.state == "enter_name": self.draw_enter_name()
        elif self.state == "prologue": self.draw_prologue()
        elif self.state == "help_choice": self.draw_help_choice()
        elif self.state == "help_happy": self.draw_help_happy()
        elif self.state in ("story_intro",): self.draw_story_intro(self.story_text)
        elif self.state in ("hallway","anim_walk","anim_open"): self.draw_hallway()
        elif self.state == "stage1": self.draw_stage(0, self.answer_input)
        elif self.state == "stage2": self.draw_stage(1, self.answer_input)
        elif self.state == "stage3": self.draw_stage(2, self.answer_input)
        elif self.state == "stage4": self.draw_stage(3, self.answer_input)
        elif self.state == "stage5": self.draw_stage(4, self.answer_input)
        elif self.state == "ending": self._maybe_save_score(); self.draw_ending()
        elif self.state == "leaderboards": self.draw_leaderboards()
        else: self.draw_menu()
        self.after(33, self.redraw)

    def _blink_loop(self):
        self.cursor_visible = not self.cursor_visible; self.after(500, self._blink_loop)

    def _apply_opacity(self, pil_img, opacity):
        """Return a copy of pil_img with its alpha channel multiplied by opacity (0..1)."""
        try:
            if pil_img is None:
                return None
            im = pil_img.copy()
            if im.mode != "RGBA":
                im = im.convert("RGBA")
            # multiply alpha
            alpha = im.split()[3].point(lambda p: int(p * opacity))
            im.putalpha(alpha)
            return im
        except Exception as e:
            # fallback: return original
            return pil_img

    def _fade_in_hero(self):
        """Simple incremental fade for hero_opacity; clears cached hero images so PhotoImage is updated."""
        try:
            step = 1.0 / max(1, int(self.hero_fade_steps))
            self.hero_opacity = min(1.0, self.hero_opacity + step)
            keys_to_remove = [k for k in list(self._img_cache.keys()) if isinstance(k, tuple) and str(k[0]).find("hero") != -1]
            for k in keys_to_remove:
                try: del self._img_cache[k]
                except: pass
            if self.hero_opacity < 1.0:
                self.after(40, self._fade_in_hero)
        except Exception:
            pass

    def animate_to_door(self, which):
        """Walk the hero to the CENTER of the selected door."""
        if which not in self.door_geo:
            return

        # Get door's geometry
        x, y, w, h = self.door_geo[which]

        # Hero moves to the horizontal center of the door
        target_center_x = x + (w // 2)

        # Set target and start animation
        self.hero_target_x = target_center_x
        self.animating = True
        self.anim_target_door = which
        self.state = "anim_walk"

        # Make sure door opening animation is reset
        self.door_opening = None

        # Begin walking steps
        self._walk_step()


    def _walk_step(self):
        """Walking loop: move hero by small steps at delay self._walk_delay for smoother motion."""
        if not self.animating:
            return
        dx = self.hero_target_x - self.hero_x
        step = self.hero_speed
        if abs(dx) <= step:

            self.hero_x = self.hero_target_x
            self.state = "anim_open"
            self._open_door_then_enter(self.anim_target_door)
            return
        
        if dx < 0:
            self.hero_x += -min(abs(dx), step) 
        else:
            self.hero_x += min(abs(dx), step)   

        try:
            self.after(self._walk_delay, self._walk_step)
        except Exception:
            self.after(24, self._walk_step)

    def _open_door_then_enter(self, which):
        """Show opening door image while hero stands at the door, then switch to the stage."""
        self.door_opening = which
    
        def proceed(): 
            self.door_opening = None
            self.animating = False
            self.state = f"stage{which}"
            self.answer_input = ""
        self.after(600, proceed)

    def on_key(self, event):
        if self.state == "enter_name":
            if event.keysym == "BackSpace":
                play_typing_generic(); self.player_name = self.player_name[:-1]
            elif event.keysym == "Return":
                if self.player_name.strip(): self.start_prologue(self.player_name.strip())
            else:
                ch = event.char
                if ch and ord(ch) >= 32:
                    input_box = getattr(self, "_enter_name_input_box", None)
                    available_width = getattr(self, "_enter_name_available_width", None)
                    padding_x = getattr(self, "_enter_name_padding_x", 10)
                    if input_box is None or available_width is None:
                        box_w = 800; padding_x = 10; available_width = (box_w - 40) - (padding_x * 2)
                    new_text = self.player_name + ch
                    new_width = self.small_font.measure(new_text)
                    if new_width <= available_width:
                        play_typing_generic(); self.player_name = new_text
        elif self.state.startswith("stage"):
            if event.keysym == "BackSpace":
                self.answer_input = self.answer_input[:-1]
            elif event.keysym == "Return":
                pass
            else:
                if len(event.char) > 0:
                    self.answer_input += event.char
        elif self.state == "menu":
            if event.keysym == "Return": self.state = "enter_name"

    def on_mousewheel_windows(self, event):
        delta = event.delta // 120; self._scroll_box(delta * 30)

    def on_mousewheel_linux(self, event):
        if event.num == 4: self._scroll_box(30)
        elif event.num == 5: self._scroll_box(-30)

    def _scroll_box(self, delta_pixels):
        if self.state in ("instructions", "about"):
            box_w = WIDTH - 200; inner_w = box_w - 80; text = instructions_text if self.state == "instructions" else about_text
            lines = wrap_text_to_lines(self.small_font, text, inner_w)
            line_height = self.small_font.metrics("linespace") + 6; inner_h = (HEIGHT - 200) - 140
            max_scroll = max(0, len(lines) * line_height - inner_h)
            self.scroll_offset = max(-max_scroll, min(0, self.scroll_offset + delta_pixels))

    def on_mouse_move(self, event):
        self.mouse_x = event.x; self.mouse_y = event.y

    def on_click(self, event):
        for tag, (x1, y1, x2, y2) in list(self.click_areas.items()):
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.handle_click(tag); return
        if self.state == "prologue":
            panel_x, panel_y = PANEL_MARGIN, PANEL_MARGIN; panel_w, panel_h = WIDTH - 2*PANEL_MARGIN, HEIGHT - 2*PANEL_MARGIN
            text_pad_x = 80; text_pad_y = panel_y + panel_h - 180
            if (panel_x + text_pad_x) <= event.x <= (panel_x + panel_w - text_pad_x) and text_pad_y <= event.y <= text_pad_y + 140:
                if not self.scene_done:
                    self.scene_text_shown = self.scene_text_full; self.scene_char_idx = len(self.scene_text_full); self.scene_done = True
                    if self._type_after_id:
                        try: self.after_cancel(self._type_after_id)
                        except Exception: pass
                        self._type_after_id = None
                    if pygame_available and story_typing:
                        try: story_typing.stop()
                        except Exception: pass
                else:
                    self._advance_scene()

    def handle_click(self, tag):
        play_click()
        if tag == "play":
            self.state = "enter_name"; self.player_name = ""; self.answer_input = ""; self.lives = 3; self.keys_collected = 0; self.scroll_offset = 0
            self.completed = set(); self.unlocked = {5}; self.hero_x = 120; self.animating = False; self._score_saved = False
        elif tag == "instructions":
            self.state = "instructions"; self.scroll_offset = 0
        elif tag == "leaderboards":
            self.state = "leaderboards"; self.scroll_offset = 0
        elif tag == "about":
            self.state = "about"; self.scroll_offset = 0
        elif tag == "back_to_menu":
            self.state = "menu"; self.scroll_offset = 0
        elif tag == "submit_name" and self.player_name.strip():
            self.start_prologue(self.player_name.strip())
        elif tag == "intro_back":
            self.state = "enter_name"
        elif tag == "start_game":
            loader = LoadingScreen(self, duration=2.8, gif_path=LOADING_GIF, jingle_path=LOADING_JINGLE)
            loader.start()
            self.wait_window(loader)

            self.state = "hallway"
            self.answer_input = ""

            # start hero
            self.hero_x = WIDTH - 200

            self.animating = False

            try:
                self.unlocked.add(5)
            except Exception:
                self.unlocked = {5}

            self.hero_visible = False
            self.hero_opacity = 0.0

        elif tag in ("option1","option2","option3","option4"):
            idx = int(tag[-1]) - 1; q_idx = None
            if self.state.startswith("stage"):
                try:
                    n = int(self.state.replace("stage",""))
                    q_idx = n - 1
                except Exception:
                    q_idx = None
            if q_idx is not None and 0 <= q_idx < len(questions):
                opts = questions[q_idx].get("options")
                if not opts or len(opts) < 4:
                    correct = questions[q_idx].get("answer",""); opts = [correct,"","",""]
                chosen_label = opts[idx] if idx < len(opts) else ""
                letter = ["a","b","c","d"][idx]
                self.answer_input = letter
                self.submit_answer()
        elif tag == "prologue_skip":
            if pygame_available:
                try:
                    if story_typing: story_typing.stop()
                    pygame.mixer.music.fadeout(600); self.after(650, self._restore_bg_music)
                except Exception: pass
            self.state = "help_choice"; self.help_choice_visible = True; self.help_happy_shown = False
            try: self.start_help_typing()
            except Exception: pass
            try:
                self.scene_index = len(self.prologue_scenes) - 1
                self.scene_text_shown = self.prologue_scenes[self.scene_index].get("text","")
                self.scene_done = True; self.scene_char_idx = len(self.scene_text_shown)
            except Exception:
                pass
        elif tag == "prologue_continue":
            self._advance_scene()

        # help choice handlers
        elif tag == "help_yes":
            # switch to happy screen and start happy typing
            self.state = "help_happy"; self.help_happy_shown = True
            try:
                self.start_help_happy()
            except Exception:
                pass
        elif tag == "help_no":
            self.state = "story_intro"; self.story_text = f"In a mysterious land... {self.player_name}..."; self.help_choice_visible = False; self.help_happy_shown = False
            if getattr(self, "_help_after_id", None):
                try: self.after_cancel(self._help_after_id)
                except Exception:
                    self._help_after_id = None

        elif tag == "play_again":
            self.state = "menu"; self.answer_input = ""; self.lives = 3; self.keys_collected = 0; self.completed = set(); self.unlocked = {5}; self.hero_x = 120; self.animating = False; self._score_saved = False

        elif tag == "exit_game":
            try:
                if pygame_available and bg_music_loaded: pygame.mixer.music.stop()
            except Exception:
                pass
            self.destroy()

        # Leaderboard clear button 
        elif tag == "clear_leaderboard":
            clear_leaderboard_file()
            self.state = "leaderboards"
        elif tag == "confirm_clear_no":
            self.state = "leaderboards"

        elif tag.startswith("door"):
            try:
                which = int(tag.replace("door", ""))
            except:
                which = None
            if which:
                if which in self.unlocked:
                    # Reveal & fade hero
                    self.hero_visible = True
                    self.hero_opacity = 0.0
                    try:
                        self._fade_in_hero()
                    except Exception:
                        self.hero_opacity = 1.0

                    try:
                        panel_x = PANEL_MARGIN
                        panel_w = WIDTH - 2 * PANEL_MARGIN
                        door_x, door_y, door_w, door_h = self.door_geo.get(which, (panel_x + panel_w//2, 0, 180, 360))
                        
                        safe_right = panel_x + panel_w - int(door_w * 0.6)
                        safe_left = panel_x + int(door_w * 0.6)

                        if not getattr(self, "hero_x", None):
                            self.hero_x = safe_right
                        else:
                            self.hero_x = max(safe_left, min(self.hero_x, safe_right))
                    except Exception:
                        # fallback
                        self.hero_x = WIDTH - 200
                        self.hero_y = door_y + door_h - (self.hero_h // 2)
                    except Exception:
                        self.hero_y = HEIGHT - 180

                    # walking animation
                    self.animate_to_door(which)
                else:
                    pass

    def _open_confirm_clear(self):
        
        dlg = tk.Toplevel(self)
        dlg.title("Confirm Clear")
        dlg.geometry("360x140")
        dlg.transient(self); dlg.grab_set()
        lbl = tk.Label(dlg, text="Are you sure you want to clear\nall leaderboard entries?", font=("Arial", 12), justify="center")
        lbl.pack(pady=12)
        btn_frame = tk.Frame(dlg)
        btn_frame.pack(pady=6)
        def yes():
            try: clear_leaderboard_file()
            except Exception as e: print("clear error:", e)
            dlg.grab_release(); dlg.destroy(); self.state = "leaderboards"
        def no():
            dlg.grab_release(); dlg.destroy(); self.state = "leaderboards"
        b1 = tk.Button(btn_frame, text="Yes, clear", width=12, command=yes)
        b2 = tk.Button(btn_frame, text="Cancel", width=12, command=no)
        b1.grid(row=0, column=0, padx=8); b2.grid(row=0, column=1, padx=8)

    def submit_answer(self):
        # Generic stage handler
        if not self.state.startswith("stage"):
            return

        try:
            stage_num = int(self.state.replace("stage", ""))
        except Exception:
            return

        q_idx = stage_num - 1
        if q_idx < 0 or q_idx >= len(questions):
            return

        correct_answer = str(questions[q_idx].get("answer", "")).strip().lower()
        given = str(self.answer_input).strip().lower()
        correct = (given == correct_answer)

        if correct:
            # Increase key count 
            self.keys_collected += 1
            self.completed.add(stage_num)

            if stage_num > 1:
                door_to_unlock = stage_num - 1
                self.unlocked.add(door_to_unlock)

                # Return to hallway 
                self.state = "hallway"
                self.answer_input = ""
                return

            if stage_num == 1:
                self.answer_input = ""
                self.state = "ending"
                self._maybe_save_score()
                return

        else:
            # Wrong answer handler
            self.lives -= 1
            self.answer_input = ""

            if self.lives <= 0:
                self.state = "ending"
                self._maybe_save_score()
                return
            self.state = "hallway"


    def _maybe_save_score(self):
        if getattr(self, "_score_saved", False): return
        name = (self.player_name or "").strip() or "Unknown"
        try: keys = int(self.keys_collected)
        except: keys = 0
        try: lives = int(self.lives)
        except: lives = 0
        try:
            add_score_to_leaderboard(name, keys, lives)
            self._score_saved = True
            print(f"Saved score for {name}: keys={keys} lives={lives}")
        except Exception as e:
            print("Failed to save score:", e)

if __name__ == "__main__":
    if not PIL_AVAILABLE:
        print("Pillow (PIL) is recommended for images. Install: pip install pillow")
    expected_files = [IMG_S1, IMG_S2, IMG_S3, IMG_S4, IMG_S5, IMG_S6, IMG_S7, IMG_S8, IMG_S9, CHAR_SPRITE_PATH, DOOR_CLOSED_PATH, DOOR_OPEN_PATH, IMG_S_CRY, IMG_S_HAPPY]
    missing = []
    for p in expected_files:
        try:
            if not p or not Path(p).exists():
                missing.append(str(p))
        except Exception:
            missing.append(str(p))
    if missing:
        print("\nWarning: some image files are missing (they'll display plain backgrounds).")
        for m in missing:
            print("  ", m)
        print("\nSearch dirs checked (in order):")
        for d in SEARCH_DIRS:
            print("  -", d)
    app = AdventureQuiz()
    app.mainloop()
