"""Profiler demo wrapper (moved to examples/).

This imports the existing demo implementation so the examples folder contains runnable artifacts
but the main project tree stays clean.
"""

from apps.backend.examples.profiler_demo_impl import main

if __name__ == "__main__":
    main()
