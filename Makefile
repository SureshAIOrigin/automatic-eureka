# Makefile for automatic-eureka

.PHONY: check check-python check-bash help

help:
	@echo "Available targets:"
	@echo "  make check        - Run system check (Python version)"
	@echo "  make check-python - Run system check (Python version)"
	@echo "  make check-bash   - Run system check (Bash version)"
	@echo "  make help         - Show this help message"

check: check-python

check-python:
	@python3 system_check.py

check-bash:
	@./system_check.sh
