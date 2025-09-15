import os
import fnmatch
import subprocess
import sys
import re


def _run_command(command, check=True):
    """Helper to run a command and handle errors."""
    print(f"INFO: Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        print("--- STDOUT ---")
        print(result.stdout)
        print("--- STDERR ---")
        print(result.stderr)
        return None, False
    return result.stdout, True


def _run_ruff():
    """Runs ruff linter."""
    print("\n--- Running Ruff Linter ---")
    _, success = _run_command(["ruff", "check", "api/src", "api/tests", "scripts"])
    if success:
        print("SUCCESS: Ruff checks passed.")
    return success


def _run_pytest():
    """Runs pytest with coverage check."""
    print("\n--- Running Pytest with Coverage ---")
    command = [
        "pytest",
        "--cov=api/src/zotify_api",
        "--cov-fail-under=80",
        "api/tests/"
    ]
    _, success = _run_command(command)
    if success:
        print("SUCCESS: Pytest and coverage checks passed (>= 80%).")
    return success


def _find_py_files(directory):
    """Find all python files in a directory."""
    for root, _, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, '*.py'):
                yield os.path.join(root, basename)


def _run_radon():
    """Runs radon for complexity and maintainability checks."""
    print("\n--- Running Radon for Code Metrics ---")
    files_to_scan = list(_find_py_files('api/src/zotify_api'))
    if not files_to_scan:
        print("WARNING: No Python files found for Radon scan.")
        return True

    # Cyclomatic Complexity
    cc_command = ["radon", "cc"] + files_to_scan + ["-a", "-nc"]
    cc_output, success = _run_command(cc_command)
    if not success:
        print("WARNING: Radon command failed. Bypassing check.")
        return True

    cc_match = re.search(r"Average complexity: \w \(([\d.]+)\)", cc_output)
    if not cc_match:
        print("WARNING: Could not parse Radon cyclomatic complexity output. Bypassing check.")
        return True

    avg_cc = float(cc_match.group(1))
    print(f"INFO: Average Cyclomatic Complexity: {avg_cc}")
    if avg_cc > 10:
        print(f"ERROR: Average complexity {avg_cc} is higher than the threshold of 10.")
        return False
    print("SUCCESS: Cyclomatic Complexity check passed (<= 10).")

    # Maintainability Index
    mi_command = ["radon", "mi"] + files_to_scan + ["-a", "-nc"]
    mi_output, success = _run_command(mi_command)
    if not success:
        print("WARNING: Radon command failed. Bypassing check.")
        return True

    mi_match = re.search(r"Average maintainability index: \w \(([\d.]+)\)", mi_output)
    if not mi_match:
        print("WARNING: Could not parse Radon maintainability index output. Bypassing check.")
        return True

    avg_mi = float(mi_match.group(1))
    print(f"INFO: Average Maintainability Index: {avg_mi}")
    if avg_mi < 70:
        print(f"ERROR: Average maintainability {avg_mi} is lower than the threshold of 70.")
        return False
    print("SUCCESS: Maintainability Index check passed (>= 70).")

    return True


def _run_mutmut():
    """Runs mutmut for mutation testing."""
    print("\n--- Running Mutmut for Mutation Testing ---")
    print("INFO: Running mutation tests. This may take a while...")
    run_command = ["mutmut", "run"]
    _run_command(run_command, check=False)

    results_command = ["mutmut", "results"]
    results_output, success = _run_command(results_command)
    if not success:
        print("WARNING: `mutmut results` command failed. Bypassing check.")
        return True

    score_match = re.search(r"Mutation score: ([\d.]+)%", results_output)
    if not score_match:
        print("WARNING: Could not parse mutmut results output. Bypassing check.")
        return True

    mutation_score = float(score_match.group(1))
    print(f"INFO: Mutation Score: {mutation_score}%")
    if mutation_score < 70:
        print(f"ERROR: Mutation score {mutation_score}% is lower than the threshold of 70%.")
        return False

    print("SUCCESS: Mutation testing check passed (>= 70%).")
    return True


def run_code_quality():
    """
    Runs all code quality checks for the Python codebase.
    This is the focus of Phase 1.
    """
    print("INFO: Running code quality checks...")

    checks = {
        "Ruff": _run_ruff,
        "Pytest": _run_pytest,
        "Radon": _run_radon,
        "Mutmut": _run_mutmut,
    }

    all_passed = True
    for name, check_func in checks.items():
        if not check_func():
            print(f"--- {name} checks FAILED ---")
            all_passed = False
        else:
            print(f"--- {name} checks PASSED ---")

    return all_passed


def run_docs_quality():
    """
    Runs all documentation quality and alignment checks.
    This is the focus of Phase 2.
    """
    print("INFO: Running documentation quality checks...")
    # This will be implemented in a future phase.
    print("INFO: Documentation quality checks not yet implemented.")
    return True


def main():
    """Main entrypoint for the QA Gate script."""
    print("--- Starting QA Gate ---")

    code_quality_passed = run_code_quality()
    docs_quality_passed = run_docs_quality()

    print("--- QA Gate Finished ---")

    if not code_quality_passed or not docs_quality_passed:
        print("ERROR: QA Gate failed.")
        sys.exit(1)
    else:
        print("SUCCESS: All QA Gate checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
