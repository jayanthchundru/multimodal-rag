#!/bin/bash

cd /data/jiang/chundrja/projects/multimodal-rag

source .venv/bin/activate

# Just use python, not uv run
python /home/chundrja/Deep_learning/multimodal-rag/data/pdf_to_img.py \
  --pdf-folder ./financebench/pdfs \
  --output-folder ./data/images \
  --dpi 150