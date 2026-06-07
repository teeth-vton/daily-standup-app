from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import urllib.parse
from datetime import datetime, timezone, timedelta

app = FastAPI()

# Temporary in-memory database
submissions_db = []

def get_ist_now():
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist_tz)

def get_ist_date():
    return get_ist_now().strftime("%B %d, %Y")

# Shared HTML Header for Mobile "App" Experience
PWA_HEADERS = """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#111827">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🚀</text></svg>">
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🚀</text></svg>">
"""

# ==========================================
# PAGE 1: THE TEAM SUBMISSION APP (Route: /)
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def get_form():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>ADV Submit</title>
        {PWA_HEADERS}
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @keyframes rainbowGlow {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
            .rainbow-line {{ background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37); background-size: 400% 400%; animation: rainbowGlow 12s ease infinite; }}
            .bg-adv-text {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-10deg); font-size: clamp(8rem, 20vw, 24rem); font-weight: 900; letter-spacing: -0.5rem; white-space: nowrap; z-index: 0; pointer-events: none; background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37); background-size: 400% 400%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; opacity: 0.12; }}
            body {{ position: relative; overflow-x: hidden; -webkit-tap-highlight-color: transparent; }}
        </style>
        <script>
            tailwind.config = {{ darkMode: 'class' }}
            function autoSelectRole() {{
                const nameDropdown = document.getElementById("name-dropdown");
                const roleDropdown = document.getElementById("role-dropdown");
                const teamRoles = {{
                    "Pragg": "SEO", "Yashpaal": "Coder", "Aaniket": "Coder", "Bhaavin": "Coder",
                    "Manthan": "Video Editor", "Sonic": "Video Editor", "Jenish": "Video Editor", "Dhiraj": "Video Editor",
                    "Saavan": "UX/UI", "Dhruvit": "UX/UI", "Nikhil": "AI Developer", "Karan": "Other"
                }};
                if (teamRoles[nameDropdown.value]) {{ roleDropdown.value = teamRoles[nameDropdown.value]; }}
            }}
        </script>
    </head>
    <body class="bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 font-sans min-h-screen p-4 flex justify-center items-center">
        <div class="bg-adv-text">ADV</div>
        
        <div class="relative z-10 w-full max-w-md bg-white dark:bg-gray-900 rounded-3xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden pb-4">
            <div class="rainbow-line h-3 w-full"></div>
            <div class="p-6">
                <div class="flex items-center space-x-3 mb-6">
                    <span class="text-4xl">🚀</span>
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight">Daily Standup</h1>
                        <p class="text-xs text-gray-500">Tap to submit your ADV updates</p>
                    </div>
                </div>
                
                <form action="/submit" method="POST" class="space-y-6">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Name</label>
                        <select id="name-dropdown" name="name" onchange="autoSelectRole()" required class="
