from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import urllib.parse
from datetime import datetime
import pytz

app = FastAPI()

# Temporary in-memory database to hold today's work
# (We will upgrade this to a real database later so it saves forever)
submissions_db = []

def get_ist_date():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime("%B %d, %Y")

# ==========================================
# PAGE 1: THE SUBMISSION FORM (Manager Removed)
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def get_form():
    html_content = """
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ADV Dept - Daily Standup</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @keyframes rainbowGlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
            .rainbow-line { background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37); background-size: 400% 400%; animation: rainbowGlow 12s ease infinite; }
            .bg-adv-text { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-10deg); font-size: clamp(8rem, 20vw, 24rem); font-weight: 900; letter-spacing: -0.5rem; white-space: nowrap; z-index: 0; pointer-events: none; background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37); background-size: 400% 400%; animation: rainbowGlow 12s ease infinite; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; opacity: 0.12; }
            body { position: relative; overflow-x: hidden; }
        </style>
        <script>
            tailwind.config = { darkMode: 'class' }
            function toggleTheme() {
                const html = document.documentElement;
                const btn = document.getElementById('theme-btn');
                if (html.classList.contains('dark')) {
                    html.classList.remove('dark');
                    btn.innerHTML = '<span class="text-black text-xl">☀️</span>';
                    btn.className = "bg-white border border-gray-300 rounded-full w-12 h-12 flex items-center justify-center shadow-md hover:bg-gray-100 transition duration-300";
                } else {
                    html.classList.add('dark');
                    btn.innerHTML = '<span class="text-white text-xl">🌙</span>';
                    btn.className = "bg-gray-800 border border-gray-700 rounded-full w-12 h-12 flex items-center justify-center shadow-md hover:bg-gray-700 transition duration-300";
                }
            }
            function autoSelectRole() {
                const nameDropdown = document.getElementById("name-dropdown");
                const roleDropdown = document.getElementById("role-dropdown");
                const teamRoles = {
                    "Pragg": "SEO", "Yashpaal": "Coder", "Aaniket": "Coder", "Bhaavin": "Coder",
                    "Manthan": "Video Editor", "Sonic": "Video Editor", "Jenish": "Video Editor", "Dhiraj": "Video Editor",
                    "Saavan": "UX/UI", "Dhruvit": "UX/UI", "Nikhil": "AI Developer", "Karan": "Other"
                };
                if (teamRoles[nameDropdown.value]) { roleDropdown.value = teamRoles[nameDropdown.value]; }
            }
        </script>
    </head>
    <body class="bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 font-sans min-h-screen flex flex-col items-center justify-center p-4 transition-colors duration-500">
        <div class="bg-adv-text">ADV</div>
        <div class="absolute top-4 right-4 sm:top-6 sm:right-6 z-50">
            <button id="theme-btn" onclick="toggleTheme()" class="bg-gray-800 border border-gray-700 rounded-full w-12 h-12 flex items-center justify-center shadow-md hover:bg-gray-700 transition duration-300">
                <span class="text-white text-xl">🌙</span>
            </button>
        </div>
        <div class="relative z-10 bg-white dark:bg-gray-900 w-full max-w-md rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden transition-colors duration-500 my-12">
            <div class="rainbow-line h-3.5 w-full"></div>
            <div class="p-6 sm:p-8">
                <div class="flex items-center space-x-3 mb-6">
                    <span class="text-3xl">🚀</span>
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight">Daily Standup</h1>
                        <p class="text-sm text-gray-500 dark:text-gray-400">Submit your ADV updates below</p>
                    </div>
                </div>
                <form action="/submit" method="POST" class="space-y-5">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Name</label>
                        <select id="name-dropdown" name="name" onchange="autoSelectRole()" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 cursor-pointer">
                            <option value="" disabled selected>Select your name</option>
                            <option value="Nikhil">Nikhil</option> <option value="Pragg">Pragg</option>
                            <option value="Yashpaal">Yashpaal</option> <option value="Aaniket">Aaniket</option>
                            <option value="Bhaavin">Bhaavin</option> <option value="Manthan">Manthan</option>
                            <option value="Sonic">Sonic</option> <option value="Jenish">Jenish</option>
                            <option value="Dhiraj">Dhiraj</option> <option value="Saavan">Saavan</option>
                            <option value="Dhruvit">Dhruvit</option> <option value="Karan">Karan</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Department Role</label>
                        <select id="role-dropdown" name="role" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 cursor-pointer">
                            <option value="" disabled selected>Select your track</option>
                            <option value="AI Developer">AI Developer</option> <option value="Coder">Coder</option>
                            <option value="SEO">SEO</option> <option value="UX/UI">UX/UI</option>
                            <option value="Video Editor">Video Editor</option> <option value="Other">Other</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">What did you achieve today?</label>
                        <textarea name="work_done" required rows="4" placeholder="List your tasks, bugs fixed, or assets created..." class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-gray-950 font-bold py-3.5 px-4 rounded-xl transition duration-300 shadow-lg shadow-amber-500/10 hover:shadow-amber-500/20 transform active:scale-[0.98]">
                        Submit Update
                    </button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# ==========================================
# ROUTE: SAVE DATA & REDIRECT TO DASHBOARD
# ==========================================
@app.post("/submit")
async def handle_submit(name: str = Form(...), role: str = Form(...), work_done: str = Form(...)):
    # Save to our temporary database
    submissions_db.append({
        "name": name,
        "role": role,
        "work": work_done,
        "time": datetime.now().strftime("%I:%M %p")
    })
    # After submitting, immediately send them back to the empty form for the next person
    return RedirectResponse(url="/", status_code=303)

# ==========================================
# PAGE 2: THE BOSS DASHBOARD (/dashboard)
# ==========================================
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    # 1. Generate the raw text for WhatsApp
    whatsapp_text = f"🚀 *ADV Daily Summary - {get_ist_date()}*\n\n"
    for sub in submissions_db:
        whatsapp_text += f"*{sub['name']}* ({sub['role']}): {sub['work']}\n"
    
    # Add the link to this exact dashboard so the boss can view it on the web
    dashboard_url = str(request.base_url) + "dashboard"
    whatsapp_text += f"\n📊 *View full details here:* {dashboard_url}"
    
    # 2. Encode the text so it works in a URL
    encoded_whatsapp = urllib.parse.quote(whatsapp_text)
    whatsapp_link = f"https://wa.me/?text={encoded_whatsapp}"

    # 3. Generate HTML for the submissions list
    submissions_html = ""
    if not submissions_db:
        submissions_html = '<p class="text-gray-500 text-center py-8">No updates submitted today yet.</p>'
    else:
        for sub in submissions_db:
            submissions_html += f"""
            <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 mb-3">
                <div class="flex justify-between items-center mb-2">
                    <h3 class="font-bold text-lg">{sub['name']} <span class="text-xs bg-amber-500/20 text-amber-600 dark:text-amber-400 px-2 py-1 rounded-md ml-2">{sub['role']}</span></h3>
                    <span class="text-xs text-gray-500">{sub['time']}</span>
                </div>
                <p class="text-sm text-gray-700 dark:text-gray-300">{sub['work']}</p>
            </div>
            """

    dashboard_content = f"""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ADV - Admin Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .rainbow-line {{ background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37); background-size: 400% 400%; animation: rainbowGlow 12s ease infinite; }}
            @keyframes rainbowGlow {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
        </style>
        <script>tailwind.config = {{ darkMode: 'class' }}</script>
    </head>
    <body class="bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 font-sans min-h-screen p-6">
        <div class="max-w-4xl mx-auto mt-10">
            <div class="flex justify-between items-center mb-8">
                <div>
                    <h1 class="text-3xl font-bold tracking-tight">ADV Daily Logs</h1>
                    <p class="text-gray-500">{get_ist_date()}</p>
                </div>
                
                <!-- THE WHATSAPP TRIGGER BUTTON -->
                <a href="{whatsapp_link}" target="_blank" class="flex items-center space-x-2 bg-[#25D366] hover:bg-[#1ebd59] text-white font-bold py-3 px-6 rounded-xl shadow-lg transition duration-300 transform hover:scale-105">
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.274.072.376-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.099.824zm-3.423-14.416c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm.029 18.88c-1.161 0-2.305-.292-3.318-.844l-3.677.964.984-3.595c-.607-1.052-.927-2.246-.926-3.468.001-3.825 3.113-6.937 6.937-6.937 3.825 0 6.938 3.112 6.938 6.937s-3.113 6.938-6.938 6.938z"/></svg>
                    <span>Send Daily Summary</span>
                </a>
            </div>

            <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
                <div class="rainbow-line h-2 w-full"></div>
                <div class="p-6">
                    <h2 class="text-xl font-bold mb-4 border-b border-gray-200 dark:border-gray-700 pb-2">Today's Updates</h2>
                    {submissions_html}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return dashboard_content
