"use client";

import { type ChangeEvent, type CSSProperties, useEffect, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";
import { MenuIcon, SearchIcon } from "../shared/icons";
import { AuthDialog, type AuthMode } from "./AuthDialog";
import { AUTH_CHANGE_EVENT, getAuthUser, hydrateAuthUser, logoutUser, type AuthUser } from "@/lib/auth";

const CHALLENGES = [
  {
    label: 'Say "Hello, World!" With Python',
    href: "https://www.hackerrank.com/challenges/py-hello-world",
  },
  { label: "Python: Division", href: "/challenges/python-division" },
  { label: "Python Evaluation", href: "/challenges/python-eval" },
  { label: "Python If-Else", href: "/challenges/py-if-else" },
];

const CONTESTS = [
  { label: "Pythonista Practice Session", href: "/contests/pythonista-practice-session" },
  { label: "Pythonist", href: "/contests/pythonist" },
  { label: "Pythonist 2", href: "/contests/pythonist2" },
  { label: "Pythonist 3", href: "/contests/pythonist3" },
];

const HACKERS = [
  { label: "python", href: "https://www.hackerrank.com/python" },
  { label: "python1231", href: "https://www.hackerrank.com/python1231" },
  { label: "python1111118881", href: "https://www.hackerrank.com/python1111118881" },
];

const NAV_LINKS = [
  { label: "Certify", href: "/skills-verification", active: false },
  { label: "Compete", href: "/contests", active: false },
];

const headerStyle: CSSProperties = {
  height: 60,
  background: "#121418",
  borderBottom: "2px solid #1F202A",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  position: "static",
  fontFamily: "var(--hr-font-satoshi)",
};

const desktopNavStyle: CSSProperties = {
  alignItems: "center",
};

const navLinkStyle: CSSProperties = {
  fontSize: 14,
  lineHeight: 60,
  height: 60,
  display: "inline-block",
  color: "#FFF",
  textDecoration: "none",
  fontWeight: 400,
};

const mobileNavStyle: CSSProperties = {
  gap: 8,
  alignItems: "center",
  position: "relative",
};

const hamburgerStyle: CSSProperties = {
  width: 40,
  height: 40,
  borderRadius: 8,
  background: "transparent",
  color: "#FFF",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  cursor: "pointer",
  border: "none",
  padding: 0,
};

const drawerStyle: CSSProperties = {
  position: "absolute",
  top: 48,
  left: -16,
  width: "100vw",
  background: "#FFF",
  padding: 24,
  boxShadow: "rgba(37,69,105,.1) 0 1px 4px, rgba(37,69,105,.1) 0 3px 12px",
  transition: "all .1s ease-in-out",
  zIndex: 999,
};

const drawerListStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 8,
  listStyle: "none",
  margin: 0,
  padding: 0,
};

const drawerLinkStyle: CSSProperties = {
  fontSize: 16,
  color: "#35363F",
  height: 60,
  display: "flex",
  alignItems: "center",
  textDecoration: "none",
};

const searchWrapperStyle: CSSProperties = {
  width: 200,
  position: "relative",
};

const searchInputStyle: CSSProperties = {
  height: 36,
  borderRadius: 8,
  border: "1px solid #797888",
  background: "#121418",
  color: "#FFF",
  padding: "10px 12px 10px 40px",
  fontSize: 14,
  width: "100%",
  boxSizing: "border-box",
  fontFamily: "var(--hr-font-satoshi)",
};

const searchIconStyle: CSSProperties = {
  position: "absolute",
  left: 12,
  top: "50%",
  transform: "translateY(-50%)",
  color: "#9091A8",
  pointerEvents: "none",
  display: "flex",
};

const dropdownStyle: CSSProperties = {
  position: "absolute",
  top: 52,
  left: 0,
  width: 300,
  background: "#FFF",
  borderRadius: 16,
  padding: 24,
  boxShadow: "rgba(37,69,105,.1) 0 1px 4px 0, rgba(37,69,105,.1) 0 3px 12px 0",
  zIndex: 1000,
};

const dropdownHeadingStyle: CSSProperties = {
  fontSize: 16,
  fontWeight: 700,
  color: "#121418",
  margin: 0,
};

const dropdownHrStyle: CSSProperties = {
  border: "none",
  borderTop: "1px solid #63646F",
  margin: "0 0 12px",
};

const dropdownRowStyle: CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginTop: 8,
};

const dropdownLinkStyle: CSSProperties = {
  fontSize: 14,
  color: "#35363F",
  textDecoration: "none",
};

const endedPillStyle: CSSProperties = {
  fontSize: 12,
  fontWeight: 500,
  color: "#121418",
  background: "#EBEBF3",
  borderRadius: "100px",
  padding: "4px 12px",
  whiteSpace: "nowrap",
};

const loginStyle: CSSProperties = {
  height: 40,
  padding: "8px 20px",
  borderRadius: 8,
  border: "1px solid #63646F",
  background: "transparent",
  color: "#FFF",
  fontSize: 14,
  fontWeight: 700,
  cursor: "pointer",
  fontFamily: "var(--hr-font-satoshi)",
  transition:
    "color .2s ease-in-out, background-color .2s ease-in-out, border-color .2s ease-in-out",
};

const signupStyle: CSSProperties = {
  height: 40,
  padding: "8px 20px",
  borderRadius: 8,
  border: "none",
  background: "#20D761",
  color: "#121418",
  fontSize: 14,
  fontWeight: 700,
  cursor: "pointer",
  fontFamily: "var(--hr-font-satoshi)",
  transition:
    "color .2s ease-in-out, background-color .2s ease-in-out, border-color .2s ease-in-out",
};

const headerCss = `
.hr-header-root { padding: 0 32px; }
.hr-brand-word { display: inline-flex; width: 129px; height: 60px; align-items: center; color: #F7F8FD; font-size: 20px; font-weight: 700; line-height: 1; letter-spacing: -.35px; text-decoration: none; }
.hr-header-desktop-nav { display: flex; list-style: none; margin: 0; padding: 0; }
.hr-header-link { padding: 0 24px; }
.hr-header-link:hover { color: #EBEBF3; }
.hr-header-link-active { border-bottom: 4px solid #2EC866; font-weight: 700; }
.hr-header-mobile-nav { display: flex; }
.hr-header-search { display: block; }
.hr-header-login:hover { background-color: #63646F; }
.hr-header-signup:hover { background-color: #BAF3CE; }
.hr-header-profile:hover, .hr-header-profile[data-active] { background-color: #33343E; }
.hr-header-profile-menu button:hover { background-color: #F7F8FD; }
.hr-header-search input:hover { border-color: #C1C2D6; }
.hr-header-search input::placeholder { color: #9091A8; }
.hr-drawer-link:hover { background: #F7F8FD; color: #121418; }
.hr-drawer-link-active { color: #121418; font-weight: 700; }
.hr-search-row a:hover { color: #121418; }
@media (max-width: 768px) {
  .hr-header-root { padding: 0 16px; }
  .hr-header-desktop-nav { display: none; }
  .hr-header-search { display: none; }
  .hr-brand-word { width: 124px; }
}
@media (min-width: 768px) { .hr-header-mobile-nav { display: none; } }
@media (max-width: 1280px) { .hr-header-link { padding: 0 16px; } }
@media (max-width: 1024px) { .hr-header-link { padding: 0 12px; } }
@media (min-width: 1441px) { .hr-header-search { width: 240px; } }
@media (max-width: 1280px) { .hr-header-search { width: 180px; } }
`;

export function Header() {
  const [query, setQuery] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [authMode, setAuthMode] = useState<AuthMode | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [profileOpen, setProfileOpen] = useState(false);

  useEffect(() => {
    const syncUser = () => setUser(getAuthUser());
    syncUser();
    void hydrateAuthUser();
    window.addEventListener(AUTH_CHANGE_EVENT, syncUser);
    window.addEventListener("storage", syncUser);
    return () => {
      window.removeEventListener(AUTH_CHANGE_EVENT, syncUser);
      window.removeEventListener("storage", syncUser);
    };
  }, []);
  const searchRef = useRef<HTMLDivElement>(null);
  const profileRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleMouseDown = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setSearchOpen(false);
      }
      if (profileRef.current && !profileRef.current.contains(event.target as Node)) {
        setProfileOpen(false);
      }
    };
    document.addEventListener("mousedown", handleMouseDown);
    return () => document.removeEventListener("mousedown", handleMouseDown);
  }, []);

  const showDropdown = searchOpen && query.trim() !== "";

  return (
    <header className="hr-header-root" style={headerStyle}>
      <style>{headerCss}</style>
      <div className="hr-header-nav-links hr-flex hr-align-center" style={{ height: "100%" }}>
        <ul className="hr-header-desktop-nav" style={desktopNavStyle}>
          <li>
            <a className="hr-brand-word" href="/dashboard" aria-label="Fipilot Home">
              Fipilot
            </a>
          </li>
          {NAV_LINKS.map((link) => (
            <li key={link.label}>
              <a
                href={link.href}
                className={`hr-header-link${link.active ? " hr-header-link-active" : ""}`}
                style={navLinkStyle}
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>
        <div className="hr-header-mobile-nav" style={mobileNavStyle}>
          <button
            type="button"
            aria-label="Toggle navigation menu"
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen((open) => !open)}
            style={hamburgerStyle}
          >
            <MenuIcon size={20} />
          </button>
          <a className="hr-brand-word" href="/dashboard" aria-label="Fipilot Home">
            Fipilot
          </a>
          <div
            style={{
              ...drawerStyle,
              visibility: mobileOpen ? "visible" : "hidden",
              opacity: mobileOpen ? 1 : 0,
            }}
          >
            <ul style={drawerListStyle}>
              {NAV_LINKS.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    className={`hr-drawer-link${link.active ? " hr-drawer-link-active" : ""}`}
                    style={drawerLinkStyle}
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      <div className="hr-header-right hr-flex hr-align-center" style={{ gap: 8 }}>
        <div ref={searchRef} className="hr-header-search" style={searchWrapperStyle}>
          <input
            ref={inputRef}
            type="search"
            placeholder="Search"
            value={query}
            onChange={(event: ChangeEvent<HTMLInputElement>) => setQuery(event.target.value)}
            onFocus={() => setSearchOpen(true)}
            onKeyDown={(event) => {
              if (event.key === "Escape") {
                setSearchOpen(false);
                inputRef.current?.blur();
              }
            }}
            style={searchInputStyle}
          />
          <span style={searchIconStyle}>
            <SearchIcon size={20} />
          </span>
          {showDropdown && (
            <div style={dropdownStyle}>
              <h3 style={dropdownHeadingStyle}>challenges</h3>
              {CHALLENGES.map((item) => (
                <div key={item.label} className="hr-search-row" style={dropdownRowStyle}>
                  <a href={item.href} style={dropdownLinkStyle}>
                    {item.label}
                  </a>
                </div>
              ))}
              <hr style={dropdownHrStyle} />
              <h3 style={dropdownHeadingStyle}>contests</h3>
              {CONTESTS.map((item) => (
                <div key={item.label} className="hr-search-row" style={dropdownRowStyle}>
                  <a href={item.href} style={dropdownLinkStyle}>
                    {item.label}
                  </a>
                  <span style={endedPillStyle}>ended</span>
                </div>
              ))}
              <hr style={dropdownHrStyle} />
              <h3 style={dropdownHeadingStyle}>hackers</h3>
              {HACKERS.map((item) => (
                <div key={item.label} className="hr-search-row" style={dropdownRowStyle}>
                  <a href={item.href} style={dropdownLinkStyle}>
                    {item.label}
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>
        {user === null ? (
          <>
            <button type="button" className="hr-header-login" style={loginStyle} onClick={() => setAuthMode("login")}>
              Log In
            </button>
            <button type="button" className="hr-header-signup" style={signupStyle} onClick={() => setAuthMode("signup")}>
              Sign Up
            </button>
          </>
        ) : (
          <div ref={profileRef} style={{ position: "relative" }}>
            <button
              type="button"
              className="hr-header-profile"
              data-active={profileOpen || undefined}
              aria-label="Profile menu"
              aria-expanded={profileOpen}
              onClick={() => setProfileOpen((open) => !open)}
              style={{
                width: 56,
                height: 40,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 7,
                padding: 0,
                border: 0,
                borderRadius: 8,
                color: "#EBEBF3",
                background: "transparent",
                cursor: "pointer",
              }}
            >
              <span
                aria-hidden="true"
                style={{
                  width: 32,
                  height: 32,
                  display: "grid",
                  placeItems: "center",
                  flexShrink: 0,
                  borderRadius: "50%",
                  color: "#A5A6AF",
                  background: "linear-gradient(90deg, #E9E9E9 47%, #F8F8F8 47%)",
                  fontSize: 16,
                  fontWeight: 700,
                }}
              >
                {user.name.slice(0, 1).toUpperCase()}
              </span>
              <ChevronDown size={15} />
            </button>
            {profileOpen ? (
              <div
                className="hr-header-profile-menu"
                role="menu"
                style={{
                  position: "absolute",
                  top: 51,
                  right: -2,
                  width: 150,
                  padding: 8,
                  borderRadius: 8,
                  background: "#FFF",
                  boxShadow: "0 2px 8px rgb(18 20 24 / 18%)",
                  zIndex: 1000,
                }}
              >
                <button
                  type="button"
                  role="menuitem"
                  onClick={() => void logoutUser()}
                  style={{
                    width: "100%",
                    padding: "10px 12px",
                    border: 0,
                    borderRadius: 6,
                    color: "#202129",
                    background: "transparent",
                    textAlign: "left",
                    cursor: "pointer",
                    fontFamily: "var(--hr-font-satoshi)",
                    fontSize: 14,
                  }}
                >
                  Log Out
                </button>
              </div>
            ) : null}
          </div>
        )}
      </div>
      {authMode !== null ? (
        <AuthDialog initialMode={authMode} onClose={() => setAuthMode(null)} />
      ) : null}
    </header>
  );
}
