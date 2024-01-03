@echo on
git pull https://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@github.com/NolanMehrerDW/CCT_ImportV2.git
python -m pip install --upgrade pip
Python -m pip install pyperclip keyboard pyautogui python-time colorama rich
:restart
Python "CCT_Import.py"
echo "N"
goto restart
pause
