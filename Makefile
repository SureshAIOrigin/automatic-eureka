.PHONY: check help

check:
	@echo "Running system checks..."
	@python3 system_check.py

help:
	@echo "Available targets:"
	@echo "  make check  - Run system validation checks"
	@echo "  make help   - Show this help message"
