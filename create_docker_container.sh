#! /bin/bash
docker run -d \
--name bo-container \
-p 8080:8501 \
-v bo-volume:/app/data \
bo-image:latest