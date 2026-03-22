import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    try:
        with open(raw_file_path, encoding='utf-8') as file:
            posts = json.load(file)
            enriched_posts = []
            for post in posts:
                metadata = extract_metadata(post['text'])
                post_with_metadata = post | metadata
                enriched_posts.append(post_with_metadata)

        unified_tags = get_unified_tags(enriched_posts)
        for post in enriched_posts:
            current_tags = post['tags']
            new_tags = {unified_tags.get(tag, tag) for tag in current_tags}  # Safely map tags
            post['tags'] = list(new_tags)

        # Handle file path being None or a valid path
        if processed_file_path:
            with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
                json.dump(enriched_posts, outfile, indent=4)

    except Exception as e:
        print(f"Error processing posts: {e}")


def extract_metadata(post):
    # Remove problematic characters (such as emojis) from the post text
    sanitized_post = post.encode('utf-8', errors='ignore').decode('utf-8')

    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": sanitized_post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    # Loop through each post and extract the tags
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])  # Add the tags to the set

    unique_tags_list = list(unique_tags)  # Convert to list for passing to prompt

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation"}}
    
    Here is the list of tags: 
    {tags}
    '''
    
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": unique_tags_list})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
