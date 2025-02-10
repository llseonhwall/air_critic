import json
import xml.etree.ElementTree as ET

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    
def define_convention_rule_category(convention_rule_path):
    '''
    xml 파일을 읽어서 json 형태로 규칙 정의
    '''
    try:
        convention_rules = ET.parse(convention_rule_path)
        root = convention_rules.getroot()
        
        rules_info = []
        convention_categories = set()
        for rule in root.findall('rule'):
            rule_ref = rule.get('ref')
            category = rule_ref.split('/')[-1]  # 카테고리 추출
            properties = rule.find('properties')
            convention_categories.add(category)
            if properties is not None:
                for prop in properties.findall('property'):
                    prop_name = prop.get('name')
                    prop_value = prop.get('value')
                    rules_info.append({
                        "category": category,
                        "property": prop_name,
                        "value": prop_value
                    })
        
        return json.dumps(rules_info, indent=4), convention_categories
    except ET.ParseError as e:
        print("XML 파싱 오류:", e)
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다. 경로를 확인하세요.")
    except Exception as e:
        print("알 수 없는 오류:", e)
       