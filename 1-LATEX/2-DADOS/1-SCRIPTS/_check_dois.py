# -*- coding: utf-8 -*-
"""Quick check: DOI extraction from The-Zo-perspective and s13412 PDFs."""
import os, fitz, re

PDF_DIR = r"\\?\ ".strip() + r"c:\Users\vidal\OneDrive\Documentos\13 - CLONEGIT\artigo_2_catuxe\1-LATEX\2-DADOS\2-BANCO_DADOS\1-ARTIGOS_SELECIONADOS"
doi_pat = re.compile(r"10\.\d{4,9}/[^\s,;>)\]]+")

# Check The-Zo-perspective for DOI in ALL pages
for f in os.listdir(PDF_DIR):
    if f.startswith("The-Zo"):
        print(f"=== {f[:60]} ===")
        doc = fitz.open(os.path.join(PDF_DIR, f))
        for i, page in enumerate(doc):
            text = page.get_text()
            dois = doi_pat.findall(text)
            if dois:
                for d in set(dois):
                    print(f"  Page {i+1}: {d.rstrip('.')}")
        # Also show first page title area
        first_text = doc[0].get_text()[:600]
        print(f"\nFirst page text (600 chars):")
        print(first_text)
        doc.close()
        break

print("\n" + "="*60)

# Check s13412 title/author
for f in os.listdir(PDF_DIR):
    if f.startswith("s13412"):
        print(f"\n=== {f} ===")
        doc = fitz.open(os.path.join(PDF_DIR, f))
        text = doc[0].get_text()[:600]
        print(text)
        dois = doi_pat.findall(text)
        print(f"DOIs found: {dois}")
        doc.close()
        break
