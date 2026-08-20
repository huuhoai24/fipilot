const ITEMS = ["FAQ", "About Us", "Terms Of Service", "Privacy Policy"];

export function Footer() {
  return (
    <footer
      className="hr-footer mt-auto mb-2 mx-auto max-[768px]:mb-0 max-[768px]:mx-0"
      style={{
        maxWidth: "100%",
        background: "transparent",
        padding: "6px 12px",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "center",
        gap: 12,
      }}
    >
      {ITEMS.map((label) => (
        <span
          key={label}
          style={{
            fontSize: 11,
            fontWeight: 400,
            lineHeight: "14px",
            color: "#8C96A5",
            fontFamily: "var(--hr-font-satoshi)",
            cursor: "pointer",
          }}
        >
          {label}
        </span>
      ))}
    </footer>
  );
}
