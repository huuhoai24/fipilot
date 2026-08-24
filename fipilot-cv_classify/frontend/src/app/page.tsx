import { Header } from "@/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/Header";
import { MockInterviewsSection } from "@/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/MockInterviewsSection";
import { Footer } from "@/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/Footer";
import { InterviewHistory } from "@/components/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/InterviewHistory";

export default function Home() {
  return (
    <main style={{ minHeight: "100vh", background: "#FFF", fontFamily: "var(--hr-font-satoshi)", display: "flex", flexDirection: "column" }}>
      <Header />
      <div className="hr-container" style={{ flex: 1 }}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 64,
            margin: "48px 0",
          }}
        >
          <MockInterviewsSection />
          <InterviewHistory />
        </div>
      </div>
      <Footer />
    </main>
  );
}
