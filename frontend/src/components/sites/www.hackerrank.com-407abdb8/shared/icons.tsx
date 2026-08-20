interface IconProps {
  className?: string;
  size?: number | string;
}

function baseSvgProps(size: number | string) {
  return {
    xmlns: "http://www.w3.org/2000/svg",
    width: typeof size === "number" ? size : "1em",
    height: typeof size === "number" ? size : "1em",
    viewBox: "0 0 24 24",
    fill: "none",
    className: "hr-icon",
  };
}

export function SearchIcon({ size = "1em", className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"}>
      <g
        fill="none"
        fillRule="evenodd"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
        transform="translate(2 2)"
      >
        <circle cx="9.767" cy="9.767" r="8.989" />
        <path d="M16.018 16.485 19.542 20" stroke="currentColor" />
      </g>
    </svg>
  );
}

export function ClockIcon({ size = "1em", className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"}>
      <g
        fill="none"
        fillRule="evenodd"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
      >
        <path d="M21.25 12A9.25 9.25 0 0 1 12 21.25 9.25 9.25 0 0 1 2.75 12 9.25 9.25 0 0 1 12 2.75 9.25 9.25 0 0 1 21.25 12Z" stroke="currentColor" />
        <path d="m15.431 14.943-3.77-2.25V7.848" stroke="currentColor" />
      </g>
    </svg>
  );
}

export function LockIcon({ size = "1em", className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"}>
      <g
        fill="none"
        fillRule="evenodd"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
      >
        <path
          d="M16.423 9.448V7.3a4.552 4.552 0 0 0-4.55-4.551 4.55 4.55 0 0 0-4.57 4.53v2.168"
          stroke="currentColor"
        />
        <path
          d="M15.683 21.25h-7.64a3.792 3.792 0 0 1-3.793-3.792v-4.29a3.792 3.792 0 0 1 3.792-3.791h7.641a3.792 3.792 0 0 1 3.792 3.792v4.289a3.792 3.792 0 0 1-3.792 3.792Z"
          stroke="currentColor"
        />
      </g>
    </svg>
  );
}

export function UnlockIcon({ size = "1em", className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"}>
      <g
        fill="none"
        fillRule="evenodd"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
      >
        <path
          d="M7.303 9.447v-2.168a4.55 4.55 0 0 1 4.57-4.53 4.552 4.552 0 0 1 4.55 4.551"
          stroke="currentColor"
        />
        <path
          d="M15.683 21.25h-7.64a3.792 3.792 0 0 1-3.793-3.792v-4.29a3.792 3.792 0 0 1 3.792-3.791h7.641a3.792 3.792 0 0 1 3.792 3.792v4.289a3.792 3.792 0 0 1-3.792 3.792Z"
          stroke="currentColor"
        />
      </g>
    </svg>
  );
}

export function ChevronLeftIcon({ size = 20, className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"} aria-hidden="true">
      <path
        fill="none"
        fillRule="evenodd"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
        d="m15.5 19-7-7 7-7"
      />
    </svg>
  );
}

export function ChevronRightIcon({ size = 20, className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"} aria-hidden="true">
      <path
        fill="none"
        fillRule="evenodd"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
        d="m8.5 5 7 7-7 7"
      />
    </svg>
  );
}

export function MenuIcon({ size = "1em", className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"}>
      <path
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
        d="M4 19h16M4 5h16M4 12h16"
      />
    </svg>
  );
}

export function CloseIcon({ size = "1em", className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"} aria-hidden="true">
      <path
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
        d="m6 6 12 12M18 6 6 18"
      />
    </svg>
  );
}

export function CheckIcon({ size = "1em", className }: IconProps) {
  return (
    <svg {...baseSvgProps(size)} className={className ? `hr-icon ${className}` : "hr-icon"} aria-hidden="true">
      <path
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
        d="m19 7.188-9.625 9.625L5 12.438"
      />
    </svg>
  );
}

