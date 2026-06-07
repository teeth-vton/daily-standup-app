from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT Dept - Daily Standup</title>
    <script src="https://tailwindcss.com"></script>
    <style>
        /* Custom animation for the slow rainbow glowing divider line */
        @keyframes rainbowGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .rainbow-line {
            background: linear-gradient(90deg, #d4af37, #f39c12, #9b59b6, #3498db, #2ecc71, #d4af37);
            background-size: 400% 400%;
            animation: rainbowGlow 12s ease infinite;
        }
    </style>
    <script>
        tailwind.config = {
            darkMode: 'class'
        }
        
        function toggleTheme() {
            const html = document.documentElement;
            const btn = document.getElementById('theme-btn');
            
            if (html.classList.contains('dark')) {
                // Switch to LIGHT mode
                html.classList.remove('dark');
                btn.innerHTML = '<span class="text-black text-xl">☀️</span>';
                btn.className = "bg-white border border-gray-300 rounded-full w-12 h-12 flex items-center justify-center shadow-md hover:bg-gray-100 transition duration-300";
            } else {
                // Switch to DARK mode (Default)
                html.classList.add('dark');
                btn.innerHTML = '<span class="text-white text-xl">🌙</span>';
                btn.className = "bg-gray-800 border border-gray-700 rounded-full w-12 h-12 flex items-center justify-center shadow-md hover:bg-gray-700 transition duration-300";
            }
        }
    </script>
</head>
<body class="bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100 font-sans min-h-screen flex flex-col items-center justify-center p-4 transition-colors duration-500">

    <!-- Theme Toggle Button: Positioned Top-Right on Desktop, Safe and Accessible on Mobile -->
    <div class="absolute top-4 right-4 sm:top-6 sm:right-6 z-50">
        <button id="theme-btn" onclick="toggleTheme()" class="bg-gray-800 border border-gray-700 rounded-full w-12 h-12 flex items-center justify-center shadow-md hover:bg-gray-700 transition duration-300">
            <span class="text-white text-xl">🌙</span>
        </button>
    </div>

    <!-- Main Container Card -->
    <div class="bg-white dark:bg-gray-900 w-full max-w-md rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800 overflow-hidden transition-colors duration-500 my-12">
        
        <!-- Big Giant Rainbow Glowing Line (Remains constant in both modes) -->
        <div class="rainbow-line h-3.5 w-full"></div>

        <div class="p-6 sm:p-8">
            <!-- Header -->
            <div class="flex items-center space-x-3 mb-6">
                <span class="text-3xl">🚀</span>
                <div>
                    <h1 class="text-2xl font-bold tracking-tight">Daily Standup</h1>
                    <p class="text-sm text-gray-500 dark:text-gray-400">Submit your work updates below</p>
                </div>
            </div>

            <!-- Form -->
            <form action="/submit" method="POST" class="space-y-5">
                <!-- Employee Selection -->
                <div>
                    <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Your Name</label>
                    <select name="name" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 transition duration-300">
                        <option value="" disabled selected>Select your name</option>
                        <option value="Manager">Manager</option>
                        <option value="Coder 1">Coder 1</option>
                        <option value="Coder 2">Coder 2</option>
                        <option value="SEO Handler">SEO Handler</option>
                        <option value="UX/UI Designer">UX/UI Designer</option>
                        <option value="Video Editor">Video Editor</option>
                        <option value="Photo Editor">Photo Editor</option>
                    </select>
                </div>

                <!-- Role Selection -->
                <div>
                    <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Department Role</label>
                    <select name="role" required class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 transition duration-300">
                        <option value="" disabled selected>Select your track</option>
                        <option value="Management">Management</option>
                        <option value="Coding">Coding</option>
                        <option value="SEO & Marketing">SEO & Marketing</option>
                        <option value="UX/UI Design">UX/UI Design</option>
                        <option value="Video Production">Video Production</option>
                        <option value="Photo Editing">Photo Editing</option>
                    </select>
                </div>

                <!-- Task Input -->
                <div>
                    <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">What did you achieve today?</label>
                    <textarea name="work_done" required rows="4" placeholder="List your tasks, bugs fixed, or assets created..." class="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 transition duration-300"></textarea>
                </div>

                <!-- Submit Button -->
                <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-gray-950 font-bold py-3.5 px-4 rounded-xl transition duration-300 shadow-lg shadow-amber-500/10 hover:shadow-amber-500/20 transform active:scale-[0.98]">
                    Submit Update
                </button>
            </form>
        </div>
    </div>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return HTML_CONTENT

@app.post("/submit")
async def handle_submit(name: str = Form(...), role: str = Form(...), work_done: str = Form(...)):
    return {
        "status": "success",
        "team_member": name,
        "role": role,
        "work_done": work_done,
        "message": "Data reached the Vercel backend successfully!"
    }
