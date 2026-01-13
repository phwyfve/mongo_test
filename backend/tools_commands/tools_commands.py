"""
Command registry for shell tools
Maps command names to their handler functions
"""

from .MergePdfs import merge_pdfs
from .SplitPdfs import split_pdfs
from .MergeImages import merge_images

# Command registry - maps shell command names to handler functions
COMMAND_REGISTRY = {
    "MergePdfs": merge_pdfs,
    "SplitPdfs": split_pdfs,
    "MergeImages": merge_images
}
