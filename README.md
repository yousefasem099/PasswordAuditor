# Password Auditor

## 1. Project Overview
Password Auditor is a Python-based application designed to evaluate password security, detect common passwords, and demonstrate basic password auditing concepts through a graphical user interface.

## 2. Main Features
- Password checking through a graphical interface.
- Detection of passwords included in a custom wordlist.
- Password strength evaluation.
- Synthetic password-hash auditing using PBKDF2-HMAC-SHA256.
- Windows local account name enumeration.
- Performance testing with large wordlists.
- Security tests to verify that passwords are not included in result data or application logs.

## 3. Technologies Used
- Python
- CustomTkinter
- PBKDF2-HMAC-SHA256
- JSON
- Tracemalloc

## 4. Project Structure
```text
PasswordAuditor/
│
├── main.py
├── performance_test.py
│
├── core/
│   ├── auditor.py
│   ├── checker.py
│   ├── security.py
│   ├── test_security.py
│   └── windows_auditor.py
│
├── data/
│   ├── accounts.json
│   └── wordlist.txt
│
├── reports/
│   └── audit_report.json
│
├── screenshots/
│
├── requirements.txt
└── README.md
```

## 5. Installation

Create and activate a virtual environment, then install the required packages:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 6. Running the Application

Run the following command from the project directory:

```bash
python main.py
```

## 7. Running Tests

Security tests:

```bash
python -m core.test_security
```

Performance test:

```bash
python performance_test.py
```

## 8. Important Scope and Limitations

- The password-hash auditing feature currently uses synthetic demonstration accounts.
- The Windows module enumerates local account names; it does not extract SAM or NTLM password hashes.
- The application does not currently read or audit actual Linux `/etc/shadow` entries.
- Password strength evaluation uses a basic educational heuristic and should not be considered a complete industry-standard password-strength estimator.

## 9. Security Considerations

This project is intended for educational and authorized security-auditing purposes.

Never use it to access accounts or password data without explicit authorization. Avoid storing plaintext passwords, protect audit reports, and restrict access to sensitive files.

## 10. Author
Password Auditor – Cybersecurity Practical Project