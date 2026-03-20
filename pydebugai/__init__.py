"""
PyDebugAI — AI-powered Python debugging assistant.
Like ChatGPT, but exclusively for debugging Python code.
"""

__version__ = "0.1.0"
__author__ = "PyDebugAI Team"

from .models import Diagnostic, Suggestion, AnalysisResult

__all__ = ["Diagnostic", "Suggestion", "AnalysisResult", "__version__"]
