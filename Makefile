.PHONY: paper figure test quick clean

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error announced_escalation_theory_overhaul.tex

figure:
	cd figures && latexmk -pdf -interaction=nonstopmode -halt-on-error extensive_form_diagram.tex

test:
	PYTHONPATH=code python -m unittest discover -s code -p 'test_*.py' -v

quick:
	PYTHONPATH=code python code/run_discount_falsification.py --quick

clean:
	cd paper && latexmk -c announced_escalation_theory_overhaul.tex
	cd figures && latexmk -c extensive_form_diagram.tex
