install py libs:
	pip install -r requirement.txt

run server:
	uvicorn tweepysetup:app --reload
