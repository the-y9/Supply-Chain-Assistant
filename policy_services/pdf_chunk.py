# policy_services/pdf_chunk.py
import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

import re

def is_title_case(s):
    # Check if the string is mostly title case words (ignoring small words)
    words = s.split()
    if not words:
        return False
    
    if words[0][0].islower():
        return False
    # Consider small words like 'and', 'of', 'the' as exceptions
    small_words = {'and', 'or', 'the', 'in', 'on', 'at', 'to', 'a', 'an', 'for', 'by'}
    title_case_words = [w for w in words if w[0].isupper() and (w.lower() not in small_words)]
    return len(title_case_words) >= max(1, len(words) // 2)  # majority words title case

def chunk(text, overlap_lines=1):
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    heading_block = []
    in_heading_block = True
    prev_chunk_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if in_heading_block:
            if is_title_case(line):
                heading_block.append(line)
            else:
                in_heading_block = False
                if heading_block:
                    chunks.append('\n'.join(heading_block).strip())
                    current_chunk = prev_chunk_lines[-overlap_lines:] + [line]
        else:
            if is_title_case(line):
                # Save previous chunk
                if current_chunk:
                    chunks.append('\n'.join(current_chunk).strip())
                    prev_chunk_lines = current_chunk.copy()
                current_chunk = prev_chunk_lines[-overlap_lines:] + [line]
            else:
                current_chunk.append(line)

    # Final chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk).strip())
    elif heading_block:
        chunks.append('\n'.join(heading_block).strip())

    return chunks

# Directory path
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_dir = os.path.join(script_dir, "..", "Policy Docs")
all_chunks = []

for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        full_path = os.path.join(pdf_dir, filename)
        text = extract_text_from_pdf(full_path)
        chunks = chunk(text)
        
        for idx, chunk_text in enumerate(chunks):
            all_chunks.append({
                "filename": filename,
                "chunk_id": idx,
                "text": chunk_text
            })
