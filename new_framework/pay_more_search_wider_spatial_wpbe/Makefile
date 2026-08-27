PYTHON ?= python
PYTHONPATH := src
RUN_OUT := outputs/spatial_pickup_wpbe_v4

.PHONY: test quick numerics seed-formal-results audit group-note

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -p 'test_spatial_wpbe.py' -v

quick:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/run_spatial_wpbe_numerics.py --quick --no-resume --workers 1

numerics:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/run_spatial_wpbe_numerics.py --no-resume

seed-formal-results:
	mkdir -p $(RUN_OUT)/csv $(RUN_OUT)/audit
	cp results/csv/optimized_grid.csv $(RUN_OUT)/csv/optimized_grid.csv
	cp results/metadata.json $(RUN_OUT)/metadata.json

audit: seed-formal-results
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/audit_spatial_wpbe.py

group-note:
	latexmk -cd -pdf -interaction=nonstopmode -halt-on-error -outdir=build group_meeting/group_meeting_spatial_pickup_extension.tex
	cp group_meeting/build/group_meeting_spatial_pickup_extension.pdf group_meeting/group_meeting_spatial_pickup_extension.pdf
	$(PYTHON) group_meeting/merge_group_meeting_spatial.py
