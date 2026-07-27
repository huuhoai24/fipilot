import React from 'react'
import {
  ArrowRight,
  FileCheck2,
  MessageSquareText,
  Mic,
  ShieldCheck,
  Sparkles,
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import type { InterviewMode } from '@/types'

const modeContent = {
  text: {
    title: 'Text Interview',
    eyebrow: 'Written practice',
    description: 'Practice structured technical answers at your own pace, with follow-up questions shaped by your CV and every response.',
    image: 'https://images.pexels.com/photos/1181341/pexels-photo-1181341.jpeg?cs=srgb&fm=jpg&auto=compress&w=1400',
    imageAlt: 'Software engineer reviewing work on a laptop',
    icon: MessageSquareText,
  },
  voice: {
    title: 'Speech Interview',
    eyebrow: 'Realtime practice',
    description: 'Build confidence speaking through technical decisions in a realistic conversation that adapts to your answers.',
    image: 'https://images.pexels.com/photos/5399034/pexels-photo-5399034.jpeg?cs=srgb&fm=jpg&auto=compress&w=1400',
    imageAlt: 'Professional using a laptop, headphones, and microphone',
    icon: Mic,
  },
} as const

const preparationItems = [
  {
    icon: FileCheck2,
    title: 'Upload your latest CV',
    text: 'We extract the experience and skills that should guide the interview.',
  },
  {
    icon: Sparkles,
    title: 'Choose your target',
    text: 'Set the role level, interview style, language, and session length.',
  },
  {
    icon: ShieldCheck,
    title: 'Review before starting',
    text: 'Nothing begins until your candidate profile and setup look right.',
  },
]

export function InterviewExperienceIntro({ mode }: { mode: InterviewMode }) {
  const content = modeContent[mode]
  const ModeIcon = content.icon

  const scrollToSetup = () => {
    document.getElementById('interview-setup')?.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
    })
  }

  return (
    <section className="animate-fade-in overflow-hidden rounded-[28px] border border-border bg-surface shadow-2xl shadow-black/10">
      <div className="grid lg:grid-cols-[minmax(0,1.05fr)_minmax(340px,.95fr)]">
        <div className="flex min-h-[520px] flex-col justify-between p-7 sm:p-10 lg:p-12">
          <div>
            <div className="flex items-center gap-2 text-sm font-semibold text-accent">
              <ModeIcon className="h-4 w-4" aria-hidden="true" />
              <span>{content.eyebrow}</span>
            </div>
            <h1 className="mt-6 max-w-3xl font-display text-[clamp(3rem,6vw,5.6rem)] font-semibold leading-[0.95] tracking-[-0.055em] text-text-primary">
              {content.title}
            </h1>
            <p className="mt-6 max-w-2xl text-balance text-lg leading-8 text-text-muted">
              {content.description}
            </p>
            <Button className="mt-8 w-full sm:w-auto" size="lg" onClick={scrollToSetup}>
              Set up my interview
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Button>
          </div>

          <div className="mt-12 divide-y divide-border border-y border-border">
            {preparationItems.map(({ icon: Icon, title, text }) => (
              <div key={title} className="grid gap-3 py-4 sm:grid-cols-[24px_180px_1fr] sm:items-start">
                <Icon className="mt-0.5 h-4 w-4 text-accent" aria-hidden="true" />
                <h2 className="text-sm font-semibold text-text-primary">{title}</h2>
                <p className="text-sm leading-6 text-text-muted">{text}</p>
              </div>
            ))}
          </div>
        </div>

        <figure className="relative min-h-[380px] overflow-hidden border-t border-border bg-surface-raised lg:min-h-full lg:border-l lg:border-t-0">
          <img
            src={content.image}
            alt={content.imageAlt}
            className="absolute inset-0 h-full w-full object-cover grayscale-[18%] contrast-[1.05]"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#07110d]/85 via-transparent to-[#07110d]/10" aria-hidden="true" />
          <figcaption className="absolute inset-x-0 bottom-0 p-6 text-sm leading-6 text-white/80 sm:p-8">
            Questions stay grounded in your own projects, decisions, and outcomes.
          </figcaption>
        </figure>
      </div>
    </section>
  )
}
