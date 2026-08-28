import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Document Pipeline POC\n",
    "Thử nghiệm luồng xử lý Resume: Validate -> Extract Text -> Hash/Cache -> LLM Agent -> Mock Save"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import sys\n",
    "import hashlib\n",
    "from pathlib import Path\n",
    "import fitz  # pymupdf\n",
    "\n",
    "# Thêm root path để import được các module từ backend\n",
    "backend_dir = str(Path(os.getcwd()).parent)\n",
    "if backend_dir not in sys.path:\n",
    "    sys.path.append(backend_dir)\n",
    "\n",
    "from fipilot.model.llm_client import LLMClient\n",
    "from pydantic import BaseModel, Field\n",
    "from typing import List, Optional\n",
    "import dotenv\n",
    "\n",
    "dotenv.load_dotenv(Path(backend_dir) / \".env\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Setup Data & Variables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "TEST_PDF_PATH = Path(backend_dir) / \"test\" / \"CV_hoainh.pdf\"\n",
    "MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB\n",
    "\n",
    "print(f\"Test file exists: {TEST_PDF_PATH.exists()}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Validate file type & size"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def validate_file(file_path: Path):\n",
    "    if not file_path.exists():\n",
    "        raise FileNotFoundError(\"File not found\")\n",
    "    \n",
    "    size = file_path.stat().st_size\n",
    "    if size > MAX_FILE_SIZE:\n",
    "        raise ValueError(f\"File too large: {size} bytes\")\n",
    "        \n",
    "    with open(file_path, \"rb\") as f:\n",
    "        header = f.read(4)\n",
    "        if header.startswith(b\"%PDF\"):\n",
    "            file_type = \"PDF\"\n",
    "        elif header.startswith(b\"PK\\x03\\x04\"):\n",
    "            file_type = \"DOCX\"\n",
    "        else:\n",
    "            raise ValueError(\"Unsupported file type. Must be PDF or DOCX.\")\n",
    "            \n",
    "    print(f\"Validation passed: {file_type}, {size} bytes\")\n",
    "    return file_type, size\n",
    "\n",
    "file_type, file_size = validate_file(TEST_PDF_PATH)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Extract Text & SHA-256 Hash"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def extract_text(file_path: Path):\n",
    "    text = \"\"\n",
    "    with fitz.open(file_path) as doc:\n",
    "        for page in doc:\n",
    "            text += page.get_text() + \"\\n\"\n",
    "    return text.strip()\n",
    "\n",
    "def compute_hash(file_path: Path):\n",
    "    sha256 = hashlib.sha256()\n",
    "    with open(file_path, \"rb\") as f:\n",
    "        while chunk := f.read(8192):\n",
    "            sha256.update(chunk)\n",
    "    return sha256.hexdigest()\n",
    "\n",
    "file_hash = compute_hash(TEST_PDF_PATH)\n",
    "print(f\"File Hash: {file_hash}\")\n",
    "\n",
    "resume_text = extract_text(TEST_PDF_PATH)\n",
    "print(f\"Extracted {len(resume_text)} characters\")\n",
    "print(\"-- Preview --\\n\" + resume_text[:200] + \"...\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Cache Check (Mock)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "MOCK_CACHE = {}\n",
    "\n",
    "def check_cache(file_hash: str):\n",
    "    if file_hash in MOCK_CACHE:\n",
    "        print(\"Cache hit!\")\n",
    "        return MOCK_CACHE[file_hash]\n",
    "    print(\"Cache miss! Need to process.\")\n",
    "    return None\n",
    "\n",
    "cached_result = check_cache(file_hash)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. LLM Agent (Extract CandidateProfile)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class SkillEvidence(BaseModel):\n",
    "    skill: str\n",
    "    evidence: str\n",
    "\n",
    "class CandidateProfile(BaseModel):\n",
    "    name: str = Field(..., description=\"Full name of the candidate\")\n",
    "    years_experience: Optional[int] = Field(None, description=\"Total years of experience\")\n",
    "    recent_role: Optional[str] = Field(None, description=\"Most recent job title\")\n",
    "    skills: List[str] = Field(default_factory=list, description=\"List of technical and soft skills\")\n",
    "    skill_evidence: List[SkillEvidence] = Field(default_factory=list, description=\"Evidence for extracted skills\")\n",
    "    is_resume: bool = Field(..., description=\"True if the document is a resume, False otherwise\")\n",
    "\n",
    "def extract_profile_with_llm(text: str) -> CandidateProfile:\n",
    "    llm = LLMClient()\n",
    "    \n",
    "    prompt = f\"\"\"\n",
    "    You are an expert HR extraction system.\n",
    "    Extract the candidate profile from the following document.\n",
    "    If the document does not appear to be a resume/CV, set is_resume to false.\n",
    "    \n",
    "    Document Text:\n",
    "    {text[:5000]}  # Limit text to avoid context overflow for testing\n",
    "    \"\"\"\n",
    "    \n",
    "    print(\"Calling LLM...\")\n",
    "    response = llm.chat_completion_structured(prompt=prompt, response_format=CandidateProfile)\n",
    "    return response\n",
    "\n",
    "if not cached_result:\n",
    "    profile = extract_profile_with_llm(resume_text)\n",
    "    print(f\"Extracted Name: {profile.name}\")\n",
    "    print(f\"Is Resume: {profile.is_resume}\")\n",
    "    print(f\"Skills: {profile.skills}\")\n",
    "    \n",
    "    # Save to cache\n",
    "    MOCK_CACHE[file_hash] = profile"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Mock Repository Save"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import uuid\n",
    "\n",
    "def mock_save_to_repository(candidate_profile, raw_text, file_hash):\n",
    "    candidate_id = str(uuid.uuid4())\n",
    "    print(f\"\\n[Mock Repo] Saved Candidate ID: {candidate_id}\")\n",
    "    print(f\"[Mock Repo] Linked Profile: {candidate_profile.name}\")\n",
    "    print(f\"[Mock Repo] Linked File Hash: {file_hash}\")\n",
    "    \n",
    "    return {\n",
    "        \"candidate_id\": candidate_id,\n",
    "        \"profile\": candidate_profile.model_dump(),\n",
    "        \"extraction_metadata\": {\n",
    "            \"file_hash\": file_hash,\n",
    "            \"status\": \"completed\"\n",
    "        }\n",
    "    }\n",
    "\n",
    "final_result = mock_save_to_repository(profile, resume_text, file_hash)\n",
    "print(\"\\n--- FINAL API RESPONSE MOCK ---\")\n",
    "import pprint\n",
    "pprint.pprint(final_result)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open('/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("Notebook 04_pipeline_poc.ipynb created successfully.")
