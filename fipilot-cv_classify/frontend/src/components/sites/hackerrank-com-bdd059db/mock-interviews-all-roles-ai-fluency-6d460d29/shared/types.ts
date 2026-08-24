export type DevicePermissionState = "checking" | "required" | "ready";

export type InterviewPhase =
  | "connecting"
  | "live"
  | "question-transition"
  | "processing";

export type TranscriptMode = "audio" | "chat";
