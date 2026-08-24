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
    description: 'Machine Learning, Deep Learning, Generative AI, LLMs, PyTorch, and AI system design',
    keywords: [
      'python', 'pytorch', 'tensorflow', 'keras', 'scikit-learn', 'llm', 'nlp', 'cv',
      'openai', 'langchain', 'langgraph', 'agentic ai', 'huggingface', 'transformers',
      'deep learning', 'machine learning', 'rag', 'vector database', 'embedding', 'fastapi',
      'onnx', 'tensorrt', 'bert', 'gpt', 'yolo', 'opencv', 'computer vision', 'prompt engineering'
    ],
  },
  {
    id: 'backend-developer',
    title: 'Backend Developer',
    description: 'APIs, relational & NoSQL databases, microservices, system architecture, and concurrency',
    keywords: [
      'java', 'spring', 'go', 'golang', 'c#', '.net', 'nodejs', 'express', 'nest',
      'python', 'django', 'fastapi', 'sql', 'postgresql', 'mysql', 'mongodb', 'redis',
      'kafka', 'rabbitmq', 'docker', 'grpc', 'rest api', 'restful apis', 'microservices'
    ],
  },
  {
    id: 'full-stack-developer',
    title: 'Full Stack Developer',
    description: 'End-to-end web applications, full lifecycle development, UI + APIs + databases',
    keywords: [
      'javascript', 'typescript', 'react', 'nextjs', 'nodejs', 'express', 'python',
      'fastapi', 'django', 'sql', 'postgresql', 'mongodb', 'docker', 'rest api', 'restful apis', 'git'
    ],
  },
  {
    id: 'data-scientist',
    title: 'Data Scientist',
    description: 'Statistics, predictive modeling, data analysis, experiments, and ML models',
    keywords: [
      'python', 'r', 'pandas', 'numpy', 'scipy', 'statistics', 'eda', 'sql',
      'tableau', 'power bi', 'visualization', 'data analysis', 'regression', 'classification',
      'clustering', 'scikit-learn', 'matplotlib', 'seaborn', 'spark'
    ],
  },
  {
    id: 'devops-engineer',
    title: 'DevOps Engineer',
    description: 'CI/CD pipelines, cloud infrastructure (AWS/Azure/GCP), Kubernetes, and observability',
    keywords: [
      'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'aws', 'azure', 'gcp',
      'ci/cd', 'github actions', 'gitlab ci', 'jenkins', 'linux', 'bash', 'prometheus', 'grafana'
    ],
  },
  {
    id: 'software-engineer',
    title: 'Software Engineer',
    description: 'Data structures, algorithms, object-oriented design, problem-solving, and clean code',
    keywords: [
      'dsa', 'algorithms', 'data structures', 'clean code', 'oop', 'design patterns',
      'git', 'system design', 'testing', 'unit test', 'refactoring', 'problem solving', 'playwright'
    ],
  },
]

export interface RoleMatchResult {
  id: string
  title: string
  score: number // percentage, e.g. 59%
  summary: string
  matchedSkills: string[]
  relevantExperienceCount: number
}

export function calculateRoleMatches(profile: CandidateProfile | null | undefined): RoleMatchResult[] {
  if (!profile) return []

  const originalSkills = profile.skills || []
  const experiences = profile.experiences || []
  const projects = profile.projects || []

  // Collect all text from experiences & projects
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
    // Find matching skills preserving original casing
    const matchedSkills = originalSkills.filter((origSkill) => {
      const lower = origSkill.toLowerCase().trim()
      return role.keywords.some((kw) => lower.includes(kw) || kw.includes(lower))
    })

    // Count keyword mentions in corpus
    let corpusHits = 0
    for (const kw of role.keywords) {
      if (profileCorpus.includes(kw)) {
        corpusHits += 1
      }
    }

    // Count how many experiences/projects match this role
    let relevantExperienceCount = 0
    for (const exp of experiences) {
      const expText = `${exp.title} ${exp.company} ${exp.description} ${(exp.technologies || []).join(' ')}`.toLowerCase()
      if (role.keywords.some((kw) => expText.includes(kw))) {
        relevantExperienceCount += 1
      }
    }
    for (const proj of projects) {
      const projText = `${proj.name} ${proj.role || ''} ${proj.description} ${(proj.technologies || []).join(' ')}`.toLowerCase()
      if (role.keywords.some((kw) => projText.includes(kw))) {
        relevantExperienceCount += 1
      }
    }

    // Weight formula
    const rawScore = matchedSkills.length * 3 + corpusHits * 1.5 + relevantExperienceCount * 2

    if (rawScore > 0) {
      rawScores.push({
        role,
        score: rawScore,
        matchedSkills,
        relevantExperienceCount,
      })
    }
  }

  if (rawScores.length === 0) {
    return INTERVIEW_ROLES.slice(0, 4).map((r, index) => ({
      id: r.id,
      title: r.title,
      score: index === 0 ? 40 : index === 1 ? 30 : index === 2 ? 20 : 10,
      summary: r.description,
      matchedSkills: [],
      relevantExperienceCount: 0,
    }))
  }

  const totalScore = rawScores.reduce((sum, item) => sum + item.score, 0)

  return rawScores
    .map((item) => {
      const pct = Math.max(3, Math.round((item.score / totalScore) * 100))
      return {
        id: item.role.id,
        title: item.role.title,
        score: pct,
        summary: `${item.matchedSkills.length} matched skills · ${item.relevantExperienceCount} relevant experiences`,
        matchedSkills: item.matchedSkills,
        relevantExperienceCount: item.relevantExperienceCount,
      }
    })
    .sort((a, b) => b.score - a.score)
}
