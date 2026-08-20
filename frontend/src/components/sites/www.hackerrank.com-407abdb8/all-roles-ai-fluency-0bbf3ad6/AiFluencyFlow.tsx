"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowLeft, ArrowRight, CheckCircle2, Clock3, Headphones, Lightbulb, Mic, MonitorCheck, RotateCcw, ShieldCheck, Sparkles, X } from "lucide-react";
import "./ai-fluency.css";

type FlowStep = "landing" | "setup" | "instructions" | "interview" | "submitting" | "complete" | "results";

const QUESTIONS = [
  "Tell me about a recent project where AI helped you solve a meaningful problem. What was your role?",
  "How do you decide when an AI-generated answer is trustworthy enough to use?",
  "Describe a time you improved a prompt or workflow after the first result fell short.",
];

const BENEFITS = [
  ["Focus on projects and experience", "Discuss your experience with AI tools, how you use AI in your work, and your understanding of AI concepts.", Lightbulb],
  ["A realistic, voice-based interview", "Build confidence by speaking naturally, just like you would in a real interview.", Headphones],
  ["Demonstrate AI fluency", "Show how you stay current with AI trends, evaluate tools, and apply AI effectively in real-world scenarios.", Sparkles],
  ["Improve with clear, actionable feedback", "Get specific feedback on your clarity, depth of examples, and how well you communicate your AI experience.", CheckCircle2],
] as const;

export function AiFluencyFlow() {
  const [step, setStep] = useState<FlowStep>("landing");
  const [questionIndex, setQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<string[]>(["", "", ""]);
  const [seconds, setSeconds] = useState(30 * 60);
  const [showExit, setShowExit] = useState(false);
  const [showExhausted, setShowExhausted] = useState(false);

  useEffect(() => {
    if (step !== "interview") return;
    const timer = window.setInterval(() => setSeconds((value) => Math.max(0, value - 1)), 1000);
    return () => window.clearInterval(timer);
  }, [step]);

  useEffect(() => {
    if (step !== "submitting") return;
    const timer = window.setTimeout(() => setStep(questionIndex === QUESTIONS.length - 1 ? "complete" : "interview"), 900);
    return () => window.clearTimeout(timer);
  }, [questionIndex, step]);

  useEffect(() => {
    if (step !== "complete") return;
    const timer = window.setTimeout(() => setStep("results"), 1500);
    return () => window.clearTimeout(timer);
  }, [step]);

  const setAnswer = (value: string) => {
    setAnswers((current) => current.map((answer, index) => index === questionIndex ? value : answer));
  };
  const nextQuestion = () => {
    if (questionIndex < QUESTIONS.length - 1) setQuestionIndex((current) => current + 1);
  };
  const submit = () => setStep("submitting");
  const restart = () => {
    setQuestionIndex(0);
    setAnswers(["", "", ""]);
    setSeconds(30 * 60);
    setShowExit(false);
    setShowExhausted(false);
    setStep("landing");
  };
  const minutes = String(Math.floor(seconds / 60)).padStart(2, "0");
  const remainingSeconds = String(seconds % 60).padStart(2, "0");

  return <main className="ai-flow">
    <header className="ai-flow__header"><Link href="/" className="ai-flow__brand">Fipilot</Link><span>Prepare</span><span>Certify</span><span>Compete</span><Link href="/" className="ai-flow__dashboard">Dashboard</Link></header>
    {step === "landing" && <section className="ai-flow__landing ai-flow__shell">
      <div className="ai-flow__intro"><p className="ai-flow__eyebrow">AI-POWERED MOCK INTERVIEW</p><h1>AI Fluency</h1><h2>Practice with AI-powered voice interviews</h2>
        {showExhausted && <div className="ai-flow__notice"><span>You have no mock interviews left</span><button onClick={() => setShowExhausted(false)}>Dismiss</button></div>}
        <div className="ai-flow__benefits">{BENEFITS.map(([title, description, Icon]) => <article key={title}><Icon size={21}/><div><h3>{title}</h3><p>{description}</p></div></article>)}</div>
        <div className="ai-flow__actions"><button className="ai-flow__primary" onClick={() => setStep("setup")}>Start Interview <ArrowRight size={18}/></button><button className="ai-flow__text-button" onClick={() => setShowExhausted(true)}>View credit status</button></div>
      </div>
      <aside className="ai-flow__hero"><div className="ai-flow__orb"><Sparkles size={42}/></div><p>AI FLUENCY SESSION</p><strong>30 mins</strong><span>Voice-based practice</span><div className="ai-flow__wave">◒ ◓ ◒ ◓ ◒ ◓ ◒</div></aside>
    </section>}
    {step === "setup" && <Stage title="Set up for your interview" subtitle="Check that your equipment is ready before the interview begins." back={() => setStep("landing")} next={() => setStep("instructions")} nextLabel="Continue"><div className="ai-flow__check-grid"><CheckCard icon={<Mic/>} title="Microphone" detail="Your microphone is ready"/><CheckCard icon={<MonitorCheck/>} title="Camera" detail="Camera optional for this practice"/><CheckCard icon={<ShieldCheck/>} title="A quiet space" detail="Find a place where you can speak freely"/></div><p className="ai-flow__hint">Your responses are used only to generate mock interview feedback.</p></Stage>}
    {step === "instructions" && <Stage title="How this interview works" subtitle="You will answer three AI fluency questions in a focused, timed session." back={() => setStep("setup")} next={() => setStep("interview")} nextLabel="Begin Interview"><ol className="ai-flow__instructions"><li><b>Speak naturally.</b> Share specific examples from your work with AI tools.</li><li><b>Take your time.</b> You have 30 minutes for the complete session.</li><li><b>Review your feedback.</b> Get practical suggestions when the interview ends.</li></ol></Stage>}
    {(step === "interview" || step === "submitting") && <section className="ai-flow__interview ai-flow__shell"><div className="ai-flow__session-bar"><button aria-label="Exit interview" onClick={() => setShowExit(true)}><X/></button><span>AI Fluency mock interview</span><time><Clock3 size={17}/>{minutes}:{remainingSeconds}</time></div><div className="ai-flow__progress"><span style={{width: `${((questionIndex + 1) / QUESTIONS.length) * 100}%`}}/></div><div className="ai-flow__question"><p>QUESTION {questionIndex + 1} OF {QUESTIONS.length}</p><h1>{QUESTIONS[questionIndex]}</h1><div className="ai-flow__interviewer"><div>AI</div><span>Your AI interviewer is listening</span></div><textarea value={answers[questionIndex]} onChange={(event) => setAnswer(event.target.value)} placeholder="Type a response for this interactive clone, or use this space to prepare your spoken answer." disabled={step === "submitting"}/><div className="ai-flow__question-actions"><button className="ai-flow__secondary" disabled={questionIndex === 0} onClick={() => setQuestionIndex((current) => current - 1)}><ArrowLeft size={17}/>Back</button>{questionIndex < QUESTIONS.length - 1 ? <button className="ai-flow__primary" onClick={nextQuestion}>Next <ArrowRight size={17}/></button> : <button className="ai-flow__primary" onClick={submit} disabled={step === "submitting"}>{step === "submitting" ? "Submitting…" : "Finish interview"}</button>}</div></div></section>}
    {step === "complete" && <section className="ai-flow__center ai-flow__shell"><div className="ai-flow__loader"/><p className="ai-flow__eyebrow">INTERVIEW COMPLETE</p><h1>Creating your feedback</h1><p>We’re reviewing your responses and preparing personalized AI fluency insights.</p></section>}
    {step === "results" && <section className="ai-flow__results ai-flow__shell"><p className="ai-flow__eyebrow">AI FLUENCY MOCK INTERVIEW</p><h1>Your feedback is ready</h1><div className="ai-flow__score"><div><span>AI fluency score</span><strong>82</strong><small>Strong</small></div><p>You communicated a thoughtful approach to using AI, with clear attention to validation and iteration.</p></div><div className="ai-flow__feedback"><article><h2>What went well</h2><p>You used concrete examples and explained how you verify AI output before relying on it.</p></article><article><h2>Opportunity to improve</h2><p>Make trade-offs more explicit: describe the constraints that influence which AI tool or workflow you choose.</p></article></div><div className="ai-flow__actions"><button className="ai-flow__primary" onClick={restart}><RotateCcw size={17}/>Practice again</button><Link className="ai-flow__secondary ai-flow__link-button" href="/">Back to dashboard</Link></div></section>}
    {showExit && <div className="ai-flow__modal-backdrop" role="presentation"><div className="ai-flow__modal" role="dialog" aria-modal="true" aria-labelledby="exit-title"><h2 id="exit-title">End this interview?</h2><p>Your progress will be lost and you will return to the AI Fluency start screen.</p><div><button className="ai-flow__secondary" onClick={() => setShowExit(false)}>Keep practicing</button><button className="ai-flow__danger" onClick={restart}>End interview</button></div></div></div>}
  </main>;
}

function Stage({ title, subtitle, children, back, next, nextLabel }: { title: string; subtitle: string; children: React.ReactNode; back: () => void; next: () => void; nextLabel: string }) { return <section className="ai-flow__stage ai-flow__shell"><p className="ai-flow__eyebrow">AI FLUENCY MOCK INTERVIEW</p><h1>{title}</h1><p className="ai-flow__subtitle">{subtitle}</p><div className="ai-flow__stage-card">{children}</div><div className="ai-flow__actions"><button className="ai-flow__secondary" onClick={back}><ArrowLeft size={17}/>Back</button><button className="ai-flow__primary" onClick={next}>{nextLabel}<ArrowRight size={17}/></button></div></section>; }
function CheckCard({ icon, title, detail }: { icon: React.ReactNode; title: string; detail: string }) { return <article className="ai-flow__check"><span>{icon}</span><div><h2>{title}</h2><p>{detail}</p></div><CheckCircle2 className="ai-flow__success" size={20}/></article>; }
