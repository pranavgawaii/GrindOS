"""
merge.py — Legacy utility (kept for reference).

Since build.py now outputs each subject directly as a single
GrindOS_<SUBJECT>_Booklet.pdf into output/, this script is
no longer needed for normal workflow.

To regenerate any booklet, just run:
    python build.py <subject>       # e.g. python build.py sql
    python build.py all             # rebuild everything

Output will appear in:
    notes/output/GrindOS_<SUBJECT>_Booklet.pdf
"""
print("ℹ️  merge.py is no longer needed.")
print("    Run: python build.py <subject>  to rebuild a booklet.")
print("    Run: python build.py all        to rebuild all booklets.")
