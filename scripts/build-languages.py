"""Compatibility entry point. The bilingual site is now built from content/ sources."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('build-site.py')),run_name='__main__')
