#!/bin/bash

YYYYMMDD=$(date +%Y%m%d)

podman build --tag gemini-vision-ui:${YYYYMMDD} .
