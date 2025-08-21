import subprocess  # nosec B404

def main():
    print("Running ruff to find errors...")
    result = subprocess.run(  # nosec B603 B607
        ["ruff", "check", "."],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Ruff found errors:")
        print(result.stdout)
    else:
        print("No ruff errors found.")

if __name__ == "__main__":
    main()
