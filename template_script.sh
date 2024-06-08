#!/bin/bash

export GEMINI_MODEL=gemini-1.5-flash
export GEMINI_API_KEY=

streamlit run src/vision-ui.py \
    --browser.gatherUsageStats=false \
    --server.maxUploadSize 20
