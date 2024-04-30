ALL_PACKAGES := src

reformat:
	isort $(ALL_PACKAGES)
	black $(ALL_PACKAGES)

lint:
	isort --check --diff $(ALL_PACKAGES)
	black --check --diff $(ALL_PACKAGES)
	flake8 $(ALL_PACKAGES)
	
run:
	streamlit run streamlit_app.py