#/bin/bash
latex ReportTCDB.tex
latex ReportTCDB.tex
bibtex ReportTCDB
latex ReportTCDB.tex
latex ReportTCDB.tex
dvipdfm -p a4 ReportTCDB.dvi



