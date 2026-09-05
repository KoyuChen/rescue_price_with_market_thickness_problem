.PHONY: test smoke help

test:
	OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest discover -s tests -v

smoke:
	OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m rescue_solver menu --m 1 --p1 .3 --p2 .5 --config configs/small.json --smoke --route-seed 42 --selection-markets 1000 --report-markets 2000 --output runs/make_smoke; rc=$$?; test $$rc -eq 0 -o $$rc -eq 2

help:
	python -m rescue_solver --help
