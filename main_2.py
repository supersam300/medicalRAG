import os
from litellm import completion
from openai import OpenAI
import gradio as gr
import json


ollama = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
model = "ollama/llama3.2"

system_prompt = "you are a phrmasist who will prescribe the medicine that proplerly alignes with the ailgment the person is suffering from"
common_remedies = {
    "Fever & Body Pain": {
        "active_ingredients": ["Paracetamol", "Ibuprofen", "Aceclofenac"],
        "common_brands": ["Dolo 650", "Calpol", "Crocin", "Combiflam", "Sumo"],
        "notes": "Dolo 650 is widely used for fever; Combiflam is a popular mix for pain."
    },
    "Cough & Common Cold": {
        "active_ingredients": ["Phenylephrine", "Chlorpheniramine", "Dextromethorphan"],
        "common_brands": ["Sinarest", "Solvin Cold", "Wikoryl", "Ascoril", "Alex"],
        "notes": "Honitus and Koflet are popular herbal alternatives for throat irritation."
    },
    "Allergies & Sneezing": {
        "active_ingredients": ["Cetirizine", "Levocetirizine", "Fexofenadine"],
        "common_brands": ["Okacet", "Cetzine", "Levocet", "Allegra"],
        "notes": "Allegra is often preferred as it is less likely to cause drowsiness."
    },
    "Nasal Congestion": {
        "active_ingredients": ["Xylometazoline", "Oxymetazoline", "Saline"],
        "common_brands": ["Otrivin", "Nasivion", "Nasoclear (Saline)"],
        "notes": "Avoid using decongestant sprays for more than 3-5 days to prevent dependency."
    },
    "Acidity & Heartburn": {
        "active_ingredients": ["Magnesium Hydroxide", "Pantoprazole", "Omeprazole", "Sanchar/Soda"],
        "common_brands": ["Digene", "Gelusil", "Eno", "Pudin Hara", "Pan 40", "Omez"],
        "notes": "Eno provides rapid relief; Pan 40 and Omez are long-acting acid blockers."
    },
    "Diarrhea & Loose Motion": {
        "active_ingredients": ["Loperamide", "ORS (Oral Rehydration Salts)", "Probiotics"],
        "common_brands": ["Eldoper", "Electral (ORS)", "Vizylac", "Sporlac", "Diarex"],
        "notes": "Electral is crucial to prevent dehydration during loose motions."
    },
    "Sore Throat & Mouth Ulcers": {
        "active_ingredients": ["Lozenges", "Povidone-Iodine", "Choline Salicylate"],
        "common_brands": ["Strepsils", "Cofsils", "Betadine Gargle", "Zykee", "Ora-fast"],
        "notes": "Betadine gargles help with throat infections; Zykee is for ulcer pain."
    }
}

def medicine_prescription(ailment):
    print(f"the tool called for the ailment {ailment}")
    ailment_lower = ailment.lower()
    
    target_key = None
    
    if "fever" in ailment_lower or "body pain" in ailment_lower:
        target_key = "Fever & Body Pain"
    elif "cough" in ailment_lower or "cold" in ailment_lower:
        target_key = "Cough & Common Cold"
    elif "allergy" in ailment_lower or "sneez" in ailment_lower:
        target_key = "Allergies & Sneezing"
    elif "congestion" in ailment_lower or "nose" in ailment_lower:
        target_key = "Nasal Congestion"
    elif "acid" in ailment_lower or "heartburn" in ailment_lower:
        target_key = "Acidity & Heartburn"
    elif "diarrhea" in ailment_lower or "loose" in ailment_lower:
        target_key = "Diarrhea & Loose Motion"
    elif "throat" in ailment_lower or "ulcer" in ailment_lower:
        target_key = "Sore Throat & Mouth Ulcers"

    if target_key:
        active_ingredients = common_remedies.get(target_key)
    else:
        active_ingredients = common_remedies.get(ailment)
        if not active_ingredients:
            for key in common_remedies:
                if key.lower() == ailment_lower:
                    active_ingredients = common_remedies[key]
                    break
    
    if not active_ingredients:
        active_ingredients = "No medicine found for this ailment"

    print(f"the active ingredients for the ailment {ailment} are {active_ingredients}")
    return active_ingredients


medicine_tool = {
    "name": "medicine_prescription",
    "description": "Get the active ingredients for a specific ailment",
    "parameters": {
        "type": "object",
        "properties": {
            "ailment": {
                "type": "string",
                "description": "The ailment for which to get the active ingredients"
            }
        },
        "required": ["ailment"]
    }
}
    
tools = [{"type":"function","function":medicine_tool}]   


def handle_tool_call(tool_call):
    function_name = tool_call.function.name
    if function_name == "medicine_prescription":
        arguments = json.loads(tool_call.function.arguments)
        return str(medicine_prescription(arguments["ailment"]))
    return "Error: Unknown tool"

def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    

    response = completion(model="ollama/llama3.2", messages=messages, tools=tools, stream=False)
    
    if response.choices[0].finish_reason == "tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]
        tool_result = handle_tool_call(tool_call)
        
      
        messages.append(response.choices[0].message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        })
        
        
        stream = completion(model="ollama/llama3.2", messages=messages, stream=True)
        partial_message = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                partial_message += chunk.choices[0].delta.content
                yield partial_message
    else:
       yield response.choices[0].message.content
       

gr.ChatInterface(fn=chat).launch()       