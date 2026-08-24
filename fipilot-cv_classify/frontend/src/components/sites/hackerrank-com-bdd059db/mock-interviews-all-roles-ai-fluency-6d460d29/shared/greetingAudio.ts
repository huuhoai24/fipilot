const GREETING_AUDIO_PATH = "/audio/interview-greeting.wav";

let greetingAudio: HTMLAudioElement | null = null;

function ensureGreetingAudio(): HTMLAudioElement | null {
  if (typeof Audio === "undefined") return null;
  if (greetingAudio === null) {
    greetingAudio = new Audio(GREETING_AUDIO_PATH);
    greetingAudio.preload = "auto";
    greetingAudio.muted = false;
    greetingAudio.volume = 1;
  }
  return greetingAudio;
}

export function preloadInterviewGreeting() {
  ensureGreetingAudio()?.load();
}

export function getInterviewGreetingAudio() {
  const audio = ensureGreetingAudio();
  if (audio?.ended) audio.currentTime = 0;
  return audio;
}
