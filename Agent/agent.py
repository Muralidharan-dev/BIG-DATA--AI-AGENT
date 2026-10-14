"""Command-line launcher for the OTT Airflow pipeline."""

import argparse
import shutil
import subprocess
import sys


DAG_ID = "ott_pipeline_dag"


def trigger_pipeline() -> int:
    """Trigger the OTT DAG using the configured Airflow installation."""
    airflow = shutil.which("airflow")
    if airflow is None:
        print(
            "Airflow CLI was not found. Install/configure Airflow and run this "
            "agent in the Airflow environment.",
            file=sys.stderr,
        )
        return 1

    command = [airflow, "dags", "trigger", DAG_ID]
    print(f"Triggering Airflow DAG '{DAG_ID}'...")

    try:
        result = subprocess.run(command, check=False, text=True, capture_output=True)
    except OSError as error:
        print(f"Could not run the Airflow CLI: {error}", file=sys.stderr)
        return 1

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    if result.returncode != 0:
        print(
            f"Airflow failed to trigger DAG '{DAG_ID}' "
            f"(exit code {result.returncode}).",
            file=sys.stderr,
        )
        return result.returncode

    if not result.stdout:
        print(f"Airflow accepted the trigger request for '{DAG_ID}'.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Trigger the OTT data pipeline in Apache Airflow."
    )
    parser.parse_args()
    return trigger_pipeline()


if __name__ == "__main__":
    raise SystemExit(main())
