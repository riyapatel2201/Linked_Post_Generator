from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 8 lines"
    if length == "Medium":
        return "8 to 13 lines"
    if length == "Long":
        return "13 to 18 lines"


def generate_post(length, language, tag, tone=None, creativity=None, hashtags=None, emoji_level="None", 
                 formality=None, writing_style=None, formatting_elements=None, industry_focus=None, 
                 target_audience=None):
    prompt = get_prompt(length, language, tag, tone, hashtags, emoji_level, 
                        formality, writing_style, formatting_elements, industry_focus, 
                        target_audience)

    try:
        prompt = prompt.encode("utf-8", errors="replace").decode("utf-8")
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        return "An error occurred while preparing the prompt."

    # Apply temperature if provided
    if creativity is not None:
        response = llm.invoke(prompt, temperature=creativity)
    else:
        response = llm.invoke(prompt)

    return response.content


def get_prompt(length, language, tag, tone=None, hashtags=None, emoji_level="None", 
              formality=None, writing_style=None, formatting_elements=None, industry_focus=None, 
              target_audience=None):
    length_str = get_length_str(length)

    prompt = f'''
Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
'''
    
    # Counter for instruction numbering
    instruction_num = 4
    
    if tone:
        prompt += f'{instruction_num}) Tone/Intent: {tone}\n'
        instruction_num += 1
    
    if formality:
        prompt += f'{instruction_num}) Formality Level: {formality}\n'
        instruction_num += 1
    
    if writing_style:
        prompt += f'{instruction_num}) Writing Style: {writing_style}\n'
        instruction_num += 1
    
    # Add emoji instructions based on selected level
    if emoji_level != "None":
        prompt += f'{instruction_num}) Emoji Usage: {emoji_level}\n'
        
        if emoji_level == "Low":
            prompt += "Include 2-3 relevant emojis strategically placed within the post.\n"
        elif emoji_level == "Medium":
            prompt += "Include 4-6 relevant emojis distributed evenly throughout the post.\n"
        elif emoji_level == "High":
            prompt += "Include 7+ relevant emojis liberally throughout the post to emphasize key points.\n"
        
        instruction_num += 1
    else:
        prompt += "Do not include any emojis in the post.\n"
    
    # Add formatting elements if selected
    if formatting_elements and len(formatting_elements) > 0:
        prompt += f'{instruction_num}) Formatting Elements: {", ".join(formatting_elements)}\n'
        
        if "Bold key points" in formatting_elements:
            prompt += "Use ** around important phrases or key points to make them stand out.\n"
        
        if "Use bullet points" in formatting_elements:
            prompt += "Include a bulleted list for key points or takeaways using LinkedIn's bullet format.\n"
        
        if "Include quotations" in formatting_elements:
            prompt += "Include a relevant quote or statement in quotation marks for emphasis.\n"
        
        if "Add statistics" in formatting_elements:
            prompt += "Incorporate 1-2 relevant statistics or data points to strengthen the message.\n"
        
        instruction_num += 1
    
    # Add industry focus if selected
    if industry_focus:
        prompt += f'{instruction_num}) Industry Focus: {industry_focus}\n'
        prompt += f"Tailor the content for professionals in the {industry_focus} industry with relevant terminology and examples.\n"
        instruction_num += 1
    
    # Add target audience if selected
    if target_audience:
        prompt += f'{instruction_num}) Target Audience: {target_audience}\n'
        prompt += f"Craft the message to specifically resonate with {target_audience} on LinkedIn.\n"
        instruction_num += 1

    prompt += '''
If Language is Hinglish then it means it is a mix of Hindi and English.
The script for the generated post should always be English.
'''

    # Handle hashtags - only add if explicitly selected
    if hashtags is not None:
        if hashtags == "AUTO":
            prompt += "Include relevant, trending hashtags at the end of the post.\n"
        else:
            prompt += f"Use the following hashtags at the end: {hashtags}\n"
    else:
        prompt += "Do not include any hashtags in the post.\n"

    # Add few-shot examples
    examples = few_shot.get_filtered_posts(length, language, tag)
    if len(examples) > 0:
        prompt += "Use the writing style as per the following examples:\n"

    for i, post in enumerate(examples[:2]):  # Max 2 examples
        post_text = post['text']
        prompt += f'\nExample {i+1}:\n\n{post_text}\n'

    return prompt

if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health", tone="Inspirational", creativity=0.8, hashtags=None, emoji_level="Medium"))