PYTHON ?= python
PYTHONPATH := src

.PHONY: test quick numerics free-search audit figures group-note all

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -p 'test_spatial_wpbe.py' -v

quick:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/run_regime_numerics.py \
		--quick --main-slice-only --workers 1 --kappa 0.0125 --retention 0.8 \
		--output results/csv/regime_comparison_quick.csv \
		--metadata results/regime_metadata_quick.json

numerics:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/run_regime_numerics.py \
		--workers 1 --kappa 0.0125 --retention 0.8

free-search:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/run_regime_numerics.py \
		--main-slice-only --workers 1 --kappa 0 --retention 0.8 \
		--output results/csv/regime_comparison_free_search.csv \
		--metadata results/regime_metadata_free_search.json

audit:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/audit_regime_results.py

figures:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/plot_regime_comparison.py

group-note:
	latexmk -cd -pdf -interaction=nonstopmode -halt-on-error -outdir=build group_meeting/group_meeting_spatial_pickup_extension.tex
	cp group_meeting/build/group_meeting_spatial_pickup_extension.pdf group_meeting/group_meeting_spatial_pickup_extension.pdf
	$(PYTHON) group_meeting/merge_group_meeting_spatial.py

all: test numerics free-search audit figures group-note
