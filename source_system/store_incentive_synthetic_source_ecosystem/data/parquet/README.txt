Parquet outputs are generated locally from the supplied JSONL files.
The generation environment used to assemble this archive did not include a Parquet engine.
From the package root, install requirements and run:
    pip install -r requirements.txt
    python python/generate_parquet.py
This creates customer_behavior_events.parquet and employee_activity_events.parquet here.
