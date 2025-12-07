"""
Command registry for shell tools
Maps command names to their handler functions
"""

from .MergePdfs import merge_pdfs

# Command registry - maps shell command names to handler functions
COMMAND_REGISTRY = {
    "MergePdfs": merge_pdfs
}
