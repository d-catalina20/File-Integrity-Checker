# Log Integrity Checker

A lightweight CLI security tool written in Python to monitor and verify the integrity of log files. By leveraging cryptographic hashing (SHA-256), this tool detects unauthorized changes or potential tampering in system and application logs, acting as a File Integrity Monitoring (FIM) solution.
https://roadmap.sh/projects/file-integrity-checker

## Features
- **File & Directory Support:** Accepts a path to a single log file or recursively scans an entire directory.
- **Cryptographic Hashing:** Computes SHA-256 hashes to guarantee data integrity.
- **Baseline Storage:** Stores computed hashes securely in a local JSON database on first initialization.
- **Tamper Detection:** Compares active files against saved baselines to report modifications or unexpected changes.
- **Manual Updates:** Allows safe manual re-initialization of individual files when logs are legitimately updated.

## How It Works
1. **`init`**: Scans the path, computes SHA-256 hashes for all valid files, and saves them to `log_hashes.json`.
2. **`check`**: Recalculates the hashes of the target files and compares them with the stored baseline. Reports if a file is `Unmodified`, `MODIFIED` (tampered), or `Untracked`.
3. **`update`**: Overwrites the baseline hash for a specific file after authorized updates.

---

## Installation & Setup

1. **Clone the repository:**
   	```bash
   	git clone [https://github.com/d-catalina20/File-Integrity-Checker.git](https://github.com/d-catalina20/File-Integrity-Checker.git)
   	cd File-Integrity-Checker
   	# (Optional) Set up a virtual environment:
   	python3 -m venv .venv
	source .venv/bin/activate  # On Windows use: venv\Scripts\activate
	```

## Usage Examples
1. **Initialize Baseline Hashes**
To start tracking a directory or a specific log file:
	```bash
	python3 src/main.py init ../test_logs
	# Output: Hashes stored successfully.
	```
2. **Verify File Integrity**
Run this periodically to detect tampering:
	```bash
	python3 src/main.py check ../test_logs
	# Output (if safe):
	# /path/to/test_logs/auth.log -> Status: Unmodified
	# /path/to/test_logs/syslog.log -> Status: Unmodified
	# Output (if altered):
	# /path/to/test_logs/syslog.log -> Status: MODIFIED (Hash mismatch! Possible tampering!)
	```

3. **Update an Authorized Log File**
	```bash
	python3 src/main.py update ../test_logs/syslog.log
	# Output: Hash updated successfully for /path/to/test_logs/syslog.log
	```
