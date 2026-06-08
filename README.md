ADV Standup Engine: Documentation
1. Overview
The ADV Standup Engine is a lightweight, mobile-first web application designed to streamline daily standup reporting for our 12-person IT department. It replaces manual WhatsApp messaging with a structured, AI-enhanced submission and summary system.

2. Key Features
Submission Portal: Mobile-friendly form with voice-to-text input (Gujarati/English).

Automated Role Mapping: Smart dropdowns that auto-populate roles.

Monthly Ledger: Automatic monthly data reset on the 1st of each month.

AI Summarization: One-click summary of today's work.

Natural Voice Reporting: Integration with Sarvam AI for human-like Gujarati voice summaries.

3. Deployment & Maintenance (The "How-To")
This project is deployed on Vercel using a Python FastAPI runtime.

Repository: [https://github.com/teeth-vton/daily-standup-app.git]

Live Dashboard: [https://daily-standup-app.vercel.app/dashboard]

How to update the API Key (When credits expire):
Navigate to api/index.py in your GitHub repository.

Scroll to the voice_summary_audio function at the bottom.

Locate the headers dictionary:

Python
headers = {
    "api-subscription-key": "PASTE_YOUR_NEW_KEY_HERE", 
    "Content-Type": "application/json"
}
Commit the changes. Vercel will automatically redeploy the new key within 60 seconds.

4. Technical Architecture
Frontend: Tailwind CSS (Mobile-responsive, dark mode supported).

Backend: FastAPI (Serverless Python functions).

Database: Temporary in-memory state (resets monthly).

Voice Engine: Sarvam AI bulbul:v3 model.
