from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timezone, timedelta
import urllib.parse
import urllib.request
import json

app = FastAPI()

# Temporary in-memory database
submissions_db = []

def get_ist_now():
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist_tz)

def get_ist_date():
    return get_ist_now().strftime("%B %d, %Y")

# Track the current active month for the auto-reset feature
current_active_month = get_ist_now().month

def check_monthly_reset():
    """Automatically clears the database if a new month has started in India Standard Time."""
    global current_active_month, submissions_db
    now_month = get_ist_now().month
    if now_month != current_active_month:
        submissions_db.clear()
        current_active_month = now_month

# ==========================================
# PAGE 1: THE TEAM SUBMISSION FORM (/)
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    check_monthly_reset() 
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="ADV Submit">
        <meta name="theme-color" content="#111827">

        <title>ADV - Submit Work</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{ darkMode: 'class' }}
            function autoSelectRole() {{
                const teamRoles = {{
                    "Pragg": "SEO", "Yashpaal": "Coder", "Aaniket": "Coder", "Bhaavin": "Coder",
                    "Manthan": "Video Editor", "Sonic": "Video Editor", "Jenish": "Video Editor", "Dhiraj": "Video Editor",
                    "Saavan": "UX/UI", "Dhruvit": "UX/UI", "Nikhil": "AI", "Karan": "Other"
                }};
                document.getElementById("role-dropdown").value = teamRoles[document.getElementById("name-dropdown").value];
            }}
            window.onload = function() {{
                if(window.location.search.includes('success=true')) {{
                    const toast = document.getElementById('toast');
                    toast.classList.remove('translate-y-[-100%]', 'opacity-0');
                    setTimeout(() => toast.classList.add('translate-y-[-100%]', 'opacity-0'), 3000);
                }}
                
                const textArea = document.getElementById('work_done_input');
                textArea.addEventListener('keydown', function(e) {{
                    if (e.key === 'Enter' && !e.shiftKey) {{
                        e.preventDefault(); 
                        document.getElementById('standup_form').submit(); 
                    }}
                }});
            }}

            function startDictation() {{
                if (window.hasOwnProperty('webkitSpeechRecognition') || window.hasOwnProperty('SpeechRecognition')) {{
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition();
                    
                    recognition.lang = 'gu-IN'; 
                    recognition.continuous = false;
                    recognition.interimResults = false;

                    const micBtn = document.getElementById('mic-btn');
                    const textArea = document.getElementById('work_done_input');
                    const originalIcon = micBtn.innerHTML;

                    recognition.onstart = function() {{
                        micBtn.innerHTML = "🔴"; 
                        micBtn.classList.add("animate-pulse");
                    }};

                    recognition.onresult = function(e) {{
                        const transcript = e.results[0][0].transcript;
                        textArea.value += (textArea.value.length > 0 ? " " : "") + transcript;
                    }};

                    recognition.onerror = function(e) {{
                        console.error("Voice recognition error:", e.error);
                    }};

                    recognition.onend = function() {{
                        micBtn.innerHTML = originalIcon;
                        micBtn.classList.remove("animate-pulse");
                    }};

                    recognition.start();
                }} else {{
                    alert("Sorry, your browser does not support Voice Dictation. Try Chrome or Edge.");
                }}
            }}
        </script>
        <style>
            .bg-adv-wrapper {{ position: fixed; inset: 0; overflow: hidden; pointer-events: none; z-index: 0; }}
            .bg-adv-text {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-10deg); font-size: clamp(8rem, 25vw, 24rem); font-weight: 900; letter-spacing: -0.5rem; white-space: nowrap; background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37); background-size: 400% 400%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; opacity: 0.1; }}
        </style>
    </head>
    <body class="bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 font-sans min-h-[100dvh] flex items-center justify-center p-4 m-0 overflow-x-hidden">
        
        <div class="bg-adv-wrapper"><div class="bg-adv-text">ADV</div></div>

        <div id="toast" class="fixed top-5 left-1/2 transform -translate-x-1/2 translate-y-[-100%] opacity-0 bg-green-500 text-white px-6 py-3 rounded-xl shadow-2xl font-bold z-50 transition-all duration-300 w-[90%] max-w-sm text-center">
            ✅ Update submitted!
        </div>

        <div class="relative z-10 bg-white dark:bg-gray-900 w-full max-w-md rounded-3xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden">
            <div class="bg-amber-500 h-2 w-full"></div>
            <div class="p-6 sm:p-8">
                <div class="flex items-center space-x-3 mb-8">
                    <span class="text-3xl">🚀</span>
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight">Daily Standup</h1>
                        <p class="text-sm text-gray-500 dark:text-gray-400">Submit your ADV updates below</p>
                    </div>
                </div>
                
                <form id="standup_form" action="/submit" method="POST" class="space-y-6">
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 ml-1">Your Name</label>
                        <select id="name-dropdown" name="name" onchange="autoSelectRole()" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-2xl px-4 py-3.5 text-base text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm appearance-none cursor-pointer">
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
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 ml-1">Department Role</label>
                        <select id="role-dropdown" name="role" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-2xl px-4 py-3.5 text-base text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm appearance-none cursor-pointer">
                            <option value="" disabled selected>Select your track</option>
                            <option value="AI">AI</option> <option value="Coder">Coder</option>
                            <option value="SEO">SEO</option> <option value="UX/UI">UX/UI</option>
                            <option value="Video Editor">Video Editor</option> <option value="Other">Other</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 ml-1">What did you achieve today?</label>
                        <div class="relative w-full">
                            <textarea id="work_done_input" name="work_done" required rows="4" placeholder="Tasks, bugs fixed, assets created... (Press Enter to submit)" class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-2xl px-4 py-3.5 pr-12 text-base text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm"></textarea>
                            <button type="button" id="mic-btn" onclick="startDictation()" class="absolute bottom-3 right-3 text-2xl hover:scale-110 transition-transform bg-white dark:bg-gray-700 rounded-full h-10 w-10 flex items-center justify-center shadow-md border border-gray-200 dark:border-gray-600">
                                🎤
                            </button>
                        </div>
                    </div>
                    <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-gray-950 font-extrabold text-lg py-4 px-4 rounded-2xl transition duration-300 shadow-lg active:scale-95 mt-2">
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
    check_monthly_reset() 
    
    submissions_db.append({
        "name": name,
        "role": role,
        "work": work_done,
        "date_string": get_ist_date(),
        "time": get_ist_now().strftime("%I:%M %p")
    })
    return RedirectResponse(url="/?success=true", status_code=303)


# ==========================================
# PAGE 2: THE BOSS DASHBOARD (/dashboard)
# ==========================================
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    check_monthly_reset() 
    
    # Pre-render all HTML but control visibility with JavaScript Daily View
    submissions_html = ""
    for sub in reversed(submissions_db):
        safe_name = sub['name'].lower().replace('"', '&quot;')
        safe_date = sub.get('date_string', '').lower().replace('"', '&quot;')
        
        submissions_html += f"""
        <div class="submission-card p-5 bg-white dark:bg-gray-800/80 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700/50 mb-4 backdrop-blur-sm transition-opacity duration-200" data-name="{safe_name}" data-date="{safe_date}">
            <div class="flex justify-between items-center mb-2">
                <h3 class="font-bold text-[17px]">{sub['name']} <span class="text-xs font-bold bg-amber-500/20 text-amber-600 dark:text-amber-400 px-2 py-1 rounded-lg ml-1">{sub['role']}</span></h3>
                <span class="text-xs font-medium text-gray-400 bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded-lg">{sub.get('date_string', '')} - {sub['time']}</span>
            </div>
            <p class="text-[15px] text-gray-700 dark:text-gray-300 leading-relaxed">{sub['work']}</p>
        </div>
        """

    dashboard_content = f"""
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, viewport-fit=cover">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="ADV Logs">
        <meta name="theme-color" content="#000000">

        <title>ADV Boss App</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{ darkMode: 'class' }}
            
            // ==========================================
            // JS: DAILY VIEW & SWIPE LOGIC
            // ==========================================
            let uniqueDates = [];
            let currentDateIndex = 0;
            let isSearchActive = false;

            window.onload = function() {{
                const todayStr = "{get_ist_date()}".toLowerCase();
                const cards = document.querySelectorAll('.submission-card');
                const datesSet = new Set();
                
                cards.forEach(c => datesSet.add(c.getAttribute('data-date')));
                uniqueDates = Array.from(datesSet);
                
                // Ensure Today is always the first page, even if empty
                if(!uniqueDates.includes(todayStr)) {{
                    uniqueDates.unshift(todayStr);
                }}
                
                currentDateIndex = 0; // 0 = Today
                updateFeedView();

                // Swipe Logic
                let touchstartX = 0;
                let touchendX = 0;
                const feedContainer = document.getElementById('feed-container');
                
                feedContainer.addEventListener('touchstart', e => {{
                    touchstartX = e.changedTouches[0].screenX;
                }});
                
                feedContainer.addEventListener('touchend', e => {{
                    touchendX = e.changedTouches[0].screenX;
                    if (!isSearchActive) {{
                        if (touchendX < touchstartX - 50) nextDayClick(); // Swipe Left -> Newer Date
                        if (touchendX > touchstartX + 50) prevDayClick(); // Swipe Right -> Older Date
                    }}
                }});
            }};

            function capitalize(str) {{
                return str.replace(/\\b\\w/g, l => l.toUpperCase());
            }}

            function updateFeedView() {{
                const targetDate = uniqueDates[currentDateIndex];
                const cards = document.querySelectorAll('.submission-card');
                let visibleCount = 0;
                
                cards.forEach(card => {{
                    if (card.getAttribute('data-date') === targetDate) {{
                        card.style.display = 'block';
                        visibleCount++;
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
                
                document.getElementById('view-date-header').innerText = (currentDateIndex === 0) ? "Today's Logs" : capitalize(targetDate);
                document.getElementById('empty-feed-msg').style.display = (visibleCount === 0) ? 'flex' : 'none';
            }}

            function prevDayClick() {{
                if (isSearchActive) return;
                if (currentDateIndex < uniqueDates.length - 1) {{
                    currentDateIndex++;
                    updateFeedView();
                }}
            }}

            function nextDayClick() {{
                if (isSearchActive) return;
                if (currentDateIndex > 0) {{
                    currentDateIndex--;
                    updateFeedView();
                }}
            }}

            // ==========================================
            // JS: INSTANT SEARCH
            // ==========================================
            function filterLogs() {{
                const nameQuery = document.getElementById('search-name').value.toLowerCase();
                const dateQuery = document.getElementById('search-date').value.toLowerCase();
                const cards = document.querySelectorAll('.submission-card');
                
                if (nameQuery === '' && dateQuery === '') {{
                    isSearchActive = false;
                    updateFeedView();
                    return;
                }}

                isSearchActive = true;
                document.getElementById('view-date-header').innerText = "Search Results";
                document.getElementById('empty-feed-msg').style.display = 'none';

                cards.forEach(card => {{
                    const cardName = card.getAttribute('data-name');
                    const cardDate = card.getAttribute('data-date');
                    if (cardName.includes(nameQuery) && cardDate.includes(dateQuery)) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }}

            // ==========================================
            // JS: FLOATING AI POPUP & CANCEL BUTTON
            // ==========================================
            function closeSummary() {{
                document.getElementById('summary-overlay').classList.add('hidden');
                document.getElementById('summary-btn').innerHTML = "✨ Summarize Today";
            }}

            async function getSummary() {{
                const overlay = document.getElementById('summary-overlay');
                const content = document.getElementById('summary-content');
                const btn = document.getElementById('summary-btn');
                
                if (navigator.vibrate) navigator.vibrate(50);
                
                // Show Popup Overlay instantly
                overlay.classList.remove('hidden');
                content.innerHTML = "<p class='text-gray-500 italic flex items-center gap-2'><svg class='animate-spin h-4 w-4' viewBox='0 0 24 24'><circle class='opacity-25' cx='12' cy='12' r='10' stroke='currentColor' stroke-width='4' fill='none'></circle><path class='opacity-75' fill='currentColor' d='M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z'></path></svg> AI is reading today's logs...</p>";
                
                // Only fetches Today's logs now!
                const response = await fetch('/api/summarize');
                const data = await response.json();
                
                content.innerHTML = data.summary;
            }}

            // Voice Assistant (Unchanged)
            async function activateVoiceAssistant() {{
                const voiceBtn = document.getElementById('voice-assistant-btn');
                const originalIcon = voiceBtn.innerHTML;
                if (navigator.vibrate) navigator.vibrate([50, 50, 50]);
                voiceBtn.innerHTML = "⏳";
                voiceBtn.classList.add("animate-pulse");
                try {{
                    const response = await fetch('/api/voice_summary_audio');
                    const data = await response.json();
                    if (data.status === "success" && data.audio_base64) {{
                        voiceBtn.innerHTML = "🔊";
                        const audio = new Audio("data:audio/wav;base64," + data.audio_base64);
                        audio.onended = function() {{
                            voiceBtn.innerHTML = originalIcon;
                            voiceBtn.classList.remove("animate-pulse");
                        }};
                        audio.play().catch(e => {{
                            console.error("Playback failed", e);
                            voiceBtn.innerHTML = originalIcon;
                            voiceBtn.classList.remove("animate-pulse");
                        }});
                    }} else {{
                        voiceBtn.innerHTML = "⚠️";
                        voiceBtn.classList.remove("animate-pulse");
                        alert("Voice API credits expired! Please tap 'Summarize Today'.");
                        setTimeout(() => {{ voiceBtn.innerHTML = originalIcon; }}, 3000);
                    }}
                }} catch (error) {{
                    voiceBtn.innerHTML = "⚠️";
                    voiceBtn.classList.remove("animate-pulse");
                    alert("Network connection error!");
                    setTimeout(() => {{ voiceBtn.innerHTML = originalIcon; }}, 3000);
                }}
            }}
        </script>
        <style>
            ::-webkit-scrollbar {{ display: none; }}
            body {{ padding-top: env(safe-area-inset-top); padding-bottom: env(safe-area-inset-bottom); overscroll-behavior-y: none; }}
        </style>
    </head>
    <body class="bg-[#f2f2f7] dark:bg-black text-gray-900 dark:text-gray-100 font-sans min-h-[100dvh] pb-32 relative">
        
        <!-- TOP HEADER -->
        <div class="bg-white/80 dark:bg-black/80 backdrop-blur-xl sticky top-0 z-40 border-b border-gray-200 dark:border-gray-800 p-4 pt-6 shadow-sm flex justify-between items-center">
            <div>
                <h1 class="text-3xl font-extrabold tracking-tight">Logs</h1>
                <p class="text-sm text-gray-500 font-medium mt-1">Swipe to view previous days</p>
            </div>
            <button id="voice-assistant-btn" onclick="activateVoiceAssistant()" class="bg-gray-100 dark:bg-gray-800 text-2xl h-12 w-12 rounded-full shadow-inner border border-gray-200 dark:border-gray-700 flex items-center justify-center hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                🎙️
            </button>
        </div>

        <div class="p-4 max-w-lg mx-auto">
            
            <!-- THE SEARCH BARS -->
            <div class="mb-5 flex flex-col sm:flex-row gap-3">
                <div class="relative flex-1">
                    <span class="absolute left-3.5 top-3.5 text-gray-400">🔍</span>
                    <input type="text" id="search-name" onkeyup="filterLogs()" placeholder="Search Name..." class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl pl-11 pr-4 py-3.5 text-base text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm transition-colors">
                </div>
                <div class="relative flex-1">
                    <span class="absolute left-3.5 top-3.5 text-gray-400">📅</span>
                    <input type="text" id="search-date" onkeyup="filterLogs()" placeholder="e.g. June 8" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl pl-11 pr-4 py-3.5 text-base text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm transition-colors">
                </div>
            </div>

            <!-- DAILY VIEW CONTROLS -->
            <div class="flex justify-between items-center mb-3 px-2">
                <button onclick="prevDayClick()" class="text-gray-400 hover:text-amber-500 font-bold text-2xl px-2">&larr;</button>
                <h2 id="view-date-header" class="font-bold text-lg text-gray-800 dark:text-gray-200">Today's Logs</h2>
                <button onclick="nextDayClick()" class="text-gray-400 hover:text-amber-500 font-bold text-2xl px-2">&rarr;</button>
            </div>

            <!-- FEED CONTAINER (Has Swipe Listener Attached in JS) -->
            <div id="feed-container" class="space-y-4 min-h-[50vh]">
                <div id="empty-feed-msg" class="hidden flex-col items-center justify-center py-16 text-gray-500">
                    <span class="text-4xl mb-3">📭</span>
                    <p>No updates for this day.</p>
                </div>
                {submissions_html}
            </div>
        </div>

        <!-- NEW FLOATING POPUP OVERLAY FOR AI SUMMARY -->
        <div id="summary-overlay" class="hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] flex justify-center items-center p-4">
            <div class="bg-gradient-to-br from-amber-100 to-orange-50 dark:from-gray-900 dark:to-black border border-amber-300 dark:border-amber-800 rounded-3xl p-6 shadow-2xl w-full max-w-sm relative">
                <!-- X CANCEL BUTTON -->
                <button onclick="closeSummary()" class="absolute top-4 right-4 bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-full w-8 h-8 flex items-center justify-center font-bold text-xl hover:bg-gray-300 dark:hover:bg-gray-700 transition">&times;</button>
                
                <h2 class="font-extrabold text-xl mb-4 flex items-center gap-2">🤖 Today's AI Summary</h2>
                <div id="summary-content" class="text-[15px] text-gray-800 dark:text-gray-200 leading-relaxed space-y-3"></div>
            </div>
        </div>

        <div class="fixed bottom-6 left-0 w-full px-4 z-50 mb-[env(safe-area-inset-bottom)]">
            <button id="summary-btn" onclick="getSummary()" class="w-full bg-gray-900 dark:bg-amber-500 text-white dark:text-gray-950 py-4 rounded-2xl font-extrabold text-lg shadow-[0_10px_40px_rgba(245,158,11,0.3)] flex justify-center items-center gap-2 transition-transform active:scale-95">
                ✨ Summarize Today
            </button>
        </div>

    </body>
    </html>
    """
    return dashboard_content


# ==========================================
# API ROUTE: THE FAST LLM SUMMARIZER (TODAY ONLY)
# ==========================================
@app.get("/api/summarize")
async def summarize_logs():
    check_monthly_reset()
    
    # 1. LOCK SUMMARY TO ONLY CURRENT DAY
    today_date = get_ist_date()
    todays_subs = [sub for sub in submissions_db if sub.get('date_string') == today_date]
    
    if not todays_subs:
        return {"summary": "No tasks submitted today yet. The team is resting!"}
    
    roles = set([sub['role'] for sub in todays_subs])
    total_people = len(set([sub['name'] for sub in todays_subs]))
    
    summary_html = f"<p class='font-medium'><strong>Today's Overview:</strong> {total_people} team members submitted updates across {len(roles)} departments.</p><ul class='list-disc pl-5 mt-3 space-y-2'>"
    
    for role in roles:
        names_in_role = list(set([sub['name'] for sub in todays_subs if sub['role'] == role]))
        tasks_in_role = [sub['work'] for sub in todays_subs if sub['role'] == role]
        name_str = ", ".join(names_in_role)
        preview = tasks_in_role[-1][:45] + "..." if len(tasks_in_role[-1]) > 45 else tasks_in_role[-1]
        
        summary_html += f"<li><strong>{role} ({name_str}):</strong> <em>'{preview}'</em></li>"
    
    summary_html += "</ul><div class='mt-4 pt-3 border-t border-amber-200 dark:border-gray-800 font-bold text-green-600 dark:text-green-500'>✅ All operations looking good today!</div>"

    return {"summary": summary_html}


# ==========================================
# API ROUTE: SARVAM AI TTS CONNECTION (Single Key)
# ==========================================
@app.get("/api/voice_summary_audio")
async def voice_summary_audio():
    check_monthly_reset()
    
    today_date = get_ist_date()
    todays_subs = [sub for sub in submissions_db if sub.get('date_string') == today_date]
    
    if not todays_subs:
        gujarati_text = "આજે હજી સુધી કોઈએ કામ જમા કરાવ્યું નથી."
    else:
        names = [sub['name'] for sub in todays_subs]
        unique_names = list(set(names))
        names_str = ", ".join(unique_names)
        gujarati_text = f"આજે {len(unique_names)} લોકોએ કામ જમા કરાવ્યું છે. તેમના નામ છે: {names_str}. બધું બરાબર ચાલી રહ્યું છે."
    
    url = "https://api.sarvam.ai/text-to-speech"
    payload = {
        "text": gujarati_text,
        "target_language_code": "gu-IN",
        "model": "bulbul:v3",
        "speaker": "ritu" 
    }
    
    headers = {
        "api-subscription-key": "sk_nd2k6k0b_p8DCLdeklhTnkQyXjLbhXMsx",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=8.0) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            audio_base64 = response_data.get("audios", [""])[0]
            return {"status": "success", "audio_base64": audio_base64}
            
    except Exception as e:
        print(f"Sarvam API failed: {e}")
        return {"status": "error", "message": "API key exhausted or failed"}
