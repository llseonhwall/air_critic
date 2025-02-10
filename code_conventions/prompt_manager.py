class CodeConventionPrompt:
    """
    generate prompt for code convention violation detection
    """
    def __init__(self, convention_rules, convention_categories, code):
        self.convention_rules = convention_rules
        self.convention_categories = convention_categories
        self.code = code
    
    def get_prompt(self):
        system_prompt = """
            You are a highly skilled code reviewer and refactoring expert specializing in Java programming conventions.\n
            Your task is to:
            1. Identify convention violations in the given Java code.
            2. Provide detailed information for each violation:
                - Category of violation.
                - The line number and code snippet that violates the convention.
                - A suggestion to fix the violation.
            3. If There are no violations, retrun an empty 'violations' dict {{}} and 'refactored_code' "".
            4. Refactor the entire code to adhere to the conventions.
            Return your response in a structured JSON format.
            """
        
        user_prompt = """
        Here are the coding conventions to follow: {convention_rules}\n\n 
        Select a violation convention category from the following: {convention_category}\n\n 
        Analyze the following code: '''\n{code}'''\n\n
        
        Step1: Identify all convention violations. For each violation, provice:
        - "category": Category of the violation.
        - "line": Line number of the violation.
        - "snippet": Code snippet that violates the convention.
        - "suggestion": A suggestion to fix the violation.
        Step2: Refactor the entire code to adhere to the conventions.

        Return your response in this JSON format:
        {{
            \"violations"\: [
                {{
                    \"category"\: "string",
                    \"line"\: "int",
                    \"snippet"\: "string",
                    \"suggestion"\: ""string"
                }}
            ],
            \"refactored_code"\: "string of the entire refactored code"
        }}
        """
        return {"system_prompt": system_prompt, "user_prompt": user_prompt}
    
    def get_prompt_data(self):
        return {"convention_rules": self.convention_rules, 
                "convention_category": self.convention_categories, 
                "code": self.code}

        