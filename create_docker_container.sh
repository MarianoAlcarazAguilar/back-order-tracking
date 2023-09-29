#! /bin/bash
docker run -d \
--name bo-container \
-p 443:8501 \
bo-image:v1