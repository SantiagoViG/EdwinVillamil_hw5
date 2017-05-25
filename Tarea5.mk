depencircuitoRC=Best_Fit.png Histograma_C.png Histograma_R.png Verosimilitud_C.png Verosimilitud_R.png

circuitoRC.py:CircuitoRC.txt
	python circuitoRC.py
	pdflatex Resultados_hw5.tex

depencircuitoRC:circuitoRC.py
	python circuitoRC.py

Resultados_hw5.pdf:Resultados_hw5.tex depencircuitoRC
	pdflatex Resultados_hw5.tex
