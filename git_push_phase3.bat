@echo off
SET GIT="C:\Users\JunZhang\AppData\Local\GitHubDesktop\app-3.5.8\resources\app\git\cmd\git.exe"

echo Staging files...
%GIT% add agent.py app.py tools.py run_app.bat sample_data.csv

echo Committing...
%GIT% commit -m "Phase 3: Basic LLM Integration"

echo Pushing to GitHub...
%GIT% push origin main

echo Done! Check GitHub for the commit.
pause
