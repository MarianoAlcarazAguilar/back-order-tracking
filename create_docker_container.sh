#! /bin/bash
docker run -d \
--name bo-container \
-p 80:8501 \
-v bo-volume:/app/data \
bo-image:v1