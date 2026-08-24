import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const TMP = "D:\\OJT_F_Software\\ojt\\Mapping\\data_cv\\fix-ai\\fipilot\\tmp\\presentations\\knowledge_matrix_slide";
const OUT = "D:\\OJT_F_Software\\ojt\\Mapping\\data_cv\\fix-ai\\fipilot\\output\\presentations\\FiPilot_Knowledge_Matrix_Structure_Slide.pptx";
const W = 1280;
const H = 720;

const C = {
  bg: "#F7F9FC",
  white: "#FFFFFF",
  navy: "#173F7A",
  blue: "#2F66C5",
  bluePale: "#EAF1FC",
  purple: "#5F36B3",
  purplePale: "#F0EAFE",
  green: "#17824F",
  greenPale: "#E7F5ED",
  orange: "#E96324",
  orangePale: "#FFF0E8",
  line: "#C8D8F0",
  text: "#182235",
  muted: "#66748A",
};

function addText(slide, text, left, top, width, height, options = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontFamily: "Arial",
    fontSize: options.fontSize ?? 16,
    bold: options.bold ?? false,
    color: options.color ?? C.text,
    alignment: options.alignment ?? "left",
    italic: options.italic ?? false,
  };
  return shape;
}

function addRect(slide, left, top, width, height, options = {}) {
  const geometry = options.geometry ?? "roundRect";
  return slide.shapes.add({
    geometry,
    position: { left, top, width, height },
    fill: options.fill ?? C.white,
    line: {
      style: "solid",
      fill: options.line ?? C.line,
      width: options.lineWidth ?? 1,
    },
    ...(geometry === "roundRect" ? { borderRadius: "rounded-xl" } : {}),
  });
}

function addRule(slide, left, top, width, fill = C.line) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left, top, width, height: 2 },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function addFlowStep(slide, number, title, body, left, top, color, fill) {
  addRect(slide, left, top, 314, 58, { fill, line: color, lineWidth: 1 });
  addRect(slide, left + 12, top + 12, 34, 34, {
    geometry: "ellipse",
    fill: color,
    line: color,
    lineWidth: 0,
  });
  addText(slide, number, left + 12, top + 18, 34, 22, {
    fontSize: 16,
    bold: true,
    color: C.white,
    alignment: "center",
  });
  addText(slide, title, left + 58, top + 8, 236, 22, {
    fontSize: 16,
    bold: true,
    color,
  });
  addText(slide, body, left + 58, top + 30, 240, 22, {
    fontSize: 16,
    color: C.text,
  });
}

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}

const presentation = Presentation.create({ slideSize: { width: W, height: H } });
const slide = presentation.slides.add();
slide.background.fill = C.bg;

// Connectors are created before the nodes so they remain behind the content.
slide.shapes.add({
  geometry: "rightArrow",
  position: { left: 410, top: 346, width: 40, height: 24 },
  fill: C.blue,
  line: { style: "solid", fill: C.blue, width: 0 },
});
slide.shapes.add({
  geometry: "rightArrow",
  position: { left: 818, top: 346, width: 40, height: 24 },
  fill: C.purple,
  line: { style: "solid", fill: C.purple, width: 0 },
});

addText(slide, "03  DATA & KNOWLEDGE", 56, 28, 330, 24, {
  fontSize: 14,
  bold: true,
  color: C.blue,
});
addText(slide, "The knowledge matrix aligns role, level and topic evidence", 56, 57, 1120, 48, {
  fontSize: 36,
  bold: true,
  color: C.navy,
});
addText(slide, "Two catalog dimensions become bounded, traceable context for the interview planner.", 58, 112, 1090, 30, {
  fontSize: 18,
  color: C.muted,
});
addRect(slide, 1174, 28, 38, 38, { geometry: "rect", fill: "#DCE8FA", line: "#DCE8FA", lineWidth: 0 });
addRect(slide, 1219, 28, 38, 38, { geometry: "rect", fill: "#91B1EB", line: "#91B1EB", lineWidth: 0 });
addRule(slide, 56, 151, 1200);

// Source matrix.
addRect(slide, 58, 180, 346, 404, { fill: C.bluePale, line: C.blue, lineWidth: 1 });
addText(slide, "SOURCE MATRIX", 82, 202, 298, 28, {
  fontSize: 21,
  bold: true,
  color: C.blue,
  alignment: "center",
});
addText(slide, "10 roles  ×  4 levels", 82, 241, 298, 42, {
  fontSize: 28,
  bold: true,
  color: C.navy,
  alignment: "center",
});
addRule(slide, 90, 296, 282, C.line);
addText(slide, "DOMAIN TOPICS", 84, 314, 146, 24, { fontSize: 16, bold: true, color: C.blue });
addText(slide, "domains[role]", 236, 314, 136, 24, { fontSize: 16, bold: true, color: C.navy, alignment: "right" });
addText(slide, "Category  →  Subcategory  →  Topic", 84, 349, 288, 28, {
  fontSize: 16,
  bold: true,
  color: C.text,
  alignment: "center",
});
addText(slide, "Each topic stores a title, path and interview anchors.", 86, 384, 284, 48, {
  fontSize: 16,
  color: C.muted,
  alignment: "center",
});
addRule(slide, 90, 445, 282, C.line);
addText(slide, "LEVEL GUIDANCE", 84, 463, 166, 24, { fontSize: 16, bold: true, color: C.purple });
addText(slide, "levels[role][level]", 234, 463, 138, 24, { fontSize: 16, bold: true, color: C.navy, alignment: "right" });
addRect(slide, 84, 500, 288, 48, { fill: C.purplePale, line: C.purple, lineWidth: 1 });
addText(slide, "Intern  |  Junior  |  Middle  |  Senior", 94, 514, 268, 24, {
  fontSize: 16,
  bold: true,
  color: C.purple,
  alignment: "center",
});

// Catalog records.
addRect(slide, 452, 180, 360, 404, { fill: C.white, line: C.line, lineWidth: 1 });
addText(slide, "CATALOG RECORDS", 478, 202, 308, 28, {
  fontSize: 21,
  bold: true,
  color: C.navy,
  alignment: "center",
});
addRect(slide, 482, 247, 300, 114, { fill: C.bluePale, line: C.blue, lineWidth: 1 });
addText(slide, "TOPIC RECORD", 500, 262, 264, 22, { fontSize: 17, bold: true, color: C.blue, alignment: "center" });
addText(slide, "title · path · anchors\nrole + topic path + anchor text", 500, 294, 264, 48, {
  fontSize: 16,
  color: C.text,
  alignment: "center",
});
addRect(slide, 482, 377, 300, 86, { fill: C.purplePale, line: C.purple, lineWidth: 1 });
addText(slide, "LEVEL RECORD", 500, 391, 264, 22, { fontSize: 17, bold: true, color: C.purple, alignment: "center" });
addText(slide, "knowledge depth · evaluation focus", 500, 424, 264, 24, {
  fontSize: 16,
  color: C.text,
  alignment: "center",
});
addRect(slide, 482, 480, 300, 78, { fill: C.navy, line: C.navy, lineWidth: 0 });
addText(slide, "topic_id = role :: path :: title", 496, 494, 272, 22, { fontSize: 16, bold: true, color: C.white, alignment: "center" });
addText(slide, "document_id = SHA-256(topic_id)[:32]", 490, 524, 284, 22, { fontSize: 16, color: "#D8E5FF", alignment: "center" });

// Runtime selection.
addRect(slide, 860, 180, 362, 404, { fill: C.white, line: C.line, lineWidth: 1 });
addText(slide, "RUNTIME SELECTION", 888, 202, 306, 28, {
  fontSize: 21,
  bold: true,
  color: C.navy,
  alignment: "center",
});
addText(slide, "CandidateProfile: role · skills · evidence", 886, 239, 310, 22, {
  fontSize: 16,
  bold: true,
  color: C.blue,
  alignment: "center",
});
addText(slide, "InterviewConfig: target experience level", 886, 265, 310, 22, {
  fontSize: 16,
  bold: true,
  color: C.purple,
  alignment: "center",
});
addFlowStep(slide, "1", "Select domain", "Profile tokens + domain terms", 884, 302, C.blue, C.bluePale);
addFlowStep(slide, "2", "Attach level guidance", "Up to 10 guidance statements", 884, 368, C.purple, C.purplePale);
addFlowStep(slide, "3", "Score domain topics", "Token overlap + exact-title boost", 884, 434, C.green, C.greenPale);
addFlowStep(slide, "4", "Return bounded context", "Top-8 topics → Interview Planner", 884, 500, C.orange, C.orangePale);

addRect(slide, 58, 606, 1164, 58, { fill: C.navy, line: C.navy, lineWidth: 0 });
addText(slide, "Production uses deterministic lexical scoring; embeddings and vector search remain a research shadow.", 88, 623, 1104, 28, {
  fontSize: 18,
  bold: true,
  color: C.white,
  alignment: "center",
});
addText(slide, "Source: Knowledge/; catalog.json; chunks.py; local.py; interview_planner/agent.py", 56, 686, 1168, 16, {
  fontSize: 11,
  color: C.muted,
  alignment: "right",
});

slide.speakerNotes.textFrame.setText([
  "[VỊ TRÍ VÀ HƯỚNG DẪN CHỈNH SỬA]",
  "Loại: SLIDE MỚI - BỔ SUNG",
  "Vị trí: Chèn sau slide 15 - Resume-to-CandidateProfile Method và trước slide 16 - RAG Knowledge Retrieval Pipeline trong deck cũ.",
  "Cách thực hiện: Dùng slide này để trả lời cấu trúc Knowledge Matrix, nguồn dữ liệu và cách matrix đi vào Interview Planner.",
  "",
  "[SPEAKER NOTES NHANH]",
  "Knowledge Matrix không phải model được train; đây là catalog kiến thức curated và có thể truy vết.",
  "Matrix có hai cấu trúc liên kết theo role: domains[role] chứa cây Category → Subcategory → Topic; levels[role][level] chứa hướng dẫn theo Intern, Junior, Middle, Senior.",
  "Mỗi topic có title, path và anchors. Hệ thống tạo topic_id ổn định; document_id là 32 ký tự đầu của SHA-256(topic_id), đồng thời giữ content hash để so sánh nội dung.",
  "Ở runtime, CandidateProfile cung cấp role/skills/evidence; target experience level đến từ InterviewConfig.",
  "Production chọn domain bằng token matching, ghép tối đa 10 level-guidance statements, chấm điểm topic bằng token overlap và exact-title boost, rồi trả tối đa 8 topic cho Interview Planner.",
  "Cần giữ ranh giới: production hiện dùng lexical scoring; embedding/vector là research shadow.",
  "",
  "[Sources]",
  "- Knowledge\\Domains\\<Role>\\<Category>\\<Subcategory>\\<Topic>.md",
  "- Knowledge\\Levels\\<Role>\\<Intern|Junior|Middle|Senior>.md",
  "- backend\\services\\interview_knowledge\\catalog.json",
  "- backend\\services\\interview_knowledge\\chunks.py",
  "- backend\\services\\interview_knowledge\\local.py",
  "- backend\\services\\interview_planner\\agent.py",
]);
slide.speakerNotes.setVisible(true);

await fs.mkdir(TMP, { recursive: true });
await fs.mkdir("D:\\OJT_F_Software\\ojt\\Mapping\\data_cv\\fix-ai\\fipilot\\output\\presentations", { recursive: true });
await writeBlob(`${TMP}\\knowledge-matrix-slide.png`, await presentation.export({ slide, format: "png", scale: 2 }));
await fs.writeFile(`${TMP}\\knowledge-matrix-slide.layout.json`, await (await slide.export({ format: "layout" })).text());
await fs.writeFile(`${TMP}\\inspection.ndjson`, (await presentation.inspect({
  kind: "slide,textbox,shape,notes",
  maxChars: 20000,
})).ndjson);
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUT);
console.log(`Created ${OUT}`);
