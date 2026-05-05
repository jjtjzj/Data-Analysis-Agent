@echo off
SET GIT="C:\Users\JunZhang\AppData\Local\GitHubDesktop\app-3.5.8\resources\app\git\cmd\git.exe"

echo Amending commit message...
%GIT% commit --amend -m "Commit 3: Basic LLM Integration"

echo Force pushing to GitHub...
%GIT% push origin main --force

echo Done!
pause
