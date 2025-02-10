import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from prompt_manager import CodeConventionPrompt
from pmd_analyzer import PMDAnalyzer
from utils import *

class ConventionRuleCheckerAgent:
    def __init__(self, llm, pmd_analyzer):
        self.llm = llm
        self.pmd_analyzer = pmd_analyzer
        
    def excute_pmd(self):
        self.pmd_analyzer.save_java_file_from_text()
        pmd_results = self.pmd_analyzer.run_pmd_analysis()
        evaluate_score = self.pmd_analyzer.analyze_convention_violations()
        return evaluate_score
    
    def excute_llm(self, system_prompt, user_prompt, prompt_data):
        messages = [("system", system_prompt),
                    ("user", user_prompt)]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke(prompt_data)
        return response

if __name__ == "__main__":
    CONVENTION_RULE_PATH = "/home/elicer/HSH/convention_rule_checker/custom_ruleset.xml"
    JAVA_SAVE_PATH = "/home/elicer/HSH/convention_rule_checker/user_code.java"
    PMD_PATH = "/home/elicer/pmd-bin-7.9.0/bin/pmd" 
    
    code = """
    public class example {
    public void mymethod() {
        System.out.println("Hello World");
        }
    public void anotherMethod() {
        System.out.println("Another method");
        }
    }
    """
    # input 정의
    convention_rules, convention_categories = define_convention_rule_category(CONVENTION_RULE_PATH)
    prompter = CodeConventionPrompt(convention_rules, convention_categories, code)
    
    # 모델 정의
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    pmd_analyzer = PMDAnalyzer(PMD_PATH, CONVENTION_RULE_PATH, code, JAVA_SAVE_PATH)
    
    # 프롬프트 및 프롬프트 데이터 정의
    prompts = prompter.get_prompt()
    prompt_data = prompter.get_prompt_data()
    
    # 실행
    agent = ConventionRuleCheckerAgent(llm, pmd_analyzer)
    llm_response = agent.excute_llm(prompts["system_prompt"], prompts["user_prompt"], prompt_data)
    scores = agent.excute_pmd()
    
    print(llm_response)
    print(scores)