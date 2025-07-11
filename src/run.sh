#!/bin/bash

exec streamlit run vision-ui.py \
    --browser.gatherUsageStats=false \
    --server.baseUrlPath=/vision-gemini \
    --server.maxUploadSize 20 \
    --server.address 10.0.2.100 \
    --server.port 8501
