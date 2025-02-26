# Educational Scholarship Advisor Expert System with GUI
# Compatible with Spyder IDE
# Date: February 25, 2025

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ScholarshipExpertSystem:
    def __init__(self):
        """
        Initialize the expert system with an empty knowledge base
        """
        self.facts = {}  # Dictionary to store facts
        self.rules = []  # List to store rules
        self.conclusions = {}  # Dictionary to store conclusions
        self.setup_rules()
        
    def setup_rules(self):
        """
        Setup the rules for the scholarship advisor system
        """
        # Rule 1: Academic Merit Scholarship
        self.add_rule(
            "R1",
            [("gpa", ">=", 3.5), ("extracurricular_activities", "==", True)],
            "merit_scholarship",
            "Eligible",
            "If GPA >= 3.5 and has extracurricular activities, then eligible for Merit Scholarship"
        )
        
        # Rule 2: Financial Need Scholarship
        self.add_rule(
            "R2",
            [("family_income", "<=", 20000), ("gpa", ">=", 2.5)],
            "need_based_scholarship",
            "Eligible",
            "If family income <= 20,000 RWF and GPA >= 2.5, then eligible for Need-Based Scholarship"
        )
        
        # Rule 3: Sports Scholarship
        self.add_rule(
            "R3",
            [("sports_achievement", "==", True), ("gpa", ">=", 2.0)],
            "sports_scholarship",
            "Eligible",
            "If has sports achievements and GPA >= 2.0, then eligible for Sports Scholarship"
        )
        
        # Rule 4: Leadership Scholarship
        self.add_rule(
            "R4",
            [("leadership_role", "==", True), ("gpa", ">=", 3.0)],
            "leadership_scholarship",
            "Eligible",
            "If has leadership roles and GPA >= 3.0, then eligible for Leadership Scholarship"
        )
        
        # Rule 5: Community Service Scholarship
        self.add_rule(
            "R5",
            [("community_service", ">=", 50), ("gpa", ">=", 2.7)],
            "community_service_scholarship",
            "Eligible",
            "If has >= 50 hours of community service and GPA >= 2.7, then eligible for Community Service Scholarship"
        )
        
        # Rule 6: Low eligibility if not meeting any criteria
        self.add_rule(
            "R6",
            [("gpa", "<", 2.0)],
            "scholarship_eligibility",
            "Low",
            "If GPA < 2.0, then scholarship eligibility is Low"
        )
        
        # Rule 7: High eligibility if eligible for multiple scholarships
        self.add_rule(
            "R7",
            [("merit_scholarship", "==", "Eligible"), ("leadership_scholarship", "==", "Eligible")],
            "scholarship_eligibility",
            "High",
            "If eligible for both Merit and Leadership scholarships, then overall eligibility is High"
        )
        
        # Rule 8: Medium eligibility if eligible for at least one scholarship
        self.add_rule(
            "R8",
            [("need_based_scholarship", "==", "Eligible")],
            "scholarship_eligibility",
            "Medium",
            "If eligible for Need-Based scholarship, then overall eligibility is at least Medium"
        )
        
    def add_rule(self, rule_id, conditions, conclusion, conclusion_value, description):
        """
        Add a rule to the knowledge base
        """
        rule = {
            "id": rule_id,
            "conditions": conditions,
            "conclusion": conclusion,
            "conclusion_value": conclusion_value,
            "description": description
        }
        self.rules.append(rule)
        
    def evaluate_condition(self, condition):
        """
        Evaluate a single condition
        """
        fact_name, operator, value = condition
        
        if fact_name not in self.facts:
            return False
        
        fact_value = self.facts[fact_name]
        
        if operator == "==":
            return fact_value == value
        elif operator == "!=":
            return fact_value != value
        elif operator == ">":
            return fact_value > value
        elif operator == "<":
            return fact_value < value
        elif operator == ">=":
            return fact_value >= value
        elif operator == "<=":
            return fact_value <= value
        elif operator == "in":
            return fact_value in value
        else:
            return False
        
    def evaluate_rule(self, rule):
        """
        Evaluate a rule against the current facts
        """
        all_conditions_met = True
        
        for condition in rule["conditions"]:
            if not self.evaluate_condition(condition):
                all_conditions_met = False
                break
                
        return all_conditions_met
    
    def infer(self):
        """
        Run the inference engine to apply rules and derive new facts
        """
        rules_fired = []
        
        # Continue until no new facts are added
        changes_made = True
        while changes_made:
            changes_made = False
            
            for rule in self.rules:
                if self.evaluate_rule(rule):
                    # If rule conditions are met and conclusion isn't already set
                    conclusion = rule["conclusion"]
                    conclusion_value = rule["conclusion_value"]
                    
                    # Only add the conclusion if it's new or different
                    if conclusion not in self.conclusions or self.conclusions[conclusion] != conclusion_value:
                        self.conclusions[conclusion] = conclusion_value
                        rules_fired.append(f"Rule {rule['id']}: {rule['description']}")
                        changes_made = True
        
        return self.conclusions, rules_fired

class ScholarshipAdvisorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Scholarship Advisor")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.expert_system = ScholarshipExpertSystem()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frames
        self.header_frame = tk.Frame(self.root, bg="#3498db", height=70)
        self.header_frame.pack(fill="x")
        
        self.content_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.content_frame.pack(fill="both", expand=True)
        
        # Create header
        header_label = tk.Label(
            self.header_frame, 
            text="Educational Scholarship Advisor", 
            font=("Arial", 20, "bold"),
            bg="#3498db",
            fg="white"
        )
        header_label.pack(pady=15)
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.content_frame)
        
        self.input_tab = ttk.Frame(self.tab_control)
        self.results_tab = ttk.Frame(self.tab_control)
        self.about_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.input_tab, text="Student Information")
        self.tab_control.add(self.results_tab, text="Scholarship Results")
        self.tab_control.add(self.about_tab, text="About")
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Set up input tab
        self.setup_input_tab()
        
        # Set up results tab
        self.setup_results_tab()
        
        # Set up about tab
        self.setup_about_tab()
        
    def setup_input_tab(self):
        # Create a frame for user inputs
        input_frame = tk.Frame(self.input_tab, bg="#ecf0f1", padx=20, pady=20)
        input_frame.pack(fill="both", expand=True)
        
        # Add title
        title_label = tk.Label(
            input_frame,
            text="Enter Student Information",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1"
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # GPA input
        gpa_label = tk.Label(input_frame, text="GPA (0.0-4.0):", bg="#ecf0f1", font=("Arial", 12))
        gpa_label.grid(row=1, column=0, sticky="w", pady=10)
        
        self.gpa_var = tk.StringVar()
        self.gpa_entry = tk.Entry(input_frame, textvariable=self.gpa_var, width=30)
        self.gpa_entry.grid(row=1, column=1, sticky="w", pady=10)
        
        # Family income
        income_label = tk.Label(input_frame, text="Annual Family Income (RWF):", bg="#ecf0f1", font=("Arial", 12))
        income_label.grid(row=2, column=0, sticky="w", pady=10)
        
        self.income_var = tk.StringVar()
        self.income_entry = tk.Entry(input_frame, textvariable=self.income_var, width=30)
        self.income_entry.grid(row=2, column=1, sticky="w", pady=10)
        
        # Extracurricular activities
        self.extracurricular_var = tk.BooleanVar()
        extracurricular_check = tk.Checkbutton(
            input_frame,
            text="Extracurricular Activities",
            variable=self.extracurricular_var,
            bg="#ecf0f1",
            font=("Arial", 12)
        )
        extracurricular_check.grid(row=3, column=0, columnspan=2, sticky="w", pady=10)
        
        # Sports achievements
        self.sports_var = tk.BooleanVar()
        sports_check = tk.Checkbutton(
            input_frame,
            text="Sports Achievements",
            variable=self.sports_var,
            bg="#ecf0f1",
            font=("Arial", 12)
        )
        sports_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
        
        # Leadership roles
        self.leadership_var = tk.BooleanVar()
        leadership_check = tk.Checkbutton(
            input_frame,
            text="Leadership Roles",
            variable=self.leadership_var,
            bg="#ecf0f1",
            font=("Arial", 12)
        )
        leadership_check.grid(row=5, column=0, columnspan=2, sticky="w", pady=10)
        
        # Community service hours
        community_label = tk.Label(input_frame, text="Community Service Hours:", bg="#ecf0f1", font=("Arial", 12))
        community_label.grid(row=6, column=0, sticky="w", pady=10)
        
        self.community_var = tk.StringVar()
        self.community_entry = tk.Entry(input_frame, textvariable=self.community_var, width=30)
        self.community_entry.grid(row=6, column=1, sticky="w", pady=10)
        
        # Submit button
        submit_button = tk.Button(
            input_frame,
            text="Check Scholarship Eligibility",
            command=self.process_input,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        )
        submit_button.grid(row=7, column=0, columnspan=2, pady=20)
        
        # Clear button
        clear_button = tk.Button(
            input_frame,
            text="Clear Form",
            command=self.clear_form,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        clear_button.grid(row=8, column=0, columnspan=2)
        
    def setup_results_tab(self):
        results_frame = tk.Frame(self.results_tab, bg="#ecf0f1", padx=20, pady=20)
        results_frame.pack(fill="both", expand=True)
        
        # Results title
        results_title = tk.Label(
            results_frame,
            text="Scholarship Eligibility Results",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1"
        )
        results_title.pack(anchor="w", pady=(0, 10))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Arial", 11)
        )
        self.results_text.pack(fill="both", expand=True)
        self.results_text.config(state=tk.DISABLED)
        
    def setup_about_tab(self):
        about_frame = tk.Frame(self.about_tab, bg="#ecf0f1", padx=20, pady=20)
        about_frame.pack(fill="both", expand=True)
        
        about_title = tk.Label(
            about_frame,
            text="About This Expert System",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1"
        )
        about_title.pack(anchor="w", pady=(0, 10))
        
        about_text = scrolledtext.ScrolledText(
            about_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Arial", 11)
        )
        about_text.pack(fill="both", expand=True)
        
        about_content = """Educational Scholarship Advisor Expert System

This rule-based expert system evaluates a student's eligibility for various scholarships based on academic performance, financial need, extracurricular activities, and other factors relevant in the Rwandan/African context.

The system uses forward chaining with IF-THEN rules to determine which scholarships a student might be eligible for based on their profile.

Scholarships evaluated:
- Academic Merit Scholarship
- Financial Need-Based Scholarship
- Sports Achievement Scholarship
- Leadership Scholarship
- Community Service Scholarship

Developed by: Group 8
Course: Artificial Intelligence (AI) - Traditional AI & Expert Systems
INES - RUHENGERI
Faculty of Sciences and Information Technology
Department of Computer Science
SWE / YEAR 3 / DAY - 2024-2025
"""
        
        about_text.insert(tk.END, about_content)
        about_text.config(state=tk.DISABLED)
        
    def process_input(self):
        try:
            # Get values from form
            gpa = float(self.gpa_var.get())
            if gpa < 0 or gpa > 4.0:
                messagebox.showerror("Input Error", "GPA must be between 0.0 and 4.0")
                return
            
            try:
                income = float(self.income_var.get())
            except:
                income = 0
            
            try:
                community_hours = float(self.community_var.get())
            except:
                community_hours = 0
            
            # Add facts to expert system
            self.expert_system.facts = {
                "gpa": gpa,
                "family_income": income,
                "extracurricular_activities": self.extracurricular_var.get(),
                "sports_achievement": self.sports_var.get(),
                "leadership_role": self.leadership_var.get(),
                "community_service": community_hours
            }
            
            # Run inference engine
            conclusions, rules_fired = self.expert_system.infer()
            
            # Switch to results tab
            self.tab_control.select(1)
            
            # Display results
            self.display_results(conclusions, rules_fired)
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please ensure all numeric fields contain valid numbers.")
    
    def display_results(self, conclusions, rules_fired):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Add student information summary
        self.results_text.insert(tk.END, "Student Information Summary:\n", "heading")
        self.results_text.insert(tk.END, f"GPA: {self.expert_system.facts['gpa']}\n")
        self.results_text.insert(tk.END, f"Family Income: {self.expert_system.facts['family_income']} RWF\n")
        self.results_text.insert(tk.END, f"Extracurricular Activities: {'Yes' if self.expert_system.facts['extracurricular_activities'] else 'No'}\n")
        self.results_text.insert(tk.END, f"Sports Achievements: {'Yes' if self.expert_system.facts['sports_achievement'] else 'No'}\n")
        self.results_text.insert(tk.END, f"Leadership Roles: {'Yes' if self.expert_system.facts['leadership_role'] else 'No'}\n")
        self.results_text.insert(tk.END, f"Community Service Hours: {self.expert_system.facts['community_service']}\n\n")
        
        # Add rules that fired
        self.results_text.insert(tk.END, "Rules Applied:\n", "heading")
        for rule in rules_fired:
            self.results_text.insert(tk.END, f"- {rule}\n")
        
        # Add scholarship eligibility results
        self.results_text.insert(tk.END, "\nScholarship Eligibility Results:\n", "heading")
        
        scholarships = [
            ("merit_scholarship", "Academic Merit Scholarship"),
            ("need_based_scholarship", "Financial Need-Based Scholarship"),
            ("sports_scholarship", "Sports Achievement Scholarship"),
            ("leadership_scholarship", "Leadership Scholarship"),
            ("community_service_scholarship", "Community Service Scholarship")
        ]
        
        eligible_count = 0
        for key, name in scholarships:
            status = conclusions.get(key, "Not Eligible")
            if status == "Eligible":
                eligible_count += 1
                self.results_text.insert(tk.END, f"✅ {name}: {status}\n")
            else:
                self.results_text.insert(tk.END, f"❌ {name}: Not Eligible\n")
        
        # Overall eligibility
        self.results_text.insert(tk.END, "\nOverall Eligibility:\n", "heading")
        overall = conclusions.get("scholarship_eligibility", "Not Determined")
        if overall == "High":
            message = "The student has high eligibility for scholarships and should apply to multiple programs."
        elif overall == "Medium":
            message = "The student has moderate eligibility and should focus on applying to the specific scholarships listed as eligible above."
        elif overall == "Low":
            message = "The student has low eligibility for scholarships. Consider improving GPA and participating in more activities."
        else:
            if eligible_count > 0:
                message = "The student is eligible for at least one scholarship and should apply."
                overall = "Medium"
            else:
                message = "The student is not currently eligible for the evaluated scholarships."
                overall = "Low"
        
        self.results_text.insert(tk.END, f"Rating: {overall}\n")
        self.results_text.insert(tk.END, message)
        
        # Make text read-only again
        self.results_text.config(state=tk.DISABLED)
    
    def clear_form(self):
        self.gpa_var.set("")
        self.income_var.set("")
        self.community_var.set("")
        self.extracurricular_var.set(False)
        self.sports_var.set(False)
        self.leadership_var.set(False)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScholarshipAdvisorGUI(root)
    root.mainloop()
