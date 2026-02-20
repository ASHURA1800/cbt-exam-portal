@echo off
title CBT Exam Portal v15
color 0A
echo.
echo  ============================================
echo   CBT Exam Portal v15 — Starting...
echo  ============================================
echo.
echo  Installing required packages...
pip install streamlit --quiet
echo.
echo  Starting CBT Portal...
echo  Open your browser to: http://localhost:8501
echo.
streamlit run bank_exam_app.py --server.port 8501 --server.headless false
pause
