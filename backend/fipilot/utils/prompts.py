"""
Prompt management module
"""
from typing import Dict
 
SYSTEM_PROMPT = """
You are a professional resume analysis assistant. Your task is to convert the given resume text into the JSON output format specified below.
"""


WORK_EXPERIENCE_PROMPT = """{
  "workExperience": [  # Work experience / internship experience
    {
      "companyName": "", # Company name, e.g.: Viettel
      "employmentPeriod": {  # Start and end dates of this experience
        "startDate": "",# Start/joining date. If not present, leave "" (do not fabricate). Format: %Y.%m or %Y, e.g. 2024, 2024.1
        "endDate": "" # If ongoing, fill (present). If not present, leave "" (do not fabricate). Format: %Y.%m or %Y, e.g. 2024, 2024.1
      },
      "position": "", # Job title, e.g. Algorithm Engineer, Team Lead, Expert Software Engineer. Follow the original text exactly — do not fabricate or infer the position
      "internship": 0, # Whether this experience is an internship. 1 if internship, 0 if not
      "jobDescription_refer_index_range": [start_index,end_index]   # List
       # If not present, fill []. Do not confuse this with the project description.
       # Definition of jobDescription_refer_index_range: the paragraph index range of the original text referenced by the work experience description. This generally includes work achievements, performance, main duties, project background, tech stack used, job description, etc. Include as much as possible, up until the next work experience entry.
       # jobDescription_refer_index_range must NOT include the companyName, employmentPeriod, or position fields. Do not include the companyName, employmentPeriod, or position fields in the description range.
       # jobDescription_refer_index_range must NOT include the companyName, employmentPeriod, or position fields. Do not include the companyName, employmentPeriod, or position fields in the description range.
       # Example 1 below
       # [22]: Viettel 2021.11-2022.11
       # [22]: Job description: worked in field sales, achieved xx performance
       # [23]: Rated A in field sales assessment
       # [24]: Company: Alibaba Cloud
       # If "jobDescription_refer_index_range":[22,23], it represents all content from paragraph index 22 to 23 (inclusive of both 22 and 23), i.e. 22 + 23
       # Example 2 below
       # [22]: Job description: worked in field sales, achieved xx performance
       # [23]: Rated A in field sales assessment
       # [...]:  ...
       # [40]: Contributed xxx in sales performance to the successful conclusion of the company's field sales campaign.
       # If "jobDescription_refer_index_range": [22,40], it represents all content from paragraph index 22 to 40 (inclusive of both 22 and 40), i.e. 22 + 23 + 24 .... + 39 + 40
    }, ...
  ]
  }
"""

EDUCATION_PROMPT = """
{
  "education": [  # Education history
    {
      "degreeLevel": "", # Degree: Bachelor's/Master's/Doctorate/Associate/High School/Middle School. If not present, leave ""
      "period": {  # Start and end dates of this education experience, format "yyyy.mm" or "yyyy", e.g. "2021.2"
        "startDate": "", # Start date. Format: %Y.%m or %Y, e.g. 2024, 2024.1
        "endDate":""  # If ongoing, fill (present). If not present, leave ""
      },
      "school": "", # School name, e.g. FPT University, University of Information Technology
      "department": "", # Department, e.g. Department of Information Engineering
      "major": "", # Major, e.g. Software Engineer, Computer Science
      "educationDescription": "" # Education description, including coursework grades, research direction, GPA, honors/awards, etc. for this education experience, excluding the degree itself. Use the exact wording from the resume; if not present, leave "" (empty)
    }, ...
  ]
}
"""

THINK_TAG = " /no_think"
 
 
def get_prompts() -> Dict[str, str]:
    """Get all prompts"""
    return {
        "work_experience": SYSTEM_PROMPT + WORK_EXPERIENCE_PROMPT + THINK_TAG,
        "education": SYSTEM_PROMPT + EDUCATION_PROMPT + THINK_TAG,
    }
 
