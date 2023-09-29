#! /bin/bash
docker run -d \
--name bo-container \
-p 80:8501 \
bo-image:v1