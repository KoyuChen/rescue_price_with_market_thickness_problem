PYTHON ?= python

.PHONY: formal formal-figures formal-clean group group-clean empirical-test mixed-test paper figure test quick clean

formal-figures:
	PYTHONPATH=code $(PYTHON) paper/formal/scripts/generate_theory_outputs.py

formal:
	cd paper/formal && TEXINPUTS=..: BSTINPUTS=..: latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

formal-clean:
	cd paper/formal && TEXINPUTS=..: BSTINPUTS=..: latexmk -c main.tex

group:
	cd group_meeting && latexmk -pdf -interaction=nonstopmode -halt-on-error group_meeting_market_thickness.tex
	cp group_meeting/group_meeting_market_thickness.pdf output/pdf/group_meeting_market_thickness.pdf

group-clean:
	cd group_meeting && latexmk -c group_meeting_market_thickness.tex

empirical-test:
	$(PYTHON) -m unittest discover -s empirical/tests -p 'test_*.py' -v
	$(PYTHON) empirical/src/calibration_contract.py --synthetic

mixed-test:
	PYTHONPATH=code $(PYTHON) code/check_mixed_supply_theorems.py

paper: formal

figure:
	cd figures && latexmk -pdf -interaction=nonstopmode -halt-on-error extensive_form_diagram.tex

test:
	PYTHONPATH=code $(PYTHON) -m unittest discover -s code -p 'test_*.py' -v
	PYTHONPATH=code $(PYTHON) code/check_mixed_supply_theorems.py

quick:
	PYTHONPATH=code $(PYTHON) code/run_discount_falsification.py --quick

clean: formal-clean group-clean
	cd figures && latexmk -c extensive_form_diagram.tex
