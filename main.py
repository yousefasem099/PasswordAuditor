
import customtkinter as ctk
from tkinter import messagebox

from core.checker import PasswordChecker
from core.auditor import SystemAccountAuditor
from core.windows_auditor import WindowsAccountAuditor


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PasswordAuditorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Password Auditing & Policy Enforcement Tool")
        self.geometry("950x750")
        self.minsize(850, 650)

        self.create_interface()

    def create_interface(self):

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.tabview.add("Password Checker")
        self.tabview.add("System Auditor")

        self.create_password_checker_tab()
        self.create_system_auditor_tab()

    # ==========================================
    # PASSWORD CHECKER TAB
    # ==========================================

    def create_password_checker_tab(self):

        tab = self.tabview.tab("Password Checker")

        ctk.CTkLabel(
            tab,
            text="PASSWORD SECURITY CHECKER",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 20))

        self.password_entry = ctk.CTkEntry(
            tab,
            placeholder_text="Enter your password",
            show="*",
            width=400,
            height=45
        )
        self.password_entry.pack(pady=15)

        self.show_password_var = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            tab,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password
        ).pack(pady=5)

        ctk.CTkButton(
            tab,
            text="CHECK PASSWORD",
            width=220,
            height=45,
            command=self.check_password
        ).pack(pady=20)

        self.password_result = ctk.CTkLabel(
            tab,
            text="Enter a password to analyze its security.",
            font=("Arial", 15),
            wraplength=650
        )
        self.password_result.pack(pady=15)

        self.strength_label = ctk.CTkLabel(
            tab,
            text="Password Strength: Not evaluated",
            font=("Arial", 16, "bold")
        )
        self.strength_label.pack(pady=10)

        self.strength_progress = ctk.CTkProgressBar(
            tab,
            width=400
        )
        self.strength_progress.pack(pady=10)
        self.strength_progress.set(0)

        self.recommendation_label = ctk.CTkLabel(
            tab,
            text="",
            font=("Arial", 14),
            wraplength=650,
            justify="left"
        )
        self.recommendation_label.pack(pady=20)

    def toggle_password(self):

        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def check_password(self):

        password = self.password_entry.get()

        if not password:
            messagebox.showwarning(
                "Missing Password",
                "Please enter a password first."
            )
            return

        try:
            result = PasswordChecker.check_password(password)

            self.password_result.configure(
                text=str(result)
            )

        except Exception as error:
            self.password_result.configure(
                text=f"Password analysis error: {error}"
            )

        finally:
            password = None

    # ==========================================
    # SYSTEM AUDITOR TAB
    # ==========================================

    def create_system_auditor_tab(self):

        tab = self.tabview.tab("System Auditor")

        ctk.CTkLabel(
            tab,
            text="SYSTEM PASSWORD AUDITOR",
            font=("Arial", 24, "bold")
        ).pack(pady=(20, 15))

        ctk.CTkButton(
            tab,
            text="RUN SYNTHETIC PASSWORD AUDIT",
            width=300,
            height=45,
            command=self.run_audit
        ).pack(pady=10)

        ctk.CTkButton(
            tab,
            text="SCAN WINDOWS LOCAL ACCOUNTS",
            width=300,
            height=45,
            command=self.run_windows_audit
        ).pack(pady=10)

        self.audit_output = ctk.CTkTextbox(
            tab,
            width=820,
            height=430,
            font=("Consolas", 13),
            wrap="word"
        )
        self.audit_output.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ==========================================
    # SYNTHETIC PASSWORD AUDIT
    # ==========================================

    def run_audit(self):

        try:
            auditor = SystemAccountAuditor()
            results = auditor.audit_accounts()

            self.audit_output.delete("1.0", "end")

            self.audit_output.insert(
                "end",
                "SYNTHETIC PASSWORD AUDIT RESULTS\n"
                "====================================\n\n"
            )

            self.audit_output.insert(
                "end",
                str(results)
            )

            self.audit_output.insert(
                "end",
                "\n\nSynthetic audit completed.\n"
            )

        except Exception as error:

            messagebox.showerror(
                "Audit Error",
                str(error)
            )

    # ==========================================
    # WINDOWS LOCAL ACCOUNT AUDIT
    # ==========================================

    def run_windows_audit(self):

        try:

            accounts = WindowsAccountAuditor.get_local_accounts()
            policy = WindowsAccountAuditor.get_password_policy()

            self.audit_output.delete("1.0", "end")

            self.audit_output.insert(
                "end",
                "WINDOWS LOCAL ACCOUNT SECURITY AUDIT\n"
                "========================================\n\n"
            )

            self.audit_output.insert(
                "end",
                f"Total local accounts: {len(accounts)}\n\n"
            )

            self.audit_output.insert(
                "end",
                "LOCAL ACCOUNTS\n"
                "--------------\n\n"
            )

            for index, account in enumerate(accounts, start=1):

                self.audit_output.insert(
                    "end",
                    f"Account #{index}\n"
                )

                self.audit_output.insert(
                    "end",
                    f"Username: {account.get('username', 'Unknown')}\n"
                )

                self.audit_output.insert(
                    "end",
                    f"Enabled: {account.get('enabled', 'Unknown')}\n"
                )

                self.audit_output.insert(
                    "end",
                    f"Password Required: "
                    f"{account.get('password_required', 'Unknown')}\n"
                )

                self.audit_output.insert(
                    "end",
                    f"Password Last Set: "
                    f"{account.get('password_last_set', 'Unknown')}\n"
                )

                self.audit_output.insert(
                    "end",
                    "----------------------------------------\n"
                )

            self.audit_output.insert(
                "end",
                "\nPASSWORD POLICY\n"
                "---------------\n\n"
            )

            for key, value in policy.items():

                self.audit_output.insert(
                    "end",
                    f"{key}: {value}\n"
                )

            # Security recommendations

            self.audit_output.insert(
                "end",
                "\nSECURITY RECOMMENDATIONS\n"
                "------------------------\n\n"
            )

            recommendations = []

            min_length = policy.get(
                "Minimum password length"
            )

            if min_length is not None:

                try:
                    if int(min_length) < 12:
                        recommendations.append(
                            "Increase minimum password length to at least 12 characters."
                        )
                except ValueError:
                    pass

            history = policy.get(
                "Length of password history maintained"
            )

            if history is not None:

                if str(history).lower() in ("none", "0"):
                    recommendations.append(
                        "Enable password history to prevent password reuse."
                    )

            lockout = policy.get(
                "Lockout threshold"
            )

            if lockout is not None:

                if str(lockout).lower() == "never":
                    recommendations.append(
                        "Configure an account lockout threshold."
                    )

            if recommendations:

                for number, recommendation in enumerate(
                    recommendations,
                    start=1
                ):
                    self.audit_output.insert(
                        "end",
                        f"{number}. {recommendation}\n"
                    )

            else:

                self.audit_output.insert(
                    "end",
                    "No recommendations generated from the available policy values.\n"
                )

            self.audit_output.insert(
                "end",
                "\nAUDIT SUMMARY\n"
                "-------------\n"
                "Windows account enumeration: Completed\n"
                "Password policy inspection: Completed\n"
                "SAM hash extraction: Not performed\n"
                "NTLM hash analysis: Not performed\n"
                "Plaintext passwords accessed: No\n"
            )

        except Exception as error:

            messagebox.showerror(
                "Windows Audit Error",
                str(error)
            )


if __name__ == "__main__":

    app = PasswordAuditorApp()
    app.mainloop()
