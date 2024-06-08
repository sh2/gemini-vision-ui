#!/bin/bash

podman run \
        --detach \
        --restart=always \
        --publish=8501:8501 \
        --env=GEMINI_MODEL=gemini-1.5-flash \
        --env=GEMINI_API_KEY= \
        --name=gemini-vision-ui \
        gemini-vision-ui:20240101
