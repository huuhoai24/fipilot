"""
Prompt management module
"""

from typing import Dict

SYSTEM_PROMPT = """
You are a professional resume analysis assistant. Your task is to convert the given resume text into the JSON output format specified below and return only the exact schema, do not add fields..
"""


WORK_EXPERIENCE_PROMPT = """{
  "workExperience": [  # Work experience
    {
      "type": "", # "Work" or "Project"
      "name": "", # Company name, e.g.: Viettel | Project name, e.g: OCR project
      "position": "", # Job title, e.g. Algorithm Engineer, Team Lead, Expert Software Engineer. Follow the original text exactly — do not fabricate or infer the position
      "description_refer_index_range": [start_index,end_index]   # List
       # If not present, fill []. Do not confuse this with the project description.
       # Definition of description_refer_index_range: the paragraph index range of the original text referenced by the work experience description, project description. This generally includes work achievements, performance, main duties, project background, tech stack used, job description, etc. Include as much as possible, up until the next work experience entry.
       # Example 1 below
       # [22]: Viettel 2021.11-2022.11
       # [22]: Job description: worked in field sales, achieved xx performance
       # [23]: Rated A in field sales assessment
       # [24]: Company: Alibaba Cloud
       # If "description_refer_index_range":[22,23], it represents all content from paragraph index 22 to 23 (inclusive of both 22 and 23), i.e. 22 + 23
       # Example 2 below
       # [22]: Job description: worked in field sales, achieved xx performance
       # [23]: Rated A in field sales assessment
       # [...]:  ...
       # [40]: Contributed xxx in sales performance to the successful conclusion of the company's field sales campaign.
       # If "description_refer_index_range": [22,40], it represents all content from paragraph index 22 to 40 (inclusive of both 22 and 40), i.e. 22 + 23 + 24 .... + 39 + 40
    }
  ]
}
"""


def get_prompts() -> Dict[str, str]:
    """Get all prompts"""
    return {
        "work_experience": SYSTEM_PROMPT + WORK_EXPERIENCE_PROMPT,
    }
