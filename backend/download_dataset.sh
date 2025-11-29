#!/usr/bin/env bash
set -e
echo "This script will attempt to download the IndicAccentDb dataset from Hugging Face."
echo "Make sure git-lfs is installed and you have enough disk space."
mkdir -p data
cd data
git lfs install || true
if [ -d IndicAccentDb ]; then
  echo "IndicAccentDb already exists in backend/data."
  exit 0
fi
git clone https://huggingface.co/datasets/DarshanaS/IndicAccentDb
echo "Download finished. Dataset is in backend/data/IndicAccentDb"
