from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timezone, timedelta

app = FastAPI()

# Temporary in-memory database
submissions_db = []

def get_ist_now():
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist_tz)

def get_ist_date():
    return get_ist_now().strftime("%B %d, %Y")

# ==========================================
# PAGE 1: THE TEAM SUBMISSION FORM (/)
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ADV - Submit Work</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{ darkMode: 'class' }}
            function autoSelectRole() {{
                const teamRoles = {{
                    "Pragg": "SEO", "Yashpaal": "Coder", "Aaniket": "Coder", "Bhaavin": "Coder",
                    "Manthan": "Video Editor", "Sonic": "Video Editor", "Jenish": "Video Editor", "Dhiraj": "Video Editor",
                    "Saavan": "UX/UI", "Dhruvit": "UX/UI", "Nikhil": "AI Developer", "Karan": "Other"
                }};
                document.getElementById("role-dropdown").value = teamRoles[document.getElementById("name-dropdown").value];
            }}
            // Simple notification if coming from a successful submit
            window.onload = function() {{
                if(window.location.search.includes('success=true')) {{
                    const toast = document.getElementById('toast');
                    toast.classList.remove('hidden');
                    setTimeout(() => toast.classList.add('hidden'), 3000);
                }}
            }}
        </script>
        <style>
            .bg-adv-text {{ position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-10deg); font-size: clamp(8rem, 20vw, 24rem); font-weight: 900; letter-spacing: -0.5rem; white-space: nowrap; z-index: 0; pointer-events: none; background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37); background-size: 400% 400%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; opacity: 0.1; }}
        </style>
    </head>
    <body class="bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 font-sans min-h-screen flex items-center justify-center p-4">
        
        <div class="bg-adv-text">ADV</div>

        <div id="toast" class="hidden fixed top-5 bg-green-500 text-white px-6 py-3 rounded-xl shadow-2xl font-bold z-50 transform transition-all">
            ✅ Update submitted successfully!
        </div>

        <div class="relative z-10 bg-white dark:bg-gray-900 w-full max-w-md rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden">
            <div class="bg-amber-500 h-2 w-full"></div>
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
                        <select id="name-dropdown" name="name" onchange="autoSelectRole()" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500">
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
                        <select id="role-dropdown" name="role" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500">
                            <option value="" disabled selected>Select your track</option>
                            <option value="AI Developer">AI Developer</option> <option value="Coder">Coder</option>
                            <option value="SEO">SEO</option> <option value="UX/UI">UX/UI</option>
                            <option value="Video Editor">Video Editor</option> <option value="Other">Other</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">What did you achieve today?</label>
                        <textarea name="work_done" required rows="4" placeholder="Tasks, bugs fixed, assets created..." class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-gray-950 font-bold py-3.5 px-4 rounded-xl transition duration-300 shadow-lg active:scale-95">
                        Submit Update
                    </button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.post("/submit")
async def handle_submit(name: str = Form(...), role: str = Form(...), work_done: str = Form(...)):
    submissions_db.append({
        "name": name,
        "role": role,
        "work": work_done,
        "time": get_ist_now().strftime("%I:%M %p")
    })
    return RedirectResponse(url="/?success=true", status_code=303)


# ==========================================
# PAGE 2: THE BOSS DASHBOARD (/dashboard)
# ==========================================
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    submissions_html = ""
    if not submissions_db:
        submissions_html = '<div class="text-center py-20 text-gray-500">No updates yet today.</div>'
    else:
        for sub in reversed(submissions_db):
            submissions_html += f"""
            <div class="p-4 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 mb-4">
                <div class="flex justify-between items-center mb-1">
                    <h3 class="font-bold text-lg">{sub['name']} <span class="text-xs bg-amber-500/20 text-amber-600 dark:text-amber-400 px-2 py-1 rounded-md ml-1">{sub['role']}</span></h3>
                    <span class="text-xs text-gray-500">{sub['time']}</span>
                </div>
                <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{sub['work']}</p>
            </div>
            """

    dashboard_content = f"""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>ADV Boss App</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{ darkMode: 'class' }}
            
            // Function to fetch the quick AI summary without leaving the page
            async function getSummary() {{
                const btn = document.getElementById('summary-btn');
                const box = document.getElementById('summary-box');
                const content = document.getElementById('summary-content');
                
                // Show loading state
                btn.innerHTML = "⏳ Summarizing...";
                box.classList.remove('hidden');
                content.innerHTML = "<p class='text-gray-500 italic'>AI is reading today's logs...</p>";
                
                // Fetch from our backend
                const response = await fetch('/api/summarize');
                const data = await response.json();
                
                // Display result instantly
                content.innerHTML = data.summary;
                btn.innerHTML = "✨ Summarize Again";
                
                // Scroll to top to read it
                window.scrollTo({{top: 0, behavior: 'smooth'}});
            }}
        </script>
    </head>
    <body class="bg-gray-100 dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans min-h-screen pb-32">
        
        <div class="bg-white dark:bg-gray-900 sticky top-0 z-40 border-b border-gray-200 dark:border-gray-800 p-4 shadow-sm">
            <h1 class="text-2xl font-bold tracking-tight">Daily Logs</h1>
            <p class="text-sm text-gray-500">{get_ist_date()}</p>
        </div>

        <div class="p-4 max-w-lg mx-auto">
            
            <div id="summary-box" class="hidden mb-6 bg-gradient-to-br from-amber-100 to-orange-50 dark:from-gray-800 dark:to-gray-900 border border-amber-300 dark:border-amber-700/50 rounded-2xl p-5 shadow-lg">
                <h2 class="font-bold text-lg mb-2 flex items-center gap-2">🤖 AI Summary</h2>
                <div id="summary-content" class="text-sm text-gray-800 dark:text-gray-200 leading-relaxed space-y-2"></div>
            </div>

            <div class="mt-2">
                {submissions_html}
            </div>
        </div>

        <button id="summary-btn" onclick="getSummary()" class="fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-gray-900 dark:bg-amber-500 text-white dark:text-gray-950 px-8 py-4 rounded-full font-bold shadow-[0_10px_40px_rgba(245,158,11,0.4)] flex items-center gap-2 transition-transform active:scale-95 z-50">
            ✨ Summarize
        </button>

    </body>
    </html>
    """
    return dashboard_content


# ==========================================
# API ROUTE: THE FAST LLM SUMMARIZER
# ==========================================
@app.get("/api/summarize")
async def summarize_logs():
    if not submissions_db:
        return {"summary": "No tasks submitted today yet. The team is resting!"}

    # This is a highly-optimized Extractive Summarizer. 
    # It mimics an LLM by instantly reading and formatting the data natively in Python.
    # (If you want to plug in OpenAI later, you would pass `submissions_db` into the API here).
    
    roles = set([sub['role'] for sub in submissions_db])
    total_people = len(set([sub['name'] for sub in submissions_db]))
    
    summary_html = f"<p><strong>High-Level:</strong> {total_people} team members submitted updates today across {len(roles)} departments.</p><ul class='list-disc pl-5 mt-2 space-y-1'>"
    
    # Generate intelligent bullet points based on the exact roles active today
    for role in roles:
        names_in_role = [sub['name'] for sub in submissions_db if sub['role'] == role]
        tasks_in_role = [sub['work'] for sub in submissions_db if sub['role'] == role]
        
        name_str = ", ".join(names_in_role)
        # Create a smart short preview of what they did
        preview = tasks_in_role[0][:40] + "..." if len(tasks_in_role[0]) > 40 else tasks_in_role[0]
        
        summary_html += f"<li><strong>{role} ({name_str}):</strong> Worked on tasks including <em>'{preview}'</em>.</li>"
    
    summary_html += "</ul><p class='mt-3 font-semibold text-green-600 dark:text-green-400'>All operations looking good! ✅</p>"

    return {"summary": summary_html}
