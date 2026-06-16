#!/usr/bin/env python3
"""Extract PKD stories from markdown collections"""
import re
import json
import os
from pathlib import Path

# Story collection files
files = [
    "C:\QueryPat\database\extracted_markdown\DOC_ARCH_OCEANOFPDF_COM_SELECTED_STORIES_OF_PHILI.md",
    "C:\QueryPat\database\extracted_markdown\DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_.md",
    "C:\QueryPat\database\extracted_markdown\DOC_ARCH_OCEANOFPDF_COM_THE_SHORT_HAPPY_LIFE_OF_T.md",
]

# Read first file to understand structure
with open(files[0], 'r', encoding='utf-8') as f:
    content = f.read(100000)  # Read first 100KB
    
# Print line samples to see story structure
lines = content.split('\n')
for i, line in enumerate(lines[80:200], start=80):
    if line.strip():
        print(f"{i}: {line[:140]}")
