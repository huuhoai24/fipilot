import type { CandidateProfile } from '@/types'

export interface RoleDefinition {
  id: string
  title: string
  description: string
  keywords: string[]
}

export const INTERVIEW_ROLES: RoleDefinition[] = [
  {
    id: 'ai-engineer',
    title: 'AI Engineer',
    description: 'Generative AI, LLMs, RAG, PyTorch, LangChain, Agentic AI, and model deployment',
    keywords: [
      'pytorch', 'tensorflow', 'keras', 'llm', 'large language models', 'rag', 'langchain',
      'langgraph', 'agentic ai', 'huggingface', 'transformers', 'deep learning',
      'generative ai', 'vector database', 'pinecone', 'chromadb', 'qdrant', 'weaviate',
      'openai', 'gemini', 'embeddings', 'prompt engineering', 'onnx', 'tensorrt',
      'bert', 'gpt', 'yolo', 'opencv', 'computer vision', 'nlp', 'fine-tuning', 'lora'
    ],
  },
  {
    id: 'backend-developer',
    title: 'Backend Developer',
    description: 'APIs, relational & NoSQL databases, microservices, system architecture, and concurrency',
    keywords: [
      'fastapi', 'django', 'flask', 'java', 'spring', 'spring boot', 'golang', 'go',
      'c#', '.net', 'asp.net', 'nodejs', 'node.js', 'express', 'nest.js', 'nestjs',
      'microservices', 'grpc', 'postgresql', 'mysql', 'mongodb', 'redis', 'kafka',
      'rabbitmq', 'database design', 'sql', 'rest api', 'restful apis'
    ],
  },
  {
    id: 'business-analyst',
    title: 'Business Analyst',
    description: 'Requirements analysis, user stories, BRD/SRS, BPMN, stakeholder communication, and Agile',
    keywords: [
      'business analysis', 'requirements analysis', 'user stories', 'brd', 'srs',
      'bpmn', 'flowchart', 'stakeholder management', 'agile', 'scrum', 'jira',
      'confluence', 'gap analysis', 'product backlog', 'acceptance criteria',
      'use case', 'wireframing', 'process mapping', 'business process'
    ],
  },
  {
    id: 'data-engineer',
    title: 'Data Engineer',
    description: 'Data pipelines, ETL/ELT workflows, Spark, Kafka, Airflow, and data warehousing',
    keywords: [
      'data engineering', 'etl', 'elt', 'spark', 'pyspark', 'kafka', 'airflow',
      'dbt', 'hadoop', 'hive', 'snowflake', 'databricks', 'data warehouse',
      'data lake', 'bigquery', 'redshift', 'sql', 'data pipeline', 'presto', 'trino'
    ],
  },
  {
    id: 'data-scientist',
    title: 'Data Scientist',
    description: 'Statistics, predictive modeling, exploratory data analysis, Pandas, and ML experiments',
    keywords: [
      'pandas', 'numpy', 'scipy', 'statistics', 'statistical modeling', 'eda',
      'exploratory data analysis', 'tableau', 'power bi', 'powerbi', 'data visualization',
      'data analysis', 'regression', 'classification', 'clustering', 'scikit-learn',
      'sklearn', 'matplotlib', 'seaborn', 'jupyter'
    ],
  },
  {
    id: 'devops-engineer',
    title: 'DevOps Engineer',
    description: 'CI/CD pipelines, cloud infrastructure (AWS/Azure/GCP), Kubernetes, and observability',
    keywords: [
      'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'aws', 'azure', 'gcp',
      'google cloud', 'ci/cd', 'github actions', 'gitlab ci', 'jenkins', 'linux',
      'bash', 'shell scripting', 'prometheus', 'grafana', 'helm', 'cloudformation'
    ],
  },
  {
    id: 'full-stack-developer',
    title: 'Full Stack Developer',
    description: 'End-to-end web applications, full lifecycle development, UI + APIs + databases',
    keywords: [
      'javascript', 'typescript', 'react', 'nextjs', 'next.js', 'vue', 'angular',
      'nodejs', 'node.js', 'express', 'nest.js', 'nestjs', 'full stack', 'fullstack',
      'html', 'css', 'tailwind', 'graphql', 'rest api', 'restful apis', 'postgresql', 'mongodb'
    ],
  },
  {
    id: 'software-engineer',
    title: 'Software Engineer',
    description: 'Data structures, algorithms, object-oriented design, problem-solving, testing, and clean code',
    keywords: [
      'dsa', 'algorithms', 'data structures', 'clean code', 'oop', 'design patterns',
      'git', 'github', 'system design', 'unit test', 'refactoring',
      'problem solving', 'software engineering', 'code review', 'debugging'
    ],
  },
  {
    id: 'tester-qa-qc',
    title: 'Tester / QA / QC',
    description: 'Test plans, automated testing (Playwright/Selenium), test cases, and quality assurance',
    keywords: [
      'testing', 'qa', 'qc', 'quality assurance', 'test automation', 'test cases',
      'playwright', 'selenium', 'cypress', 'jest', 'pytest', 'postman',
      'manual testing', 'automation testing', 'regression testing', 'unit testing',
      'performance testing', 'jmeter', 'load testing', 'bug report', 'test plan'
    ],
  },
  {
    id: 'web-developer',
    title: 'Web Developer',
    description: 'Modern web UI development, HTML5, CSS3/Tailwind, JavaScript/TypeScript, and frontend performance',
    keywords: [
      'html', 'css', 'javascript', 'typescript', 'frontend', 'web development',
      'react', 'vue', 'tailwind', 'responsive design', 'sass', 'scss',
      'webpack', 'vite', 'dom', 'ui development', 'browser compatibility'
    ],
  },
]

export interface RoleMatchResult {
  id: string
  title: string
  score: number // percentage 0-100
  summary: string
  matchedSkills: string[]
  relevantExperienceCount: number
}

function escapeRegExp(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function skillMatchesKeyword(skill: string, keyword: string): boolean {
  const s = skill.toLowerCase().trim()
  const k = keyword.toLowerCase().trim()

  if (s === k) return true

  // Short acronyms or keywords require exact matching to avoid false substring hits
  if (k.length <= 2 || s.length <= 2) {
    return s === k
  }

  // Check if keyword is an exact word or phrase match within the skill string
  const regex = new RegExp(`(^|[^a-z0-9])${escapeRegExp(k)}([^a-z0-9]|$)`, 'i')
  if (regex.test(s)) return true

  // Check reverse if the skill is multi-word and keyword matches
  const reverseRegex = new RegExp(`(^|[^a-z0-9])${escapeRegExp(s)}([^a-z0-9]|$)`, 'i')
  return reverseRegex.test(k)
}

function textContainsKeyword(text: string, keyword: string): boolean {
  const k = keyword.toLowerCase().trim()
  if (k.length <= 2) {
    const regex = new RegExp(`\\b${escapeRegExp(k)}\\b`, 'i')
    return regex.test(text)
  }
  const regex = new RegExp(`(^|[^a-z0-9])${escapeRegExp(k)}([^a-z0-9]|$)`, 'i')
  return regex.test(text)
}

/**
 * Calculates or formats top 6 role matches from Candidate Profile.
 * - Prioritizes AI-generated role_matches from backend.
 * - Falls back to semantic keyword analysis if AI role_matches is not present.
 * - Always returns exactly 6 roles sorted descending.
 * - Roles with 0% match have empty matched skills.
 */
export function calculateRoleMatches(profile: CandidateProfile | null | undefined): RoleMatchResult[] {
  if (!profile) return []

  const roleMapById = new Map<string, RoleDefinition>(INTERVIEW_ROLES.map((r) => [r.id, r]))
  const roleMapByTitle = new Map<string, RoleDefinition>(
    INTERVIEW_ROLES.map((r) => [r.title.toLowerCase().trim(), r]),
  )

  // 1. If AI returned structured role_matches from Gemini backend
  if (profile.role_matches && profile.role_matches.length > 0) {
    const parsedMatches: RoleMatchResult[] = []
    const seenRoleIds = new Set<string>()

    for (const rm of profile.role_matches) {
      const matchedRole =
        (rm.role_id ? roleMapById.get(rm.role_id) : undefined) ||
        roleMapByTitle.get(rm.title.toLowerCase().trim())

      const roleId = matchedRole?.id || rm.role_id || rm.id || rm.title.toLowerCase().replace(/[^a-z0-9]/g, '-')
      const roleTitle = matchedRole?.title || rm.title
      const score = Math.max(0, Math.min(100, Math.round(rm.score || 0)))
      const matchedSkills = rm.matched_skills || rm.matchedSkills || []
      const expCount = rm.relevant_experience_count ?? rm.relevantExperienceCount ?? 0

      if (!seenRoleIds.has(roleId)) {
        seenRoleIds.add(roleId)
        parsedMatches.push({
          id: roleId,
          title: roleTitle,
          score,
          summary: score > 0 ? `${matchedSkills.length} matched skills · ${expCount} relevant experiences` : '',
          matchedSkills: score > 0 ? matchedSkills : [],
          relevantExperienceCount: score > 0 ? expCount : 0,
        })
      }
    }

    // Sort by score descending
    parsedMatches.sort((a, b) => b.score - a.score)

    // Fill with remaining roles up to 6 if needed
    for (const role of INTERVIEW_ROLES) {
      if (parsedMatches.length >= 6) break
      if (!seenRoleIds.has(role.id)) {
        seenRoleIds.add(role.id)
        parsedMatches.push({
          id: role.id,
          title: role.title,
          score: 0,
          summary: '',
          matchedSkills: [],
          relevantExperienceCount: 0,
        })
      }
    }

    return parsedMatches.slice(0, 6)
  }

  // 2. Fallback: Semantic matching across all 10 roles
  const originalSkills = profile.skills || []
  const experiences = profile.experiences || []
  const projects = profile.projects || []

  const profileCorpus = [
    ...originalSkills,
    profile.recent_role || '',
    profile.specialization || '',
    ...experiences.flatMap((e) => [e.title, e.company, e.description, ...(e.technologies || [])]),
    ...projects.flatMap((p) => [p.name, p.role || '', p.description, ...(p.technologies || [])]),
  ]
    .join(' ')
    .toLowerCase()

  const rawScores: { role: RoleDefinition; score: number; matchedSkills: string[]; relevantExperienceCount: number }[] = []

  for (const role of INTERVIEW_ROLES) {
    const matchedSkills = originalSkills.filter((origSkill) =>
      role.keywords.some((kw) => skillMatchesKeyword(origSkill, kw)),
    )

    let corpusHits = 0
    for (const kw of role.keywords) {
      if (textContainsKeyword(profileCorpus, kw)) {
        corpusHits += 1
      }
    }

    let relevantExperienceCount = 0
    for (const exp of experiences) {
      const expText = `${exp.title} ${exp.company} ${exp.description} ${(exp.technologies || []).join(' ')}`
      if (role.keywords.some((kw) => textContainsKeyword(expText, kw))) {
        relevantExperienceCount += 1
      }
    }
    for (const proj of projects) {
      const projText = `${proj.name} ${proj.role || ''} ${proj.description} ${(proj.technologies || []).join(' ')}`
      if (role.keywords.some((kw) => textContainsKeyword(projText, kw))) {
        relevantExperienceCount += 1
      }
    }

    const rawScore = matchedSkills.length * 4 + corpusHits * 1.5 + relevantExperienceCount * 2.5

    if (rawScore > 0) {
      rawScores.push({
        role,
        score: rawScore,
        matchedSkills,
        relevantExperienceCount,
      })
    }
  }

  const resultMatches: RoleMatchResult[] = []
  const includedRoleIds = new Set<string>()

  if (rawScores.length > 0) {
    const totalScore = rawScores.reduce((sum, item) => sum + item.score, 0)
    rawScores.sort((a, b) => b.score - a.score)

    for (const item of rawScores) {
      const pct = Math.max(1, Math.round((item.score / totalScore) * 100))
      includedRoleIds.add(item.role.id)
      resultMatches.push({
        id: item.role.id,
        title: item.role.title,
        score: pct,
        summary: `${item.matchedSkills.length} matched skills · ${item.relevantExperienceCount} relevant experiences`,
        matchedSkills: item.matchedSkills,
        relevantExperienceCount: item.relevantExperienceCount,
      })
    }
  }

  // Ensure exactly 6 roles by adding 0% un-matched roles from INTERVIEW_ROLES
  for (const role of INTERVIEW_ROLES) {
    if (resultMatches.length >= 6) break
    if (!includedRoleIds.has(role.id)) {
      includedRoleIds.add(role.id)
      resultMatches.push({
        id: role.id,
        title: role.title,
        score: 0,
        summary: '',
        matchedSkills: [],
        relevantExperienceCount: 0,
      })
    }
  }

  return resultMatches.slice(0, 6)
}
