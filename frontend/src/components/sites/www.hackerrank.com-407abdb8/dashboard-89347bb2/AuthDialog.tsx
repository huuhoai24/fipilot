"use client";

import { type CSSProperties, type FormEvent, useEffect, useRef, useState } from "react";
import { CheckIcon, CloseIcon } from "../shared/icons";
import { loginUser, registerUser } from "@/lib/auth";

export type AuthMode = "login" | "signup";

interface AuthDialogProps {
  initialMode: AuthMode;
  onClose: () => void;
}

interface FieldError {
  field: string;
  message: string;
}

const dialogStyle: CSSProperties = {
  position: "fixed",
  top: "50%",
  left: "50%",
  zIndex: 990,
  minHeight: 120,
  borderRadius: 12,
  background: "#FFFFFF",
  boxSizing: "border-box",
  transform: "translate(-50%, -50%)",
  fontFamily: "var(--hr-font-satoshi)",
};

const authBoxStyle: CSSProperties = {
  width: "100%",
  boxSizing: "border-box",
};

const overlayStyle: CSSProperties = {
  position: "fixed",
  inset: 0,
  zIndex: 989,
  background: "rgba(18, 20, 24, 0.85)",
};

const headerRowStyle: CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "flex-start",
  width: "100%",
};

const titlesStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
};

const titleStyle: CSSProperties = {
  margin: 0,
  fontSize: 24,
  fontWeight: 700,
  lineHeight: "36px",
  color: "#121418",
};

const closeButtonStyle: CSSProperties = {
  width: 40,
  height: 40,
  minWidth: 40,
  minHeight: 40,
  display: "inline-flex",
  justifyContent: "center",
  alignItems: "center",
  borderRadius: 8,
  border: "1px solid #9091A8",
  background: "transparent",
  color: "#121418",
  cursor: "pointer",
  padding: 0,
  transition:
    "color .2s ease-in-out, background-color .2s ease-in-out, border-color .2s ease-in-out",
};

const subtitleStyle: CSSProperties = {
  margin: "8px 0 0",
  fontSize: 14,
  fontWeight: 400,
  lineHeight: "20px",
  color: "#121418",
};

const formStyle: CSSProperties = {
  marginTop: 16,
  display: "flex",
  flexDirection: "column",
  gap: 16,
};

const fieldStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 4,
};

const inputStyle: CSSProperties = {
  width: "100%",
  height: 40,
  padding: "10px 12px",
  borderRadius: 8,
  border: "1px solid #9091A8",
  background: "#FFFFFF",
  color: "#1F202A",
  fontSize: 14,
  boxSizing: "border-box",
  fontFamily: "var(--hr-font-satoshi)",
  outline: "none",
  caretColor: "#1F202A",
  transition: "border-color .2s ease-in-out",
};

const submitStyle: CSSProperties = {
  width: "100%",
  height: 48,
  padding: "16px 20px",
  borderRadius: 8,
  border: "none",
  fontSize: 14,
  fontWeight: 700,
  lineHeight: "20px",
  cursor: "pointer",
  fontFamily: "var(--hr-font-satoshi)",
  transition:
    "color .2s ease-in-out, background-color .2s ease-in-out, border-color .2s ease-in-out",
};

const checkboxStyle: CSSProperties = {
  width: 20,
  height: 20,
  display: "inline-flex",
  justifyContent: "center",
  alignItems: "center",
  borderRadius: 4,
  border: "1px solid #9091A8",
  background: "#F7F8FD",
  color: "#FFFFFF",
  cursor: "pointer",
  padding: 0,
  transition:
    "color .2s ease-in-out, background-color .2s ease-in-out, border-color .2s ease-in-out",
};

const checkboxCheckedStyle: CSSProperties = {
  ...checkboxStyle,
  background: "#121418",
  borderColor: "#121418",
};

const linkStyle: CSSProperties = {
  fontSize: 14,
  fontWeight: 500,
  lineHeight: "20px",
  color: "#2358DB",
  textDecoration: "none",
  cursor: "pointer",
};

const footerRowStyle: CSSProperties = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  margin: "32px 0 16px",
};

const footerTextStyle: CSSProperties = {
  margin: 0,
  fontSize: 16,
  fontWeight: 400,
  lineHeight: "24px",
  color: "#121418",
};

const footerLinkStyle: CSSProperties = {
  ...linkStyle,
  fontSize: 16,
  lineHeight: "24px",
};

const errorStyle: CSSProperties = {
  margin: 0,
  fontSize: 12,
  fontWeight: 400,
  lineHeight: "16px",
  color: "#D32F2F",
};

const dialogCss = `
.auth-dialog { width: 548px; max-width: 548px; max-height: calc(100% - 128px); }
.auth-box { padding: 48px; }
.auth-dialog-backdrop { animation: hr-auth-fade .15s cubic-bezier(.16,1,.3,1); }
.auth-dialog-panel { animation: hr-auth-in .15s cubic-bezier(.16,1,.3,1); }
@keyframes hr-auth-fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes hr-auth-in { from { opacity: 0; transform: translate(-50%, calc(-50% - 20px)) scale(.96); } to { opacity: 1; transform: translate(-50%, -50%) scale(1); } }
.auth-input:hover, .auth-input:focus { border-color: #63646F; }
.auth-input::placeholder { color: #63646F; font-weight: 500; }
.auth-close-btn:hover, .auth-checkbox:hover { background: #EBEBF3; }
.auth-submit:not(:disabled):hover { background: #0E612C; }
.auth-footer-link:hover { text-decoration: underline; text-underline-offset: 4px; }
@media (max-width: 767px) {
  .auth-dialog { width: min(548px, 80vw); max-height: 95%; }
  .auth-box { padding: 32px; }
}
`;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function AuthDialog({ initialMode, onClose }: AuthDialogProps) {
  const [mode, setMode] = useState<AuthMode>(initialMode);
  const [closing, setClosing] = useState(false);
  const [username, setUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [authError, setAuthError] = useState("");
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "";
    };
  }, []);

  useEffect(() => {
    const focusable = panelRef.current?.querySelector<HTMLInputElement>("input");
    focusable?.focus();
  }, [mode, submitted]);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape" && !closing) {
        setClosing(true);
        window.setTimeout(onClose, 150);
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [closing, onClose]);

  function handleClose() {
    if (closing) return;
    setClosing(true);
    window.setTimeout(onClose, 150);
  }

  function switchMode(next: AuthMode) {
    setMode(next);
    setErrors([]);
    setSubmitted(false);
    setUsername("");
    setLoginPassword("");
    setRememberMe(false);
    setFullName("");
    setEmail("");
    setSignupPassword("");
    setAuthError("");
  }

  function clearError(field: string) {
    setErrors((current) => current.filter((error) => error.field !== field));
  }

  function validateLogin(): FieldError[] {
    const next: FieldError[] = [];
    if (username.trim() === "") {
      next.push({ field: "username", message: "Please enter your email address." });
    } else if (!EMAIL_RE.test(username.trim())) {
      next.push({ field: "username", message: "Please enter a valid email address." });
    }
    if (loginPassword.trim() === "") {
      next.push({ field: "loginPassword", message: "Please enter your password." });
    }
    return next;
  }

  function validateSignup(): FieldError[] {
    const next: FieldError[] = [];
    if (fullName.trim() === "") {
      next.push({ field: "fullName", message: "Please enter your full name." });
    }
    if (email.trim() === "") {
      next.push({ field: "email", message: "Please enter your email address." });
    } else if (!EMAIL_RE.test(email.trim())) {
      next.push({ field: "email", message: "Please enter a valid email address." });
    }
    if (signupPassword.trim() === "") {
      next.push({ field: "signupPassword", message: "Please enter a password." });
    } else if (signupPassword.length < 8) {
      next.push({
        field: "signupPassword",
        message: "Your password must be at least 8 characters long.",
      });
    }
    return next;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const next = mode === "login" ? validateLogin() : validateSignup();
    if (next.length > 0) {
      setErrors(next);
      return;
    }
    setErrors([]);
    setSubmitting(true);
    setAuthError("");
    try {
      if (mode === "signup") {
        await registerUser(fullName.trim(), email.trim(), signupPassword);
      } else {
        await loginUser(username.trim(), loginPassword);
      }
      setSubmitted(true);
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : "Authentication failed");
    } finally {
      setSubmitting(false);
    }
  }

  function errorFor(field: string): string | undefined {
    return errors.find((error) => error.field === field)?.message;
  }

  const loginValid = username.trim() !== "" && loginPassword.trim() !== "";
  const signupValid =
    fullName.trim() !== "" && email.trim() !== "" && signupPassword.trim() !== "";

  return (
    <div role="presentation">
      <style>{dialogCss}</style>
      <div
        className="auth-dialog-backdrop"
        style={overlayStyle}
        onClick={handleClose}
        aria-hidden="true"
      />
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="auth-dialog-title"
        data-state={closing ? "closed" : "open"}
        className="auth-dialog auth-dialog-panel"
        style={dialogStyle}
      >
        <div className="auth-box" style={authBoxStyle}>
          <div style={headerRowStyle}>
            <div style={titlesStyle}>
              {mode === "login" ? (
                <>
                  <h1 id="auth-dialog-title" style={titleStyle}>
                    Welcome Back!
                  </h1>
                  <h1 style={titleStyle}>Login to your account</h1>
                </>
              ) : (
                <>
                  <h1 id="auth-dialog-title" style={titleStyle}>
                    Join us
                  </h1>
                  <h1 style={titleStyle}>Create a Fipilot account</h1>
                </>
              )}
            </div>
            <button
              type="button"
              aria-label="Close"
              className="auth-close-btn"
              style={closeButtonStyle}
              onClick={handleClose}
            >
              <CloseIcon size={20} />
            </button>
          </div>

          {submitted ? (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                padding: "40px 0 8px",
              }}
            >
              <div
                style={{
                  width: 56,
                  height: 56,
                  borderRadius: "50%",
                  background: "#13813A",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <CheckIcon size={32} />
              </div>
              <h2
                style={{
                  margin: "24px 0 0",
                  fontSize: 24,
                  fontWeight: 700,
                  lineHeight: "36px",
                  color: "#121418",
                }}
              >
                {mode === "signup" ? "Account created successfully" : "Welcome back!"}
              </h2>
              <p
                style={{
                  margin: "8px 0 0",
                  fontSize: 14,
                  lineHeight: "20px",
                  color: "#121418",
                }}
              >
                {mode === "signup"
                  ? "You can now sign in with your new credentials."
                  : "You've been signed in."}
              </p>
              <button
                type="button"
                className="auth-submit"
                style={{ ...submitStyle, background: "#13813A", color: "#FFFFFF", marginTop: 24 }}
                onClick={handleClose}
              >
                Continue
              </button>
            </div>
          ) : (
            <>
              {authError ? <p style={errorStyle}>{authError}</p> : null}
              <h4 style={subtitleStyle}>
                {mode === "login"
                  ? "It's nice to see you again. Ready to code?"
                  : "Be part of a 30 million-strong community of developers"}
              </h4>

              <form noValidate style={formStyle} onSubmit={handleSubmit}>
                {mode === "login" ? (
                  <>
                    <div style={fieldStyle}>
                      <input
                        type="text"
                        name="username"
                        autoComplete="username"
                        placeholder="Your email"
                        aria-label="Your email"
                        aria-invalid={errorFor("username") ? true : undefined}
                        className="auth-input"
                        style={errorFor("username") ? { ...inputStyle, borderColor: "#D32F2F" } : inputStyle}
                        value={username}
                        onChange={(event) => {
                          setUsername(event.target.value);
                          clearError("username");
                        }}
                      />
                      {errorFor("username") ? <p style={errorStyle}>{errorFor("username")}</p> : null}
                    </div>
                    <div style={fieldStyle}>
                      <input
                        type="password"
                        name="loginPassword"
                        autoComplete="current-password"
                        placeholder="Your password"
                        aria-label="Your password"
                        aria-invalid={errorFor("loginPassword") ? true : undefined}
                        className="auth-input"
                        style={
                          errorFor("loginPassword")
                            ? { ...inputStyle, borderColor: "#D32F2F" }
                            : inputStyle
                        }
                        value={loginPassword}
                        onChange={(event) => {
                          setLoginPassword(event.target.value);
                          clearError("loginPassword");
                        }}
                      />
                      {errorFor("loginPassword") ? (
                        <p style={errorStyle}>{errorFor("loginPassword")}</p>
                      ) : null}
                    </div>
                    <button
                      type="submit"
                      disabled={!loginValid || submitting}
                      className="auth-submit"
                      style={{
                        ...submitStyle,
                        background: loginValid ? "#13813A" : "#C1C2D6",
                        color: "#FFFFFF",
                      }}
                    >
                      {submitting ? "Please wait..." : "Log In"}
                    </button>
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        height: 22,
                      }}
                    >
                      <div style={{ display: "flex", alignItems: "center" }}>
                        <button
                          type="button"
                          role="checkbox"
                          name="rememberMe"
                          aria-checked={rememberMe}
                          aria-labelledby="remember-me-label"
                          style={rememberMe ? checkboxCheckedStyle : checkboxStyle}
                          className="auth-checkbox"
                          onClick={() => setRememberMe((checked) => !checked)}
                        >
                          {rememberMe ? <CheckIcon size={16} /> : null}
                        </button>
                        <label
                          id="remember-me-label"
                          style={{
                            margin: "0 0 0 8px",
                            fontSize: 14,
                            fontWeight: 400,
                            lineHeight: "20px",
                            color: "#4A4B53",
                            cursor: "pointer",
                          }}
                          onClick={() => setRememberMe((checked) => !checked)}
                        >
                          Remember me
                        </label>
                      </div>
                      <a className="auth-footer-link" href="/auth/forgot_password" style={linkStyle}>
                        Forgot password?
                      </a>
                    </div>
                  </>
                ) : (
                  <>
                    <div style={fieldStyle}>
                      <input
                        type="text"
                        name="fullName"
                        autoComplete="name"
                        placeholder="Full Name"
                        aria-label="Full Name"
                        aria-invalid={errorFor("fullName") ? true : undefined}
                        className="auth-input"
                        style={
                          errorFor("fullName") ? { ...inputStyle, borderColor: "#D32F2F" } : inputStyle
                        }
                        value={fullName}
                        onChange={(event) => {
                          setFullName(event.target.value);
                          clearError("fullName");
                        }}
                      />
                      {errorFor("fullName") ? <p style={errorStyle}>{errorFor("fullName")}</p> : null}
                    </div>
                    <div style={fieldStyle}>
                      <input
                        type="email"
                        name="email"
                        autoComplete="email"
                        placeholder="Email"
                        aria-label="Email"
                        aria-invalid={errorFor("email") ? true : undefined}
                        className="auth-input"
                        style={errorFor("email") ? { ...inputStyle, borderColor: "#D32F2F" } : inputStyle}
                        value={email}
                        onChange={(event) => {
                          setEmail(event.target.value);
                          clearError("email");
                        }}
                      />
                      {errorFor("email") ? <p style={errorStyle}>{errorFor("email")}</p> : null}
                    </div>
                    <div style={fieldStyle}>
                      <input
                        type="password"
                        name="signupPassword"
                        autoComplete="new-password"
                        placeholder="Your password"
                        aria-label="Your password"
                        aria-invalid={errorFor("signupPassword") ? true : undefined}
                        className="auth-input"
                        style={
                          errorFor("signupPassword")
                            ? { ...inputStyle, borderColor: "#D32F2F" }
                            : inputStyle
                        }
                        value={signupPassword}
                        onChange={(event) => {
                          setSignupPassword(event.target.value);
                          clearError("signupPassword");
                        }}
                      />
                      {errorFor("signupPassword") ? (
                        <p style={errorStyle}>{errorFor("signupPassword")}</p>
                      ) : null}
                    </div>
                    <button
                      type="submit"
                      disabled={!signupValid || submitting}
                      className="auth-submit"
                      style={{
                        ...submitStyle,
                        background: signupValid ? "#13813A" : "#C1C2D6",
                        color: "#FFFFFF",
                      }}
                    >
                      {submitting ? "Please wait..." : "Sign up"}
                    </button>
                  </>
                )}
              </form>

              <div style={footerRowStyle}>
                <h4 style={footerTextStyle}>
                  {mode === "login" ? "Don't have an account? " : "Already have an account? "}
                  <a
                    className="auth-footer-link"
                    style={footerLinkStyle}
                    href="#"
                    onClick={(event) => {
                      event.preventDefault();
                      switchMode(mode === "login" ? "signup" : "login");
                    }}
                  >
                    {mode === "login" ? "Sign up" : "Log in"}
                  </a>
                </h4>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
