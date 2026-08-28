import re

file_path = "gateway/api/interview.py"
with open(file_path, "r") as f:
    content = f.read()

old_logic = """    # 1. Fetch Candidate Profile from DB
    profile = repository.find_by_candidate_id(current_user.uid, request.candidate_id)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate Profile not found or access denied.",
        )

    # 2. Validate: profile must be interview-ready
    if not profile.name or not profile.skills:
        raise HTTPException(
            status_code=422,
            detail="Profile is incomplete and not ready for interview.",
        )

    has_evidence = (
        len(profile.skill_evidence) > 0
        or len(profile.experiences) > 0
        or len(profile.projects) > 0
    )
    if not has_evidence:
        raise HTTPException(
            status_code=422,
            detail="Profile requires at least one experience or skill evidence.",
        )"""

new_logic = """    # 1. Fetch Candidate Profile from DB or Create Mock
    from shared.schemas.candidate import CandidateProfile
    if request.candidate_id:
        profile = repository.find_by_candidate_id(current_user.uid, request.candidate_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Candidate Profile not found or access denied.")
            
        # Validate: profile must be interview-ready
        has_evidence = (len(profile.skill_evidence) > 0 or len(profile.experiences) > 0 or len(profile.projects) > 0)
        if not profile.name or not profile.skills or not has_evidence:
            raise HTTPException(status_code=422, detail="Profile is incomplete and not ready for interview.")
    else:
        # Create a mock profile from custom_description for Custom Role interviews
        mock_skills = [s.strip() for s in (request.custom_description or "General Software Engineering").split(",")]
        profile = CandidateProfile(
            name="Anonymous Candidate",
            skills=mock_skills,
            recent_role=request.config.role,
            years_experience=0,
            specialization=request.config.role,
            projects=[],
            experiences=[],
            education="",
            skill_evidence=[]
        )"""

content = content.replace(old_logic, new_logic)

# Also fix the resume_id saving in database:
old_resume = "resume_id=uuid.UUID(request.candidate_id),"
new_resume = "resume_id=uuid.UUID(request.candidate_id) if request.candidate_id else None,"
content = content.replace(old_resume, new_resume)

with open(file_path, "w") as f:
    f.write(content)
