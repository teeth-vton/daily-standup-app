from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# HTML Template with styling embedded directly for seamless Vercel deployment
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IT Dept - Daily Standup</title>
    <script src="https://tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-100 font-sans min-h-screen flex items-center justify-center p-4">

    <div class="bg-gray-800 p-8 rounded-2xl shadow-2xl w-full max-w-lg border border-gray-700">
        <div class="flex items-center space-x-3 mb-6">
            <span class="text-3xl">🚀</span>
            <div>
                <h1 class="text-2xl font-bold tracking-tight">Daily Standup</h1>
                <p class="text-sm text-gray-400">Submit your work updates below</p>
            </div>
        </div>

        <form action="/submit" method="POST" class="space-y-5">
            <!-- Employee Selection -->
            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Your Name</label>
                <select name="name" required class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500">
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
                <label class="block text-sm font-semibold text-gray-300 mb-2">Department Role</label>
                <select name="role" required class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-indigo-500">
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
                <label class="block text-sm font-semibold text-gray-300 mb-2">What did you achieve today?</label>
                <textarea name="work_done" required rows="4" placeholder="List your tasks, bugs fixed, or assets created..." class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2.5 text-white placeholder-gray-400 focus:outline-none focus:border-indigo-500"></textarea>
            </div>

            <!-- Submit Button -->
            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-4 rounded-lg transition duration-200 shadow-lg shadow-indigo-600/20">
                Submit Update
            </button>
        </form>
    </div>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return HTML_CONTENT

@app.post("/submit")
async def handle_submit(name: str = Form(...), role: str = Form(...), work_done: str = Form(...)):
    # This acts as our temporary confirmation page
    return {
        "status": "success",
        "team_member": name,
        "role": role,
        "work_done": work_done,
        "message": "Data reached the Vercel backend successfully!"
    }
