#!/bin/bash
if [ "$DOWNLOAD" = "true" ]; then
  git clone https://huggingface.co/pharmbio/ptp /app/inference/models && \
  cd /app/inference/models && \
  git lfs pull
else
  echo "noop"
fi
exit 0