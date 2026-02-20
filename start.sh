#!/bin/bash
echo ""
echo " ============================================"
echo "  CBT Exam Portal v15 — Starting..."
echo " ============================================"
echo ""
pip install streamlit --quiet 2>/dev/null
echo " Starting CBT Portal..."
echo " Open browser to: http://localhost:8501"
echo ""
streamlit run bank_exam_app.py --server.port 8501
