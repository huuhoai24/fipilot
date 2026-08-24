import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "D:\\OJT_F_Software\\ojt\\Mapping\\data_cv\\fix-ai\\fipilot\\output\\presentations\\FiPilot_Technical_Slides_With_Knowledge_Matrix.pptx";
const BUILD = "D:\\OJT_F_Software\\ojt\\Mapping\\data_cv\\fix-ai\\fipilot\\tmp\\presentations\\fipilot_technical_revision";
const RENDER = `${BUILD}\\renders_v4`;
const LAYOUT = `${BUILD}\\layouts_v4`;

const W = 1280;
const H = 720;
const BG = "#F7F9FC";
const WHITE = "#FFFFFF";
const NAVY = "#173F7A";
const BLUE = "#4B70B5";
const BLUE2 = "#2F66C5";
const PALE = "#EAF1FC";
const PALE2 = "#DCE8FA";
const LINE = "#C8D8F0";
const TEXT = "#182235";
const MUTED = "#66748A";
const GREEN = "#17824F";
const GREEN_PALE = "#E7F5ED";
const PURPLE = "#5F36B3";
const PURPLE_PALE = "#F0EAFE";
const ORANGE = "#E96324";
const ORANGE_PALE = "#FFF0E8";
const RED = "#B64242";

const presentation = Presentation.create({ slideSize: { width: W, height: H } });

const NOTE_GUIDES = [
  {
    type: "SLIDE BÌA MỚI - DÙNG CHO DECK KỸ THUẬT ĐỘC LẬP",
    position: "Không cần chèn khi ghép vào deck cũ; bỏ slide này nếu chỉ thay/bổ sung các slide kỹ thuật.",
    action: "Dùng làm bìa khi gửi riêng phần Technical Architecture and Evaluation cho giảng viên hoặc nhóm review.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 3 - Table of Contents trong deck cũ.",
    action: "Đổi mục 03 thành Data & Knowledge Pipeline và mục 05 thành Evaluation Methodology & Results.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 8 - Project Scope & Out of Scope trong deck cũ.",
    action: "Giữ bố cục hai cột; sửa câu tiếng Anh, bổ sung giới hạn expert-human validation và warning về automated references.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 10 - System Architecture trong deck cũ.",
    action: "Thay ô Embeddings + Vector DB bằng Production: Lexical Top-8 / Research Shadow: Vector-Hybrid và thêm quyết định production.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 11 - Deployment Architecture & Trust Boundaries trong deck cũ.",
    action: "Đổi production-verified thành validated/deployed path; giữ trust boundary và chỉ dùng verified cho thuộc tính bảo mật có bằng chứng.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 12 - Multi-Agent & Orchestration Architecture trong deck cũ.",
    action: "Giữ sơ đồ agent; bổ sung retrieval adapter và ghi rõ production lexical, research vector/hybrid.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 15 - Resume-to-CandidateProfile Method trong deck cũ.",
    action: "Bổ sung OCR fallback, giới hạn 20 trang, context 16K, source verification và claim boundary cho kết quả 6/6 OCR.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn sau slide 15 - Resume-to-CandidateProfile Method và trước slide 16 - RAG Knowledge Retrieval Pipeline trong deck cũ. Trong deck kỹ thuật này, slide nằm ngay sau Resume Parsing.",
    action: "Dùng slide để giải thích Knowledge Matrix theo hai trục role × competency level, cấu trúc topic record và cách CandidateProfile chọn knowledge context.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 16 - RAG Knowledge Retrieval Pipeline trong deck cũ.",
    action: "Sửa corpus count; tách ba phần Knowledge Corpus, Production Path và Research Shadow; không mô tả vector như production.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 18 - Integrated AI Modules trong deck cũ.",
    action: "Giữ model routing cũ, bổ sung gemini-embedding-001 768D và nhãn shadow-only.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 19 - Question Generation Methodology trong deck cũ.",
    action: "Thay tuyên bố schema ngăn hallucination bằng ba lớp Grounding, Structural Validation và Adaptive Continuity.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 21 - Answer Evaluation & Adaptive Decision trong deck cũ.",
    action: "Đổi Rubric + RAG thành Rubric + Retrieved Evidence và nêu rõ MAE/Spearman dùng automated references.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn ngay sau slide 22 - Evaluation & Results divider. Sau khi thêm Knowledge Matrix, đây là slide 24 trong deck ghép hoàn chỉnh.",
    action: "Mở phần đánh giá bằng phương pháp M1-M7, trả lời rõ nhóm không fine-tune foundation model và định nghĩa bốn loại bằng chứng.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn sau slide Evaluation Protocol; khi ghép hoàn chỉnh, đây là slide 25.",
    action: "Trình bày kết quả M1-M2 cho resume extraction và thay bộ số 235 CVs trên slide evaluation cũ.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn sau slide Resume Extraction Results; khi ghép hoàn chỉnh, đây là slide 26.",
    action: "Giải thích chunk policy, token preservation, incremental update và rủi ro duplicate/tiny chunks của M3.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn sau slide Knowledge Base Construction; khi ghép hoàn chỉnh, đây là slide 27.",
    action: "Giải thích vector record, 768D embedding, Firestore collection, query inputs và cosine similarity của M4.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn sau slide Vector Storage & Similarity Search; khi ghép hoàn chỉnh, đây là slide 28.",
    action: "So sánh lexical/vector/hybrid bằng MRR, Hit@5 và latency; kết thúc bằng quyết định giữ lexical Top-8.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn sau slide Retrieval Benchmark; khi ghép hoàn chỉnh, đây là slide 29.",
    action: "Trình bày ảnh hưởng của RAG lên grounding câu hỏi, đồng thời giữ ranh giới no clear downstream-quality advantage.",
  },
  {
    type: "SLIDE MỚI - BỔ SUNG",
    position: "Chèn sau slide RAG Question Quality; khi ghép hoàn chỉnh, đây là slide 30, ngay trước Demo.",
    action: "Thay consistency 85.34% bằng bộ metric M7 và kết luận Production score trust: LOW.",
  },
  {
    type: "SLIDE CŨ - THAY TRỰC TIẾP",
    position: "Thay slide 26 - Contributions & Future Work trong deck cũ; sau khi thêm Knowledge Matrix và bảy slide đánh giá, slide này trở thành slide 33.",
    action: "Chuyển Hit@K/MRR từ Future Work sang Contributions; cập nhật future work thành human benchmark, dedup, filtering, reranking và production sync.",
  },
];
let noteGuideIndex = 0;

function addText(slide, text, left, top, width, height, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontFamily: "Arial",
    fontSize: opts.fontSize ?? 20,
    bold: opts.bold ?? false,
    color: opts.color ?? TEXT,
    alignment: opts.alignment ?? "left",
    italic: opts.italic ?? false,
  };
  return shape;
}

function addRect(slide, left, top, width, height, opts = {}) {
  return slide.shapes.add({
    geometry: opts.geometry ?? "rect",
    position: { left, top, width, height },
    fill: opts.fill ?? WHITE,
    line: { style: "solid", fill: opts.line ?? LINE, width: opts.lineWidth ?? 1 },
    ...(opts.geometry === "roundRect" ? { borderRadius: "rounded-xl" } : {}),
  });
}

function addRule(slide, left, top, width, height = 2, fill = LINE) {
  return addRect(slide, left, top, width, height, { fill, line: fill, lineWidth: 0 });
}

function addArrow(slide, left, top, width = 32, height = 18, fill = BLUE2) {
  return slide.shapes.add({
    geometry: "rightArrow",
    position: { left, top, width, height },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function addDownArrow(slide, left, top, width = 18, height = 24, fill = BLUE2) {
  return slide.shapes.add({
    geometry: "downArrow",
    position: { left, top, width, height },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function addCircleLabel(slide, text, left, top, size = 42, fill = NAVY) {
  addRect(slide, left, top, size, size, { geometry: "ellipse", fill, line: fill, lineWidth: 0 });
  addText(slide, text, left, top + 6, size, size - 8, { fontSize: 17, bold: true, color: WHITE, alignment: "center" });
}

function addHeader(slide, section, title, subtitle, page) {
  slide.background.fill = BG;
  addText(slide, section.toUpperCase(), 56, 30, 360, 24, { fontSize: 14, bold: true, color: BLUE });
  addText(slide, title, 56, 58, 1080, 52, { fontSize: 34, bold: true, color: NAVY });
  if (subtitle) addText(slide, subtitle, 58, 112, 1090, 32, { fontSize: 18, color: MUTED });
  addRect(slide, 1174, 28, 38, 38, { fill: PALE2, line: PALE2, lineWidth: 0 });
  addRect(slide, 1219, 28, 38, 38, { fill: "#91B1EB", line: "#91B1EB", lineWidth: 0 });
  addRule(slide, 56, subtitle ? 151 : 122, 1200, 2, LINE);
  addText(slide, `FIPILOT TECHNICAL REVISION  |  ${String(page).padStart(2, "0")}`, 56, 688, 420, 18, { fontSize: 11, bold: true, color: MUTED });
}

function addSourceFooter(slide, text) {
  addText(slide, text, 650, 687, 606, 18, { fontSize: 10, color: MUTED, alignment: "right" });
}

function addNotes(slide, lines, sources) {
  const guide = NOTE_GUIDES[noteGuideIndex++];
  slide.speakerNotes.textFrame.setText([
    "[VỊ TRÍ VÀ HƯỚNG DẪN CHỈNH SỬA]",
    `Loại: ${guide.type}`,
    `Vị trí: ${guide.position}`,
    `Cách thực hiện: ${guide.action}`,
    "",
    "[SPEAKER NOTES NHANH]",
    ...lines,
    "",
    "[Sources]",
    ...sources.map((s) => `- ${s}`),
  ]);
  slide.speakerNotes.setVisible(true);
}

function addBulletList(slide, items, left, top, width, opts = {}) {
  const gap = opts.gap ?? 48;
  items.forEach((item, i) => {
    addCircleLabel(slide, String(i + 1), left, top + i * gap, 28, opts.circleFill ?? NAVY);
    addText(slide, item, left + 42, top + i * gap - 2, width - 42, 38, { fontSize: opts.fontSize ?? 18, color: opts.color ?? TEXT, bold: opts.bold ?? false });
  });
}

function addMetric(slide, value, label, left, top, width, color = NAVY) {
  addText(slide, value, left, top, width, 58, { fontSize: 38, bold: true, color, alignment: "center" });
  addText(slide, label, left, top + 55, width, 46, { fontSize: 16, color: MUTED, alignment: "center" });
}

function addSimpleTable(slide, values, left, top, widths, rowHeight, opts = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  values.forEach((row, r) => {
    let x = left;
    row.forEach((cell, c) => {
      const isHeader = r === 0;
      const fill = isHeader ? (opts.headerFill ?? NAVY) : (r % 2 === 0 ? (opts.bandFill ?? PALE) : WHITE);
      addRect(slide, x, top + r * rowHeight, widths[c], rowHeight, { fill, line: LINE, lineWidth: 1 });
      addText(slide, String(cell), x + 10, top + r * rowHeight + 9, widths[c] - 20, rowHeight - 12, {
        fontSize: isHeader ? 15 : 16,
        bold: isHeader || c === 0,
        color: isHeader ? WHITE : TEXT,
        alignment: c === 0 ? "left" : "center",
      });
      x += widths[c];
    });
  });
  return total;
}

// Slide 1
{
  const slide = presentation.slides.add();
  slide.background.fill = BG;
  addText(slide, "FPT UNIVERSITY", 64, 42, 260, 30, { fontSize: 18, bold: true, color: ORANGE });
  addRect(slide, 1174, 34, 38, 38, { fill: PALE2, line: PALE2, lineWidth: 0 });
  addRect(slide, 1219, 34, 38, 38, { fill: "#91B1EB", line: "#91B1EB", lineWidth: 0 });
  addText(slide, "FIPILOT", 86, 170, 520, 88, { fontSize: 60, bold: true, color: NAVY });
  addText(slide, "Technical Architecture and Evaluation", 90, 258, 760, 70, { fontSize: 38, bold: true, color: BLUE });
  addText(slide, "Revised defense slides - M1 to M7", 92, 342, 620, 36, { fontSize: 23, color: MUTED });
  addRect(slide, 90, 442, 1080, 108, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  addText(slide, "Production path, research shadow and evidence boundaries", 130, 471, 1000, 48, { fontSize: 26, bold: true, color: WHITE, alignment: "center" });
  addText(slide, "FiPilot Team", 92, 635, 260, 28, { fontSize: 16, bold: true, color: NAVY });
  addText(slide, "Technical revision deck", 916, 635, 254, 28, { fontSize: 16, color: NAVY, alignment: "right" });
  addNotes(slide,
    [
      "Đây là deck kỹ thuật dùng để thay các slide cần chỉnh sửa trong bản cũ.",
      "Nhấn mạnh ngay từ đầu: production retrieval và các thử nghiệm vector/hybrid là hai phạm vi khác nhau.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md",
    ]);
}

// Slide 2
{
  const slide = presentation.slides.add();
  addHeader(slide, "01  Narrative", "Updated technical story", "The deck separates deployed behavior from measured research evidence.", 2);
  const items = [
    ["01", "Introduction", "Problem, scope and claim boundary"],
    ["02", "Architecture & System Design", "Production paths and trust boundaries"],
    ["03", "Data & Knowledge Pipeline", "Resume parsing, chunking and retrieval"],
    ["04", "AI Methodology", "Question generation and answer evaluation"],
    ["05", "Evaluation Methodology & Results", "M1 to M7 evidence and decisions"],
    ["06", "Conclusion", "Contributions, limitations and next work"],
  ];
  items.forEach((it, i) => {
    const y = 180 + i * 78;
    addText(slide, it[0], 76, y, 58, 34, { fontSize: 24, bold: true, color: i === 4 ? PURPLE : BLUE });
    addText(slide, it[1], 154, y, 450, 32, { fontSize: 22, bold: true, color: NAVY });
    addText(slide, it[2], 638, y + 2, 540, 30, { fontSize: 17, color: MUTED });
    if (i < items.length - 1) addRule(slide, 154, y + 54, 1030, 1, LINE);
  });
  addNotes(slide,
    [
      "Thay slide mục lục cũ để thống nhất tên mục Data & Knowledge Pipeline.",
      "Evaluation Methodology & Results được mở rộng thành một phần độc lập thay vì chỉ một slide số liệu.",
    ],
    ["D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 3"]);
}

// Slide 3
{
  const slide = presentation.slides.add();
  addHeader(slide, "01  Introduction", "Scope stays ambitious, but claims stay bounded", "FiPilot is an interview training system - not an automated hiring authority.", 3);
  addText(slide, "IN SCOPE", 86, 184, 440, 34, { fontSize: 24, bold: true, color: NAVY });
  addText(slide, "OUT OF SCOPE", 700, 184, 440, 34, { fontSize: 24, bold: true, color: NAVY });
  addRule(slide, 86, 225, 460, 4, BLUE2);
  addRule(slide, 700, 225, 460, 4, ORANGE);
  addBulletList(slide, [
    "Parse PDF/DOCX resumes into a structured CandidateProfile.",
    "Support text and voice practice for 10 IT roles and 4 levels.",
    "Provide evidence-backed feedback, reports and session history.",
  ], 88, 254, 500, { gap: 92, fontSize: 18, circleFill: BLUE2 });
  addBulletList(slide, [
    "ATS or final recruitment decision-making.",
    "Guaranteed human-level grading or production-wide accuracy.",
    "All languages, all domains or enterprise-scale SLA.",
    "Expert-human validation - not completed in M1 to M7.",
  ], 702, 254, 480, { gap: 72, fontSize: 18, circleFill: ORANGE });
  addRect(slide, 86, 591, 1074, 66, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "Reported evaluator metrics use automated references; they are not expert-human ground truth.", 118, 610, 1010, 30, { fontSize: 19, bold: true, color: RED, alignment: "center" });
  addNotes(slide,
    [
      "Sửa lỗi ngữ pháp của slide scope cũ và bổ sung ranh giới đánh giá.",
      "Không dùng các cụm human-level, expert-validated hoặc production accuracy khi trình bày kết quả M1-M7.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 8",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, evidence taxonomy and M7 claim boundary",
    ]);
}

// Slide 4
{
  const slide = presentation.slides.add();
  addHeader(slide, "02  Architecture", "Production retrieval is lexical; vector remains a research shadow", "The application pipeline stays unchanged while retrieval experiments run behind a clear boundary.", 4);
  const y = 210;
  const boxes = [
    { x: 72, w: 220, title: "Candidate actions", body: "Sign in\nUpload CV\nChoose mode\nStart session", fill: PALE, color: BLUE2 },
    { x: 332, w: 164, title: "Auth & API", body: "Firebase token\nFastAPI boundary", fill: WHITE, color: NAVY },
    { x: 536, w: 180, title: "CV processing", body: "Parse\nValidate\nCandidateProfile", fill: WHITE, color: NAVY },
    { x: 756, w: 200, title: "Knowledge retrieval", body: "Production: Lexical Top-8\nShadow: Vector / Hybrid", fill: PURPLE_PALE, color: PURPLE },
    { x: 996, w: 206, title: "Interview output", body: "Questions\nTranscript\nScore and report", fill: GREEN_PALE, color: GREEN },
  ];
  boxes.forEach((b, i) => {
    addRect(slide, b.x, y, b.w, 270, { geometry: "roundRect", fill: b.fill, line: i === 3 ? PURPLE : LINE, lineWidth: i === 3 ? 2 : 1 });
    addCircleLabel(slide, String(i + 1), b.x + b.w / 2 - 20, y + 24, 40, b.color);
    addText(slide, b.title, b.x + 16, y + 86, b.w - 32, 52, { fontSize: 20, bold: true, color: b.color, alignment: "center" });
    addText(slide, b.body, b.x + 18, y + 151, b.w - 36, 98, { fontSize: 17, color: TEXT, alignment: "center" });
    if (i < boxes.length - 1) addArrow(slide, b.x + b.w + 6, y + 126, 28, 18, BLUE2);
  });
  addRect(slide, 128, 523, 1022, 94, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  addText(slide, "Production decision", 158, 545, 230, 30, { fontSize: 19, bold: true, color: "#BBD2FF" });
  addText(slide, "Keep lexical Top-8 active until vector/hybrid meet compatibility, latency and quality gates.", 388, 542, 720, 42, { fontSize: 21, bold: true, color: WHITE });
  addNotes(slide,
    [
      "Thay ô Embeddings + Vector DB của slide kiến trúc cũ bằng hai trạng thái production và shadow.",
      "Khi hội đồng hỏi Vector DB có chạy production không, trả lời: đã đánh giá ở M4-M6 nhưng quyết định hiện tại vẫn giữ lexical Top-8.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 10",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M4-M6 production decision",
    ]);
}

// Slide 5
{
  const slide = presentation.slides.add();
  addHeader(slide, "02  Architecture", "Deployment paths share one authenticated ownership model", "Use validated or deployed - not production-verified - unless deployment logs are attached.", 5);
  addText(slide, "APPLICATION PATH", 76, 188, 270, 28, { fontSize: 18, bold: true, color: GREEN });
  addRule(slide, 76, 222, 812, 3, GREEN);
  const app = ["Frontend", "FastAPI", "Firestore", "Vertex AI / Gemini"];
  app.forEach((t, i) => {
    const x = 80 + i * 208;
    addRect(slide, x, 248, 170, 92, { geometry: "roundRect", fill: i === 2 ? GREEN_PALE : WHITE, line: i === 2 ? GREEN : LINE, lineWidth: 1 });
    addText(slide, t, x + 10, 277, 150, 32, { fontSize: 19, bold: true, color: i === 2 ? GREEN : NAVY, alignment: "center" });
    if (i < app.length - 1) addArrow(slide, x + 178, 285, 24, 16, GREEN);
  });
  addText(slide, "SPEECH PATH", 76, 382, 270, 28, { fontSize: 18, bold: true, color: BLUE2 });
  addRule(slide, 76, 416, 812, 3, BLUE2);
  const speech = ["Browser", "Voice WebSocket", "Speech service", "VAD / Whisper", "Shared engine"];
  speech.forEach((t, i) => {
    const x = 76 + i * 164;
    addRect(slide, x, 442, 136, 88, { geometry: "roundRect", fill: WHITE, line: LINE, lineWidth: 1 });
    addText(slide, t, x + 8, 467, 120, 38, { fontSize: 16, bold: true, color: NAVY, alignment: "center" });
    if (i < speech.length - 1) addArrow(slide, x + 140, 478, 20, 14, BLUE2);
  });
  addRect(slide, 930, 188, 274, 342, { geometry: "roundRect", fill: PALE, line: LINE, lineWidth: 1 });
  addText(slide, "TRUST BOUNDARY", 958, 216, 220, 32, { fontSize: 22, bold: true, color: NAVY, alignment: "center" });
  addBulletList(slide, [
    "Firebase ID token verified by FastAPI.",
    "Persistent resources scoped by Firebase UID.",
    "Text and voice use the same session ownership.",
    "WebSocket sessions are authenticated.",
  ], 956, 272, 226, { gap: 64, fontSize: 15, circleFill: GREEN });
  addRect(slide, 76, 568, 1128, 66, { geometry: "roundRect", fill: GREEN_PALE, line: "#A6D7BC", lineWidth: 1 });
  addText(slide, "Verified security property: authenticated resume -> interview -> report -> history", 110, 587, 1060, 30, { fontSize: 20, bold: true, color: GREEN, alignment: "center" });
  addNotes(slide,
    [
      "Đổi nhãn production-verified thành mô tả trung tính hơn vì master M1-M7 không phải bộ bằng chứng deployment.",
      "Phần trust boundary được giữ vì phù hợp kiến trúc xác thực và ownership hiện tại.",
    ],
    ["D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 11"]);
}

// Slide 6
{
  const slide = presentation.slides.add();
  addHeader(slide, "02  Architecture", "Agents are typed services coordinated by one stateful orchestrator", "Retrieval is an adapter input, not a claim that every agent uses a vector database.", 6);
  addRect(slide, 414, 292, 452, 126, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  addText(slide, "InterviewOrchestrator", 440, 320, 400, 38, { fontSize: 28, bold: true, color: WHITE, alignment: "center" });
  addText(slide, "shared state + adaptive loop", 444, 365, 390, 30, { fontSize: 18, italic: true, color: "#C8D8F8", alignment: "center" });
  const agents = [
    { x: 84, y: 192, t: "ResumeAgent", b: "CV -> CandidateProfile", c: BLUE2 },
    { x: 84, y: 452, t: "PlannerAgent", b: "Profile + retrieved knowledge -> plan", c: BLUE2 },
    { x: 508, y: 176, t: "QuestionAgent", b: "Plan round -> question", c: PURPLE },
    { x: 930, y: 192, t: "EvaluatorAgent", b: "Answer -> score + gaps", c: GREEN },
    { x: 930, y: 452, t: "ReportAgent", b: "Evidence -> coaching report", c: GREEN },
    { x: 482, y: 492, t: "Decision Service", b: "Probe / difficulty / next round", c: PURPLE },
  ];
  agents.forEach((a) => {
    addRect(slide, a.x, a.y, 266, 104, { geometry: "roundRect", fill: WHITE, line: a.c, lineWidth: 1 });
    addText(slide, a.t, a.x + 16, a.y + 18, 234, 30, { fontSize: 21, bold: true, color: a.c, alignment: "center" });
    addText(slide, a.b, a.x + 16, a.y + 55, 234, 38, { fontSize: 15, color: TEXT, alignment: "center" });
  });
  addArrow(slide, 360, 272, 46, 20, BLUE2);
  addArrow(slide, 360, 478, 46, 20, BLUE2);
  addArrow(slide, 616, 268, 46, 20, PURPLE);
  addArrow(slide, 874, 272, 46, 20, GREEN);
  addArrow(slide, 874, 478, 46, 20, GREEN);
  addArrow(slide, 616, 440, 46, 20, PURPLE);
  addRect(slide, 170, 620, 940, 42, { geometry: "roundRect", fill: PALE, line: LINE, lineWidth: 1 });
  addText(slide, "Production retrieval adapter: lexical Top-8 | Research adapters: vector and hybrid", 196, 630, 888, 24, { fontSize: 17, bold: true, color: NAVY, alignment: "center" });
  addNotes(slide,
    [
      "Giữ kiến trúc multi-agent cũ nhưng làm rõ retrieved context đi qua một adapter.",
      "Không nói PlannerAgent mặc định dùng vector DB; production adapter hiện là lexical Top-8.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 12",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M4-M5 retrieval decision",
    ]);
}

// Slide 7
{
  const slide = presentation.slides.add();
  addHeader(slide, "03  Data & Knowledge", "Resume parsing adds OCR fallback before structured extraction", "Images are not embedded as pictures; scanned text is recovered through OCR and verified against the source.", 7);
  const steps = [
    ["1", "Upload & validate", "PDF/DOCX\n<= 10 MB\n<= 20 pages"],
    ["2", "Native extraction", "PyMuPDF\npython-docx"],
    ["3", "OCR fallback", "RapidOCR / ONNX\nfor scanned pages"],
    ["4", "Context selection", "Normalize sections\n<= 16,000 chars"],
    ["5", "Structured extraction", "Gemini 2.5 Flash-Lite\ntyped JSON"],
    ["6", "Verify & persist", "Source checks\nPydantic\natomic replace"],
  ];
  steps.forEach((s, i) => {
    const x = 52 + i * 202;
    addRect(slide, x, 205, 170, 272, { geometry: "roundRect", fill: i === 2 ? ORANGE_PALE : (i === 5 ? GREEN_PALE : WHITE), line: i === 2 ? ORANGE : (i === 5 ? GREEN : LINE), lineWidth: 1 });
    addCircleLabel(slide, s[0], x + 64, 222, 42, i === 2 ? ORANGE : (i === 5 ? GREEN : BLUE2));
    addText(slide, s[1], x + 12, 286, 146, 55, { fontSize: 18, bold: true, color: NAVY, alignment: "center" });
    addText(slide, s[2], x + 14, 359, 142, 90, { fontSize: 15, color: TEXT, alignment: "center" });
    if (i < steps.length - 1) addArrow(slide, x + 174, 330, 24, 16, BLUE2);
  });
  addRect(slide, 96, 518, 1088, 92, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  addMetric(slide, "98.53%", "M2 micro-F1", 120, 527, 220, "#BBD2FF");
  addMetric(slide, "100%", "Experience F1", 376, 527, 220, "#BBD2FF");
  addMetric(slide, "6 / 6", "Controlled OCR scans", 632, 527, 220, "#BBD2FF");
  addText(slide, "Controlled evidence - not production-wide accuracy", 876, 548, 272, 42, { fontSize: 17, bold: true, color: WHITE, alignment: "center" });
  addNotes(slide,
    [
      "Thay pipeline cũ chỉ có pypdf/python-docx bằng pipeline M2 có OCR fallback và context selection.",
      "Nếu branch production chưa tích hợp RapidOCR và giới hạn 16K thì phải gọi đây là evaluated pipeline, không phải deployed pipeline.",
      "CV có ảnh: hệ thống không phân tích hình ảnh theo nghĩa thị giác; OCR chỉ khôi phục chữ từ trang scan.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 15",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M2",
    ]);
}

// Slide 8
{
  const slide = presentation.slides.add();
  addHeader(slide, "03  Data & Knowledge", "The knowledge matrix links role, level and topic evidence", "A versioned catalog converts curated Markdown into retrieval-ready topic records.", 8);

  // Matrix axes
  addRect(slide, 58, 182, 274, 350, { geometry: "roundRect", fill: PALE, line: BLUE2, lineWidth: 1 });
  addText(slide, "MATRIX AXES", 82, 202, 226, 26, { fontSize: 20, bold: true, color: BLUE2, alignment: "center" });
  addMetric(slide, "10", "IT roles / domains", 72, 244, 112, BLUE2);
  addText(slide, "×", 179, 270, 32, 32, { fontSize: 28, bold: true, color: MUTED, alignment: "center" });
  addMetric(slide, "4", "competency levels", 204, 244, 112, PURPLE);
  addRule(slide, 82, 350, 226, 2, LINE);
  addText(slide, "Intern  |  Junior  |  Middle  |  Senior", 76, 369, 238, 24, { fontSize: 14, bold: true, color: NAVY, alignment: "center" });
  addText(slide, "AI Engineer · Backend Developer\nBusiness Analyst · Data Engineer\nData Scientist · DevOps Engineer\nFull Stack · Software Engineer\nTester / QA / QC · Web Developer", 78, 410, 234, 104, { fontSize: 13, color: TEXT, alignment: "center" });

  // Knowledge hierarchy
  addRect(slide, 350, 182, 408, 350, { geometry: "roundRect", fill: WHITE, line: LINE, lineWidth: 1 });
  addText(slide, "KNOWLEDGE HIERARCHY", 378, 202, 352, 26, { fontSize: 20, bold: true, color: NAVY, alignment: "center" });
  const hierarchy = [
    ["ROLE / DOMAIN", BLUE2, PALE],
    ["CATEGORY", PURPLE, PURPLE_PALE],
    ["SUBCATEGORY", GREEN, GREEN_PALE],
    ["TOPIC", ORANGE, ORANGE_PALE],
  ];
  hierarchy.forEach((item, i) => {
    const y = 242 + i * 58;
    addRect(slide, 402, y, 304, 40, { geometry: "roundRect", fill: item[2], line: item[1], lineWidth: 1 });
    addText(slide, item[0], 418, y + 9, 272, 22, { fontSize: 16, bold: true, color: item[1], alignment: "center" });
    if (i < hierarchy.length - 1) addDownArrow(slide, 546, y + 41, 16, 17, item[1]);
  });
  addRect(slide, 382, 476, 344, 40, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  addText(slide, "topic_id = role :: path :: title", 392, 484, 324, 22, { fontSize: 15, bold: true, color: WHITE, alignment: "center" });

  // Runtime record
  addRect(slide, 776, 182, 446, 350, { geometry: "roundRect", fill: WHITE, line: LINE, lineWidth: 1 });
  addText(slide, "RETRIEVAL-READY RECORD", 804, 202, 390, 26, { fontSize: 20, bold: true, color: NAVY, alignment: "center" });
  const records = [
    ["TOPIC RECORD", "title · path · anchors", BLUE2, PALE],
    ["CONTENT", "Role + Topic + interview anchors", PURPLE, PURPLE_PALE],
    ["METADATA", "domain key · hashes · stable IDs", GREEN, GREEN_PALE],
    ["LEVEL GUIDANCE", "knowledge depth + evaluation focus", ORANGE, ORANGE_PALE],
  ];
  records.forEach((row, i) => {
    const y = 244 + i * 61;
    addRect(slide, 802, y, 394, 48, { geometry: "roundRect", fill: row[3], line: row[2], lineWidth: 1 });
    addText(slide, row[0], 818, y + 7, 144, 20, { fontSize: 14, bold: true, color: row[2] });
    addText(slide, row[1], 966, y + 7, 214, 32, { fontSize: 14, color: TEXT });
  });
  addText(slide, "document_id = SHA-256(topic_id) · content hash enables update checks", 802, 493, 394, 24, { fontSize: 13, bold: true, color: MUTED, alignment: "center" });

  // Runtime selection flow
  addRect(slide, 58, 552, 1164, 98, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  const flow = [
    ["CandidateProfile", "role · level · skills · evidence"],
    ["Select context", "domain + level guidance"],
    ["Score topics", "title · path · anchors"],
    ["Planner context", "production lexical Top-8"],
  ];
  flow.forEach((item, i) => {
    const x = 82 + i * 286;
    addText(slide, item[0], x, 568, 224, 24, { fontSize: 17, bold: true, color: "#CFE0FF", alignment: "center" });
    addText(slide, item[1], x, 598, 224, 32, { fontSize: 14, color: WHITE, alignment: "center" });
    if (i < flow.length - 1) addArrow(slide, x + 232, 590, 28, 16, "#BBD2FF");
  });
  addSourceFooter(slide, "Source: Knowledge/*; catalog.json; chunks.py; local.py.");
  addNotes(slide,
    [
      "Knowledge Matrix không phải là model được train; đây là knowledge catalog được curate và quản lý phiên bản.",
      "Hai trục chính là role/domain và competency level. Bên dưới mỗi role là cây Category → Subcategory → Topic.",
      "Mỗi topic được chuẩn hóa thành title, path, anchors, stable topic_id, document_id và content hash để retrieval, audit và cập nhật.",
      "Level guidance được lưu riêng theo Intern, Junior, Middle và Senior để điều chỉnh độ sâu kiến thức và tiêu chí đánh giá.",
      "CandidateProfile cung cấp role, level, skills, projects và evidence. Production chọn domain, gắn level guidance, chấm điểm topic và đưa tối đa Top-8 topic vào Planner.",
      "Trong vector shadow, chỉ normalized topic content được embedded; metadata vẫn giữ dạng có cấu trúc để filtering, traceability và incremental update.",
    ],
    [
      "Knowledge\\Domains\\<Role>\\<Category>\\<Subcategory>\\<Topic>.md",
      "Knowledge\\Levels\\<Role>\\<Intern|Junior|Middle|Senior>.md",
      "backend\\services\\interview_knowledge\\catalog.json",
      "backend\\services\\interview_knowledge\\chunks.py",
      "backend\\services\\interview_knowledge\\local.py",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M3-M5",
    ]);
}

// Slide 9
{
  const slide = presentation.slides.add();
  addHeader(slide, "03  Data & Knowledge", "One corpus supports two retrieval paths with different deployment status", "Chunk text is embedded; metadata is retained for filtering, updates and audit.", 9);
  const cols = [
    { x: 68, title: "KNOWLEDGE CORPUS", color: BLUE2, fill: PALE, lines: ["4,419 documents", "4,492 chunks", "10 IT domains", "4 competency levels"] },
    { x: 448, title: "PRODUCTION PATH", color: GREEN, fill: GREEN_PALE, lines: ["Lexical Top-8", "Role and level filters", "Skills and evidence", "Low-latency retrieval"] },
    { x: 828, title: "RESEARCH SHADOW", color: PURPLE, fill: PURPLE_PALE, lines: ["gemini-embedding-001", "768 dimensions", "Firestore cosine search", "Vector and hybrid"] },
  ];
  cols.forEach((c) => {
    addRect(slide, c.x, 192, 332, 306, { geometry: "roundRect", fill: c.fill, line: c.color, lineWidth: 1 });
    addText(slide, c.title, c.x + 18, 218, 296, 34, { fontSize: 20, bold: true, color: c.color, alignment: "center" });
    addRule(slide, c.x + 34, 267, 264, 3, c.color);
    c.lines.forEach((line, i) => {
      addCircleLabel(slide, String(i + 1), c.x + 32, 292 + i * 50, 26, c.color);
      addText(slide, line, c.x + 72, 291 + i * 50, 224, 32, { fontSize: 18, color: TEXT });
    });
  });
  addArrow(slide, 408, 333, 30, 18, BLUE2);
  addArrow(slide, 788, 333, 30, 18, BLUE2);
  addRect(slide, 94, 532, 1092, 84, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "Decision", 120, 552, 124, 28, { fontSize: 20, bold: true, color: ORANGE });
  addText(slide, "Do not activate vector/hybrid until compatibility, latency and quality gates are satisfied.", 252, 550, 894, 34, { fontSize: 20, bold: true, color: TEXT });
  addSourceFooter(slide, "Counts from M3 master - reconcile with the frozen repository snapshot before defense.");
  addNotes(slide,
    [
      "Sửa 4,379 topic entries thành 4,419 documents và 4,492 chunks theo master M3.",
      "Nêu rõ phần được embedded là nội dung chunk; metadata dùng để lọc và audit.",
      "Cần đối chiếu lại số document với branch dùng để bảo vệ vì repo hiện kiểm tra thấy 4,418 file Markdown.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 16",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M3-M5",
    ]);
}

// Slide 10
{
  const slide = presentation.slides.add();
  addHeader(slide, "04  AI Methodology", "Model routing follows task cost and quality needs", "The embedding model is part of the research shadow, not the production generation path.", 10);
  const rows = [
    ["Resume extraction", "Gemini 2.5 Flash-Lite", "Structured JSON at lower latency and cost"],
    ["Interview planning", "Gemini 2.5 Flash", "Topic coverage and difficulty design"],
    ["Question generation", "Gemini 2.5 Flash", "Interactive per-turn question generation"],
    ["Answer evaluation", "Gemini 2.5 Pro", "Rubric scoring, gaps and explanation"],
    ["Final report", "Gemini 2.5 Pro", "Session-level evidence synthesis"],
    ["Voice interview", "Flash + faster-whisper + VieNeu", "Streaming question, STT and Vietnamese TTS"],
    ["Embedding experiment", "gemini-embedding-001 - 768D", "Shadow-only vector retrieval"],
  ];
  addSimpleTable(slide, [["TASK", "MODEL / SERVICE", "ROLE"], ...rows], 70, 184, [300, 360, 480], 54, { headerFill: NAVY, bandFill: PALE });
  addNotes(slide,
    [
      "Giữ các model đã có trên slide cũ và bổ sung embedding model ở trạng thái shadow-only.",
      "Không dùng từ train model: nhóm không fine-tune mô hình riêng trong M1-M7.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 18",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, model snapshot",
    ]);
}

// Slide 11
{
  const slide = presentation.slides.add();
  addHeader(slide, "04  AI Methodology", "Question generation combines evidence, plan bounds and retrieval", "Typed schemas validate structure; they do not independently guarantee factual correctness.", 11);
  const flow = [
    ["CandidateProfile", "skills, projects, evidence"],
    ["Plan bounds", "topic and level"],
    ["Configuration", "language and role"],
    ["Gemini Flash", "typed JSON"],
    ["Interview question", "expected points and probes"],
  ];
  flow.forEach((f, i) => {
    const x = 72 + i * 238;
    addRect(slide, x, 220, 196, 170, { geometry: "roundRect", fill: i === 3 ? PURPLE_PALE : WHITE, line: i === 3 ? PURPLE : LINE, lineWidth: 1 });
    addCircleLabel(slide, String(i + 1), x + 77, 238, 42, i === 3 ? PURPLE : BLUE2);
    addText(slide, f[0], x + 12, 301, 172, 34, { fontSize: 19, bold: true, color: NAVY, alignment: "center" });
    addText(slide, f[1], x + 16, 345, 164, 34, { fontSize: 15, color: MUTED, alignment: "center" });
    if (i < flow.length - 1) addArrow(slide, x + 199, 292, 30, 18, BLUE2);
  });
  const principles = [
    ["GROUNDING", "Candidate evidence and role knowledge guide content and expected points.", GREEN],
    ["STRUCTURE", "Typed schemas enforce required fields and valid output shape.", BLUE2],
    ["CONTINUITY", "Previous turns and deterministic rules control probes and difficulty.", PURPLE],
  ];
  principles.forEach((p, i) => {
    const x = 90 + i * 382;
    addText(slide, p[0], x, 448, 340, 28, { fontSize: 18, bold: true, color: p[2], alignment: "center" });
    addRule(slide, x + 72, 482, 196, 3, p[2]);
    addText(slide, p[1], x + 12, 500, 316, 70, { fontSize: 16, color: TEXT, alignment: "center" });
  });
  addRect(slide, 100, 604, 1080, 52, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "Schema validity is not the same as factual grounding or hallucination prevention.", 126, 619, 1028, 26, { fontSize: 18, bold: true, color: RED, alignment: "center" });
  addNotes(slide,
    [
      "Sửa câu typed schema guards against hallucinations thành ranh giới chính xác hơn.",
      "Schema chỉ bảo đảm cấu trúc. Grounding phải được đo bằng nguồn tri thức và benchmark M6.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 19",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M6",
    ]);
}

// Slide 12
{
  const slide = presentation.slides.add();
  addHeader(slide, "04  AI Methodology", "The evaluator scores content; deterministic rules control the next state", "Reported score quality is measured against automated references, not human ground truth.", 12);
  const flow = [
    ["Answer", "candidate text"],
    ["Rubric + evidence", "expected points\nprofile evidence\nproduction lexical context"],
    ["Evaluator service", "0-10 score\nevidence + feedback"],
    ["Decision service", "probe / difficulty\nfinish condition"],
    ["Next state", "probe / next round\nfinish"],
  ];
  flow.forEach((f, i) => {
    const x = 68 + i * 240;
    addRect(slide, x, 220, 198, 206, { geometry: "roundRect", fill: i === 3 ? GREEN_PALE : (i === 1 ? PALE : WHITE), line: i === 3 ? GREEN : LINE, lineWidth: 1 });
    addCircleLabel(slide, String(i + 1), x + 78, 240, 42, i === 3 ? GREEN : BLUE2);
    addText(slide, f[0], x + 12, 302, 174, 34, { fontSize: 19, bold: true, color: NAVY, alignment: "center" });
    addText(slide, f[1], x + 14, 344, 170, 62, { fontSize: 15, color: MUTED, alignment: "center" });
    if (i < flow.length - 1) addArrow(slide, x + 202, 306, 28, 18, BLUE2);
  });
  addRect(slide, 90, 478, 1096, 130, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "EVALUATION BOUNDARY", 118, 504, 252, 30, { fontSize: 21, bold: true, color: ORANGE });
  addText(slide, "MAE and Spearman correlation are computed against automated references. Production score trust remains LOW until an expert-human benchmark is completed.", 382, 497, 770, 76, { fontSize: 20, bold: true, color: TEXT });
  addNotes(slide,
    [
      "Thay Rubric + RAG bằng Rubric + evidence và ghi rõ production lexical context.",
      "Nếu hội đồng hỏi độ chính xác, dùng Spearman/MAE với automated reference; không gọi đây là human grading accuracy.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 21",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M7",
    ]);
}

// Slide 13
{
  const slide = presentation.slides.add();
  addHeader(slide, "05  Evaluation", "M1 to M7 optimize the system - not a newly trained foundation model", "Every result is tied to an evidence type and a claim boundary.", 13);
  addRect(slide, 72, 190, 460, 360, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  addText(slide, "NO CUSTOM MODEL\nFINE-TUNING", 108, 248, 388, 94, { fontSize: 34, bold: true, color: WHITE, alignment: "center" });
  addText(slide, "The team evaluates parsing, prompts, chunking, retrieval configurations and decision rules.", 116, 372, 372, 92, { fontSize: 20, color: "#D8E5FF", alignment: "center" });
  addText(slide, "EVIDENCE TYPES", 596, 190, 380, 34, { fontSize: 23, bold: true, color: NAVY });
  const evidence = [
    ["Synthetic-controlled", "Known expected fields and controlled difficulty"],
    ["Deterministic audit", "Counts, hashes, preservation and parity"],
    ["LLM-as-judge", "Question validity and grounding review"],
    ["Automated reference", "Evaluator ordering and calibration"],
  ];
  evidence.forEach((e, i) => {
    const y = 244 + i * 76;
    addCircleLabel(slide, String(i + 1), 598, y, 34, [BLUE2, GREEN, PURPLE, ORANGE][i]);
    addText(slide, e[0], 650, y - 2, 244, 28, { fontSize: 19, bold: true, color: NAVY });
    addText(slide, e[1], 906, y - 2, 286, 42, { fontSize: 15, color: MUTED });
    if (i < evidence.length - 1) addRule(slide, 650, y + 54, 542, 1, LINE);
  });
  addRect(slide, 72, 584, 1120, 64, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "Do not present controlled results as human-level, expert-validated or production-wide accuracy.", 104, 603, 1056, 30, { fontSize: 19, bold: true, color: RED, alignment: "center" });
  addNotes(slide,
    [
      "Slide mới trả lời trực tiếp câu hỏi nhóm train dữ liệu như thế nào.",
      "Câu trả lời: không fine-tune model; nhóm tối ưu pipeline và đánh giá cấu hình trên các bộ dữ liệu có kiểm soát.",
    ],
    ["D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, evaluation protocol and evidence taxonomy"]);
}

// Slide 14
{
  const slide = presentation.slides.add();
  addHeader(slide, "05  Evaluation", "M2 improves resume extraction, especially experience fields", "The benchmark uses 30 synthetic-controlled PDF/DOCX resumes.", 14);
  slide.charts.add("bar", {
    position: { left: 70, top: 195, width: 650, height: 340 },
    categories: ["Overall micro-F1", "Experience F1"],
    series: [
      { name: "M1 baseline", values: [94.78, 72.13], fill: "#A9BFE7", valuesFormatCode: "0.00" },
      { name: "M2", values: [98.53, 100], fill: BLUE2, valuesFormatCode: "0.00" },
    ],
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 70 },
    hasLegend: true,
    legend: { position: "bottom", overlay: false, textStyle: { fill: TEXT, fontSize: 13 } },
    yAxis: { min: 0, max: 100, majorUnit: 20, numberFormatCode: "0", majorGridlines: { style: "solid", fill: LINE, width: 1 }, textStyle: { fill: MUTED, fontSize: 12 } },
    xAxis: { textStyle: { fill: TEXT, fontSize: 13 } },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fill: NAVY, fontSize: 12, bold: true } },
    chartFill: WHITE,
    chartLine: { style: "solid", fill: LINE, width: 1 },
    plotAreaFill: WHITE,
  });
  addMetric(slide, "6 / 6", "Controlled OCR scans", 772, 222, 190, ORANGE);
  addMetric(slide, "3.742 s", "Mean latency", 982, 222, 190, GREEN);
  addMetric(slide, "14.716 s", "P95 latency", 772, 355, 190, PURPLE);
  addMetric(slide, "98.53%", "M2 micro-F1", 982, 355, 190, BLUE2);
  addRect(slide, 760, 502, 424, 86, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "6/6 OCR success is encouraging, but the sample is too small for a broad accuracy claim.", 788, 520, 368, 54, { fontSize: 17, bold: true, color: RED, alignment: "center" });
  addSourceFooter(slide, "Source: M1-M2 controlled evaluation.");
  addNotes(slide,
    [
      "Slide mới thay phần Resume Extraction 235 CVs của slide cũ bằng benchmark M1-M2 có nguồn rõ ràng.",
      "Giải thích micro-F1 là tổng hợp precision/recall theo field, không phải tỷ lệ CV production được parse đúng hoàn toàn.",
    ],
    ["D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M1-M2"]);
}

// Slide 15
{
  const slide = presentation.slides.add();
  addHeader(slide, "05  Evaluation", "The knowledge base is versioned, measurable and incrementally updatable", "Preservation is complete, but corpus duplication and tiny chunks remain material risks.", 15);
  addText(slide, "CORPUS CONSTRUCTION", 76, 190, 360, 30, { fontSize: 21, bold: true, color: NAVY });
  addMetric(slide, "4,419", "documents", 76, 236, 160, BLUE2);
  addMetric(slide, "4,492", "chunks", 250, 236, 160, BLUE2);
  addMetric(slide, "100%", "approx. token preservation", 76, 356, 334, GREEN);
  addText(slide, "Chunk policy", 76, 470, 170, 26, { fontSize: 18, bold: true, color: NAVY });
  addText(slide, "Target 400 | Max 600 | Min 30 | Overlap 0", 76, 505, 370, 32, { fontSize: 17, color: TEXT });
  addText(slide, "INCREMENTAL UPDATE", 500, 190, 360, 30, { fontSize: 21, bold: true, color: NAVY });
  const update = ["Hash source", "Skip unchanged", "Re-chunk changed", "Re-embed / upsert", "Delete removed"];
  update.forEach((u, i) => {
    const x = 500 + i * 139;
    addCircleLabel(slide, String(i + 1), x + 35, 248, 42, i === 4 ? ORANGE : PURPLE);
    addText(slide, u, x, 306, 112, 48, { fontSize: 16, bold: true, color: NAVY, alignment: "center" });
    if (i < update.length - 1) addArrow(slide, x + 112, 260, 22, 14, PURPLE);
  });
  addRect(slide, 500, 390, 690, 170, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "QUALITY RISKS", 526, 414, 192, 28, { fontSize: 20, bold: true, color: ORANGE });
  addText(slide, "76.71%", 528, 464, 150, 48, { fontSize: 32, bold: true, color: RED });
  addText(slide, "tiny chunks", 528, 510, 150, 26, { fontSize: 16, color: MUTED });
  addText(slide, "34.13%", 744, 464, 150, 48, { fontSize: 32, bold: true, color: RED });
  addText(slide, "exact-duplicate members", 744, 510, 190, 26, { fontSize: 16, color: MUTED });
  addText(slide, "Use deduplication and group-based splitting before the next benchmark.", 950, 450, 212, 78, { fontSize: 17, bold: true, color: TEXT, alignment: "center" });
  addSourceFooter(slide, "Source: M3 deterministic audit.");
  addNotes(slide,
    [
      "Slide mới trả lời cách cắt chuỗi, lưu knowledge base và cập nhật dữ liệu.",
      "Cập nhật dựa trên source ID, version và content hash; file không đổi được skip, file đổi được re-chunk và re-embed.",
      "100% preservation chỉ là độ phủ token xấp xỉ, không có nghĩa chất lượng ngữ nghĩa đạt 100%.",
    ],
    ["D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M3"]);
}

// Slide 16
{
  const slide = presentation.slides.add();
  addHeader(slide, "05  Evaluation", "Vector search ranks embedded chunks by cosine similarity", "The search query is built from role, level, skills, projects, evidence and interview objective.", 16);
  addRect(slide, 70, 196, 460, 330, { geometry: "roundRect", fill: PURPLE_PALE, line: PURPLE, lineWidth: 1 });
  addText(slide, "COSINE SIMILARITY", 104, 225, 392, 32, { fontSize: 22, bold: true, color: PURPLE, alignment: "center" });
  addText(slide, "cos(q, d) =", 110, 311, 170, 42, { fontSize: 30, bold: true, color: NAVY, alignment: "right" });
  addText(slide, "q · d", 300, 285, 140, 38, { fontSize: 29, bold: true, color: NAVY, alignment: "center" });
  addRule(slide, 302, 332, 136, 3, NAVY);
  addText(slide, "||q|| ||d||", 282, 345, 176, 42, { fontSize: 25, bold: true, color: NAVY, alignment: "center" });
  addText(slide, "Rank eligible chunks from highest to lowest similarity, then return Top-k context.", 108, 414, 384, 72, { fontSize: 18, color: TEXT, alignment: "center" });
  addText(slide, "VECTOR RECORD", 590, 196, 260, 30, { fontSize: 21, bold: true, color: NAVY });
  addBulletList(slide, [
    "Stable chunk ID and source ID",
    "Normalized chunk text",
    "Domain, role, level and section metadata",
    "Source version and content hash",
    "768-dimensional embedding",
  ], 592, 242, 530, { gap: 54, fontSize: 17, circleFill: PURPLE });
  addRect(slide, 590, 535, 600, 78, { geometry: "roundRect", fill: PALE, line: LINE, lineWidth: 1 });
  addText(slide, "Storage", 616, 552, 100, 28, { fontSize: 18, bold: true, color: BLUE2 });
  addText(slide, "Firestore collection: fipilot_m4_knowledge_vectors", 726, 550, 436, 32, { fontSize: 18, bold: true, color: NAVY });
  addText(slide, "Research shadow - not the production retrieval path", 726, 582, 436, 22, { fontSize: 14, color: PURPLE });
  addSourceFooter(slide, "Source: M4 vector retrieval experiment.");
  addNotes(slide,
    [
      "Slide mới trả lời vector database lưu gì và tính độ tương đồng như thế nào.",
      "Chỉ text chunk được embedded; metadata được lưu kèm để lọc, cập nhật và truy vết.",
      "Query được xây từ CandidateProfile và cấu hình phỏng vấn, sau đó dùng cùng embedding model để tạo vector q.",
    ],
    ["D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M4"]);
}

// Slide 17
{
  const slide = presentation.slides.add();
  addHeader(slide, "05  Evaluation", "Hybrid wins holdout MRR, but production activation is not justified", "The gain over vector is small and comes with compatibility and latency risks.", 17);
  slide.charts.add("bar", {
    position: { left: 66, top: 194, width: 660, height: 370 },
    categories: ["Lexical", "Vector", "Hybrid"],
    series: [{
      name: "Holdout MRR",
      values: [0.6563, 0.9531, 0.9688],
      fill: BLUE2,
      valuesFormatCode: "0.0000",
      points: [
        { idx: 0, fill: GREEN },
        { idx: 1, fill: PURPLE },
        { idx: 2, fill: "#7A4AD0" },
      ],
    }],
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 65, varyColors: true },
    hasLegend: false,
    yAxis: { min: 0, max: 1, majorUnit: 0.2, numberFormatCode: "0.0", majorGridlines: { style: "solid", fill: LINE, width: 1 }, textStyle: { fill: MUTED, fontSize: 12 } },
    xAxis: { textStyle: { fill: TEXT, fontSize: 15, bold: true } },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fill: NAVY, fontSize: 13, bold: true } },
    chartFill: WHITE,
    chartLine: { style: "solid", fill: LINE, width: 1 },
    plotAreaFill: WHITE,
  });
  addText(slide, "HOLDOUT RESULTS", 774, 200, 374, 30, { fontSize: 21, bold: true, color: NAVY });
  addSimpleTable(slide, [
    ["METHOD", "MRR", "HIT@5"],
    ["Lexical", "0.6563", "66.67%"],
    ["Vector", "0.9531", "100%"],
    ["Hybrid", "0.9688", "100%"],
  ], 770, 244, [180, 120, 120], 54, { headerFill: NAVY, bandFill: PURPLE_PALE });
  addText(slide, "Warm latency", 772, 490, 160, 28, { fontSize: 18, bold: true, color: NAVY });
  addText(slide, "Lexical 5.91 ms", 930, 488, 220, 28, { fontSize: 18, color: GREEN });
  addText(slide, "Vector / Hybrid approx. 1.12 s", 930, 524, 250, 28, { fontSize: 18, color: PURPLE });
  addRect(slide, 766, 574, 430, 76, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "Decision: retain lexical Top-8 in production.", 792, 597, 378, 30, { fontSize: 19, bold: true, color: RED, alignment: "center" });
  addSourceFooter(slide, "Source: M5 48-query synthetic holdout.");
  addNotes(slide,
    [
      "Slide mới thay future claim Recall@K/MRR bằng kết quả benchmark đã hoàn thành.",
      "Hybrid cao nhất trên holdout nhưng chỉ hơn vector 0.0157 MRR, trong khi latency và compatibility chưa đạt.",
      "Cần nhắc strict level filter từng gây regression; vì vậy chưa bật production.",
    ],
    ["D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M5"]);
}

// Slide 18
{
  const slide = presentation.slides.add();
  addHeader(slide, "05  Evaluation", "Vector context improves grounding, but overall quality remains unproven", "M6 compares No-RAG, lexical, vector and hybrid conditions.", 18);
  addMetric(slide, "80", "controlled cases", 80, 204, 210, BLUE2);
  addMetric(slide, "32", "holdout cases", 328, 204, 210, BLUE2);
  addMetric(slide, "1.875 / 2", "vector grounding", 576, 204, 220, PURPLE);
  addMetric(slide, "96.88%", "technical validity", 834, 204, 210, GREEN);
  addMetric(slide, "+0.2188", "grounding improvement", 1050, 204, 170, PURPLE);
  addRule(slide, 96, 334, 1088, 2, LINE);
  addText(slide, "What improved", 102, 372, 220, 30, { fontSize: 21, bold: true, color: GREEN });
  addText(slide, "Vector retrieval increased grounding against the controlled reference set.", 102, 414, 476, 64, { fontSize: 20, color: TEXT });
  addText(slide, "What remains unproven", 678, 372, 300, 30, { fontSize: 21, bold: true, color: ORANGE });
  addText(slide, "No clear overall downstream-quality advantage was established over the production path.", 678, 414, 470, 64, { fontSize: 20, color: TEXT });
  addRect(slide, 96, 520, 1088, 94, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "0 unsupported/hallucinated questions were observed in this tested set.", 132, 542, 1016, 30, { fontSize: 21, bold: true, color: RED, alignment: "center" });
  addText(slide, "This does not establish a universal 0% hallucination rate. LLM-as-judge; holdout was English-only.", 132, 578, 1016, 24, { fontSize: 15, color: MUTED, alignment: "center" });
  addSourceFooter(slide, "Source: M6 question-generation evaluation.");
  addNotes(slide,
    [
      "Slide mới đưa số liệu M6 vào đúng ranh giới.",
      "Không nói 0% hallucination. Câu an toàn là không quan sát thấy trường hợp unsupported trong tập kiểm thử này.",
      "Holdout chỉ có tiếng Anh nên chưa suy rộng sang tiếng Việt.",
    ],
    ["D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M6"]);
}

// Slide 19
{
  const slide = presentation.slides.add();
  addHeader(slide, "05  Evaluation", "The evaluator preserves ordering, but absolute score trust remains low", "M7 uses automated references across 80 answers - not expert-human labels.", 19);
  addSimpleTable(slide, [
    ["METRIC", "TEXT", "VOICE"],
    ["Spearman correlation", "0.954", "0.889"],
    ["MAE", "1.298", "1.244"],
    ["Pairwise ordering", "95.83%", "89.58%"],
    ["Strict group ordering", "75.0%", "37.5%"],
    ["Critical-error detection", "87.5%", "87.5%"],
    ["Unsupported feedback", "9.38%", "12.5%"],
  ], 68, 188, [470, 280, 280], 52, { headerFill: NAVY, bandFill: PALE });
  addRect(slide, 68, 578, 1030, 70, { geometry: "roundRect", fill: ORANGE_PALE, line: "#F4B38F", lineWidth: 1 });
  addText(slide, "Production score trust: LOW", 100, 598, 330, 30, { fontSize: 22, bold: true, color: RED });
  addText(slide, "Good rank correlation does not guarantee calibrated or human-equivalent scoring.", 444, 596, 628, 34, { fontSize: 18, bold: true, color: TEXT });
  addRect(slide, 1120, 188, 94, 460, { geometry: "roundRect", fill: PURPLE_PALE, line: PURPLE, lineWidth: 1 });
  addText(slide, "AUTO\nREF", 1130, 350, 74, 72, { fontSize: 20, bold: true, color: PURPLE, alignment: "center" });
  addSourceFooter(slide, "Source: M7 automated-reference benchmark.");
  addNotes(slide,
    [
      "Slide mới thay consistency 85.34% bằng các metric có định nghĩa rõ: Spearman, MAE, pairwise ordering và critical-error detection.",
      "Text tốt hơn voice về ordering; voice strict ordering chỉ 37.5% nên cần calibration và human review.",
      "Không gọi Spearman 0.954 là 95.4% accuracy.",
    ],
    ["D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M7"]);
}

// Slide 20
{
  const slide = presentation.slides.add();
  addHeader(slide, "06  Conclusion", "Measured progress, with trustworthy activation still ahead", "Retrieval benchmarks are now evidence, while human validation and production synchronization remain future work.", 20);
  addText(slide, "CONTRIBUTIONS", 74, 190, 490, 32, { fontSize: 24, bold: true, color: NAVY });
  addRule(slide, 74, 231, 500, 4, BLUE2);
  addBulletList(slide, [
    "Structured CV extraction with controlled OCR evaluation.",
    "Versioned knowledge corpus with measurable chunk preservation.",
    "Lexical, vector and hybrid Hit@K / MRR benchmarks.",
    "M1-M7 evaluation with explicit evidence boundaries.",
  ], 78, 258, 510, { gap: 74, fontSize: 18, circleFill: BLUE2 });
  addText(slide, "NEXT WORK", 680, 190, 490, 32, { fontSize: 24, bold: true, color: NAVY });
  addRule(slide, 680, 231, 500, 4, ORANGE);
  addBulletList(slide, [
    "Build a larger expert-human benchmark.",
    "Deduplicate the corpus and use group-based splitting.",
    "Correct level-filter compatibility and evaluate reranking.",
    "Synchronize evaluated pipelines with the production branch.",
    "Expand real-world, multilingual and voice evaluation.",
  ], 684, 258, 510, { gap: 62, fontSize: 17, circleFill: ORANGE });
  addRect(slide, 108, 614, 1064, 48, { geometry: "roundRect", fill: NAVY, line: NAVY, lineWidth: 0 });
  addText(slide, "Activate new AI paths only when quality, compatibility, latency and evidence gates are all satisfied.", 136, 626, 1008, 26, { fontSize: 18, bold: true, color: WHITE, alignment: "center" });
  addNotes(slide,
    [
      "Sửa Future Work cũ: MRR và Hit@K đã được hoàn thành ở M4-M5 nên chuyển sang Contribution.",
      "Future work mới tập trung vào expert-human labels, dedup, filtering, reranking và đồng bộ code production.",
      "Kết luận bảo vệ: nhóm có pipeline và benchmark rõ, nhưng không cố trình bày shadow experiment như production feature.",
    ],
    [
      "D:\\Downloads\\FiPilot_Capstone_Presentation (1).pdf, old slide 26",
      "D:\\Downloads\\FiPilot_Evaluation_Master_M1_M7.md, M1-M7 synthesis",
    ]);
}

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}

await fs.mkdir(RENDER, { recursive: true });
await fs.mkdir(LAYOUT, { recursive: true });

for (const [index, slide] of presentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  await writeBlob(`${RENDER}\\${stem}.png`, await presentation.export({ slide, format: "png", scale: 1 }));
  await fs.writeFile(`${LAYOUT}\\${stem}.layout.json`, await (await slide.export({ format: "layout" })).text());
}

await writeBlob(`${BUILD}\\montage_v4.webp`, await presentation.export({ format: "webp", montage: true, scale: 1 }));
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUT);

console.log(`Created ${OUT}`);
console.log(`Rendered ${presentation.slides.items.length} slides to ${RENDER}`);
