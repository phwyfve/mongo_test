"""
Command registry for shell tools
Maps command names to their handler functions
"""

from .MergePdfs import merge_pdfs

# Command registry - maps shell command names to handler functions
commands = {
    "MergePdfs": merge_pdfs
}
