#!/bin/bash

export GEMINI_MODEL=gemini-pro-vision
export GEMINI_API_KEY=

streamlit run src/vision-ui.py \
    --browser.gatherUsageStats=false \
    --server.maxUploadSize 20
