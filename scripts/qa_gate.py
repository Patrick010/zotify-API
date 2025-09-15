import subprocess
import sys
import re

import os

def run_command(command, **kwargs):
    """Runs a command and returns the result."""
    # Add APP_ENV=development to the environment for the command
    env = os.environ.copy()
    env["APP_ENV"] = "development"
    return subprocess.run(command, capture_output=True, text=True, env=env, **kwargs)

def run_code_quality():
    """
    Runs all Python code quality checks.
    """
    print("--- Running Code Quality Checks ---")
    all_passed = True

    # 1. Ruff
    print("\n[1/5] Running ruff...")
    result = run_command(["ruff", "check", "api/src"])
    if result.returncode != 0:
        print("❌ Ruff failed.")
        print(result.stdout)
        print(result.stderr)
        all_passed = False
    else:
        print("✅ Ruff passed.")

    # 2. Pytest
    print("\n[2/5] Running pytest with coverage...")
    result = run_command(["pytest", "--cov=api/src", "--cov-fail-under=85", "api/tests/"])
    if result.returncode != 0:
        print("❌ Pytest failed.")
        print(result.stdout)
        print(result.stderr)
        all_passed = False
    else:
        print("✅ Pytest passed.")

    # 3. Radon CC
    print("\n[3/5] Running radon for cyclomatic complexity...")
    result = run_command(["radon", "cc", "-s", "-a", "-nb", "api/src"])
    if result.returncode == 0:
        # Radon outputs the average complexity at the end. Example: "Average complexity: A (2.0)"
        match = re.search(r"Average complexity: \w+ \((\d+\.\d+)\)", result.stdout)
        if match:
            avg_complexity = float(match.group(1))
            if avg_complexity > 5.0:
                print(f"❌ Radon CC failed: Average complexity is {avg_complexity} (must be <= 5.0)")
                all_passed = False
            else:
                print(f"✅ Radon CC passed (Average complexity: {avg_complexity}).")
        else:
            # If there's no average, it means no files were complex enough to rank, which is a pass.
            print("✅ Radon CC passed (no complex files found).")
    else:
        print("❌ Radon CC failed to run.")
        print(result.stdout)
        print(result.stderr)
        all_passed = False

    # 4. Radon MI
    print("\n[4/5] Running radon for maintainability index...")
    result = run_command(["radon", "mi", "-s", "-nb", "api/src"])
    if result.returncode == 0:
        match = re.search(r"Average maintainability index: \w+ \((\d+\.\d+)\)", result.stdout)
        if match:
            avg_mi = float(match.group(1))
            if avg_mi < 80.0:
                print(f"❌ Radon MI failed: Average maintainability is {avg_mi} (must be >= 80.0)")
                all_passed = False
            else:
                print(f"✅ Radon MI passed (Average maintainability: {avg_mi}).")
        else:
            print("✅ Radon MI passed (no files to analyze).")
    else:
        print("❌ Radon MI failed to run.")
        print(result.stdout)
        print(result.stderr)
        all_passed = False

    # 5. Mutmut
    print("\n[5/5] Running mutmut for mutation testing...")
    try:
        # We point to the config file within the api directory
        run_result = run_command(["mutmut", "run", "--config-file", "api/pyproject.toml"], timeout=300) # 5 minute timeout
        if run_result.returncode not in [0, 2]: # mutmut exits 2 on timeout
            print("❌ Mutmut failed to run.")
            print(run_result.stdout)
            print(run_result.stderr)
            all_passed = False
        else:
            results_result = run_command(["mutmut", "results"])
            output = results_result.stdout
            match = re.search(r"Mutation score: (\d+\.\d+)%", output)
            if match:
                score = float(match.group(1))
                if score < 90.0:
                    print(f"❌ Mutmut failed: Mutation score is {score}% (must be >= 90%)")
                    all_passed = False
                else:
                    print(f"✅ Mutmut passed (Mutation score: {score}%).")
            else:
                print("⚠️ Mutmut results not found or in unexpected format. Could not check score.")
                print(output)

    except subprocess.TimeoutExpired:
        print("❌ Mutmut timed out after 5 minutes.")
        all_passed = False


    print("------------------------------------")
    return all_passed

def run_docs_quality():
    """
    Runs all documentation quality checks.
    """
    print("--- Running Documentation Quality Checks ---")
    # This function will be implemented in a later step.
    print("Function 'run_docs_quality' is not yet implemented.")
    print("---------------------------------------")
    return True

def main():
    """
    Main entrypoint for the QA Gate script.
    """
    print("🚀 Starting QA Gate...")

    code_quality_passed = run_code_quality()
    docs_quality_passed = run_docs_quality()

    if not code_quality_passed or not docs_quality_passed:
        print("❌ QA Gate failed.")
        sys.exit(1)

    print("✅ QA Gate passed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
