"use client";

import { useEffect, useRef, useState } from "react";
import {
  Bell,
  ChevronDown,
  Menu,
  Moon,
  Search,
} from "lucide-react";
import { BrandMark } from "../shared/BrandMark";
import styles from "./landing.module.css";
import { AuthDialog, type AuthMode } from "../../../www.hackerrank.com-407abdb8/dashboard-89347bb2/AuthDialog";
import { AUTH_CHANGE_EVENT, getAuthUser, hydrateAuthUser, logoutUser, type AuthUser } from "@/lib/auth";

type HeaderOverlay = "notifications" | "profile" | null;

export function AppHeader() {
  const [overlay, setOverlay] = useState<HeaderOverlay>(null);
  const [authMode, setAuthMode] = useState<AuthMode | null>(null);
  const [user, setUser] = useState<AuthUser | null>(null);
  const headerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    function onPointerDown(event: PointerEvent) {
      if (!headerRef.current?.contains(event.target as Node)) {
        setOverlay(null);
      }
    }

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setOverlay(null);
      }
    }

    document.addEventListener("pointerdown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, []);

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

  function toggleOverlay(next: Exclude<HeaderOverlay, null>) {
    setOverlay((current) => (current === next ? null : next));
  }

  return (
    <header className={styles.header} ref={headerRef}>
      <div className={styles.desktopIdentity}>
        <BrandMark />
        <span className={styles.logoDivider} aria-hidden="true" />
        <nav className={styles.primaryNav} aria-label="Primary navigation">
          <button className={styles.activeNav} type="button">Prepare</button>
        </nav>
      </div>

      <div className={styles.mobileIdentity}>
        <button className={styles.headerIcon} aria-label="Open navigation" type="button">
          <Menu size={21} />
        </button>
        <BrandMark compact />
      </div>

      <div className={styles.headerActions}>
        <label className={styles.searchField}>
          <Search size={20} aria-hidden="true" />
          <input aria-label="Search" placeholder="Search" type="search" />
        </label>

        <div className={styles.headerControl}>
          <button
            className={styles.headerIcon}
            data-active={overlay === "notifications" || undefined}
            onClick={() => toggleOverlay("notifications")}
            aria-expanded={overlay === "notifications"}
            aria-label="Notifications"
            type="button"
          >
            <Bell size={19} />
          </button>
          {overlay === "notifications" ? <NotificationsOverlay /> : null}
        </div>

        <button className={styles.headerIcon} aria-label="Theme" type="button">
          <Moon size={20} />
        </button>

        {user === null ? (
          <>
            <button className={styles.authLoginButton} onClick={() => setAuthMode("login")} type="button">Log In</button>
            <button className={styles.authSignupButton} onClick={() => setAuthMode("signup")} type="button">Sign Up</button>
          </>
        ) : (
          <div className={styles.headerControl}>
            <button
              className={styles.profileButton}
              data-active={overlay === "profile" || undefined}
              onClick={() => toggleOverlay("profile")}
              aria-expanded={overlay === "profile"}
              aria-label="Profile menu"
              type="button"
            >
              <span className={styles.avatar} aria-hidden="true">{user.name.slice(0, 1).toUpperCase()}</span>
              <ChevronDown size={15} />
            </button>
            {overlay === "profile" ? <ProfileOverlay onLogout={() => void logoutUser()} /> : null}
          </div>
        )}
      </div>
      {authMode !== null ? <AuthDialog initialMode={authMode} onClose={() => setAuthMode(null)} /> : null}
    </header>
  );
}

function NotificationsOverlay() {
  return (
    <section className={`${styles.headerOverlay} ${styles.notificationsOverlay}`} aria-label="Notifications panel">
      <div className={styles.overlayHeading}>
        <strong>Notifications</strong>
        <button type="button">Show All</button>
      </div>
      <div className={styles.notificationItem}>
        <p>Get interview ready for top companies.</p>
        <small>1 hour ago</small>
      </div>
      <div className={styles.notificationItem}>
        <p>Improve your coding skills. Join our 30<br />Days of Code challenge!</p>
        <small>1 hour ago</small>
      </div>
    </section>
  );
}

function ProfileOverlay({ onLogout }: { onLogout: () => void }) {
  return (
    <section className={`${styles.headerOverlay} ${styles.profileOverlay}`} aria-label="Profile panel">
      <button onClick={onLogout} type="button">Log Out</button>
    </section>
  );
}
