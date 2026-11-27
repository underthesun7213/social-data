// Build the H&M retention deck as native PPTX, Korean and English.
// Usage: node build.js ko|en <outfile>
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const LANG = process.argv[2];
const OUT = process.argv[3];
const T = (ko, en) => (LANG === "ko" ? ko : en);
const NOTES = JSON.parse(fs.readFileSync(path.join(__dirname, `notes_${LANG}.json`), "utf8"));

// H&M red sampled from the logo vector in H&M's FY2025 annual report (#E30415)
const RED = "E30415", INK = "111111", G1 = "58585B", G2 = "808284", G3 = "B8B8BA", BG2 = "F4F4F4", LINE = "DCDCDC", WHITE = "FFFFFF";
const THEME = {
  name: "H&M Retention Study",
  headFontFace: T("Malgun Gothic", "Georgia"),
  bodyFontFace: T("Malgun Gothic", "Arial"),
  colors: { dk1: INK, lt1: WHITE, dk2: G1, lt2: BG2, accent1: RED, accent2: G2, accent3: G3, accent4: "404042", accent5: "7B72B4", accent6: "C7C1E0", hlink: RED, folHlink: G1 },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = T("H&M 고객 유지·채널 분석", "H&M Retention and Channel Analysis");
pres.author = "Derek, Juan, Juha, Saddam";
const C = pres.SchemeColor;
const MX = 0.6, CW = 12.133; // margin, content width
const SW = 13.333, SH_ = 7.5; // slide size
// Photos: free Unsplash licence, cropped and toned by prep_photos.py
const PHOTO_DIR = process.env.PHOTO_DIR || path.join(__dirname, "photos");
const PHOTO = {
  cover: ["cover.jpg", "Bernd Dittrich"],
  part1: ["part1.jpg", "Tim Mossholder"],
  part2: ["part2.jpg", "Kiko Camaclang"],
  part3: ["part3.jpg", "Andrej Lišakov"],
  part4: ["part4.jpg", "Ashim D’Silva"],
  closing: ["closing.jpg", "Charlota Blunarova"],
};
const photoPath = (k) => path.join(PHOTO_DIR, PHOTO[k][0]);
const credit = (k) => `Photo: ${PHOTO[k][1]} / Unsplash`;
// one shadow style for the whole deck; a fresh object every call (pptxgenjs mutates options)
const shadow = () => ({ type: "outer", color: "000000", opacity: 0.16, blur: 10, offset: 3, angle: 90 });

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "COVER", background: { color: INK },
  objects: [
    { rect: { x: MX, y: 1.55, w: 0.16, h: 0.16, fill: { color: RED } } },
    { placeholder: { options: { name: "kicker", type: "body", x: MX + 0.3, y: 1.43, w: 11, h: 0.4, fontSize: 12, bold: true, color: "B8B8BA", charSpacing: 2, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: MX, y: 2.05, w: 11.5, h: 2.1, fontSize: 44, bold: true, color: WHITE, valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "sub", type: "body", x: MX, y: 4.35, w: 11, h: 1.0, fontSize: 18, color: "C9C9CB", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "foot", type: "body", x: MX, y: 6.55, w: 12, h: 0.5, fontSize: 11, color: "A0A0A3", valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT", background: { color: WHITE },
  objects: [
    { rect: { x: MX, y: 0.47, w: 0.12, h: 0.12, fill: { color: RED } } },
    { placeholder: { options: { name: "eyebrow", type: "body", x: MX + 0.24, y: 0.38, w: 11.5, h: 0.3, fontSize: 11, bold: true, color: RED, charSpacing: 1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: MX, y: 0.78, w: CW, h: 0.95, fontSize: 26, bold: true, color: INK, valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "source", type: "body", x: MX, y: 6.98, w: 11.2, h: 0.32, fontSize: 9, color: G2, valign: "top", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.33, y: 6.98, w: 0.4, h: 0.3, fontSize: 9, color: G2, align: "right" },
});
pres.defineSlideMaster({
  title: "SECTION", background: { color: BG2 },
  objects: [
    { placeholder: { options: { name: "num", type: "body", x: MX, y: 1.9, w: 11, h: 1.2, fontSize: 66, bold: true, color: RED, margin: 0, valign: "bottom" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: MX, y: 3.2, w: 11, h: 1.1, fontSize: 36, bold: true, color: INK, valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "desc", type: "body", x: MX, y: 4.35, w: 10, h: 1.2, fontSize: 16, color: G1, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "PSECTION", background: { color: BG2 },
  objects: [
    { rect: { x: MX, y: 1.95, w: 0.16, h: 0.16, fill: { color: RED } } },
    { placeholder: { options: { name: "num", type: "body", x: MX + 0.3, y: 1.83, w: 5, h: 0.4, fontSize: 13, bold: true, color: RED, charSpacing: 2, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: MX, y: 2.45, w: 5.7, h: 1.6, fontSize: 34, bold: true, color: INK, valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "desc", type: "body", x: MX, y: 4.2, w: 5.5, h: 1.6, fontSize: 15, color: G1, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "DARK", background: { color: INK },
  objects: [
    { rect: { x: MX, y: 0.47, w: 0.12, h: 0.12, fill: { color: RED } } },
    { placeholder: { options: { name: "eyebrow", type: "body", x: MX + 0.24, y: 0.38, w: 11.5, h: 0.3, fontSize: 11, bold: true, color: "B8B8BA", charSpacing: 1, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", align: "left", x: MX, y: 1.1, w: CW, h: 2.3, fontSize: 30, bold: true, color: WHITE, valign: "top", margin: 0 }, text: "" } },
  ],
});

// ---------- helpers ----------
let section = "";
function sec(title) { section = title; pres.addSection({ title }); }
let STEP = null;
const STEPS = [["회사", "Company"], ["문제", "Problem"], ["데이터", "Data"], ["단서", "Clue"], ["방법", "Method"], ["분석", "Analysis"], ["해결", "Solution"]];
// journey strip: where this slide sits in the story
function progress(s) {
  if (!STEP) return;
  const runs = [];
  STEPS.forEach((p, i) => {
    const on = p[0] === STEP;
    runs.push({ text: T(p[0], p[1]), options: { bold: on, color: on ? RED : "A8A8AB" } });
    if (i < STEPS.length - 1) runs.push({ text: "   ›   ", options: { color: "CFCFD1" } });
  });
  txt(s, runs, { x: MX, y: 0.1, w: 9, h: 0.22, fontSize: 8, objectName: "progress" });
}
function content(eyebrow, title, source, noteKeys) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(eyebrow, { placeholder: "eyebrow" });
  s.addText(title, { placeholder: "title" });
  if (source) s.addText(source, { placeholder: "source" });
  progress(s);
  notes(s, noteKeys);
  return s;
}
function notes(s, keys) {
  if (!keys) return;
  const arr = Array.isArray(keys) ? keys : [keys];
  const txt = arr.map((k) => (k.startsWith("=") ? k.slice(1) : NOTES[k] || "")).filter(Boolean).join("\n\n");
  if (txt) s.addNotes(txt);
}
// Evidence labels (instructor feedback: keep what the data show, what we estimate and what we assume apart)
const TAG = {
  data: { t: T("데이터", "DATA"), w: T(0.72, 0.62), fill: INK, line: INK, color: WHITE },
  est: { t: T("추정", "ESTIMATE"), w: T(0.62, 0.98), fill: WHITE, line: G1, color: G1 },
  asm: { t: T("가정", "ASSUMPTION"), w: T(0.62, 1.18), fill: WHITE, line: RED, color: RED },
};
function pill(s, kind, x, y) {
  const k = TAG[kind];
  s.addText(k.t, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x, y, w: k.w, h: 0.26, fill: { color: k.fill }, line: { color: k.line, width: 1 }, fontSize: 9, bold: true, color: k.color, align: "center", valign: "middle", margin: 0, charSpacing: 1, objectName: "tag-" + kind });
  return k.w;
}
// slide-level labels, right-aligned in the eyebrow row
function tags(s, kinds) {
  let x = MX + CW;
  [...kinds].reverse().forEach((k) => { x -= TAG[k].w; pill(s, k, x, 0.39); x -= 0.08; });
}
// method line under the title: names the analysis so the audience knows what the chart is
function method(s, body) {
  const lw = T(0.88, 0.82);
  s.addText(T("분석 방법", "METHOD"), { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: MX, y: 1.34, w: lw, h: 0.26, fill: { color: WHITE }, line: { color: INK, width: 1 }, fontSize: 9, bold: true, color: INK, align: "center", valign: "middle", margin: 0, charSpacing: 1, objectName: "method-label" });
  txt(s, body, { x: MX + lw + 0.14, y: 1.32, w: CW - lw - 0.14, h: 0.48, fontSize: 12, color: G1, objectName: "method-text" });
}
// method steps: method name, then the calculation as numbered steps the audience can follow
function steps(s, name, items) {
  const lw = T(0.88, 0.82);
  s.addText(T("분석 방법", "METHOD"), { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: MX, y: 1.32, w: lw, h: 0.26, fill: { color: WHITE }, line: { color: INK, width: 1 }, fontSize: 9, bold: true, color: INK, align: "center", valign: "middle", margin: 0, charSpacing: 1, objectName: "method-label" });
  txt(s, name, { x: MX + lw + 0.14, y: 1.31, w: CW - lw - 0.14, h: 0.3, fontSize: 12.5, bold: true, color: INK, objectName: "method-name" });
  const gap = 0.24, n = items.length, w = (CW - gap * (n - 1)) / n, y = 1.7, h = 0.58;
  items.forEach((it, i) => {
    const x = MX + i * (w + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: BG2 }, line: { type: "none" }, objectName: "step-" + (i + 1) });
    s.addText(String(i + 1), { shape: pres.shapes.OVAL, x: x + 0.1, y: y + 0.15, w: 0.28, h: 0.28, fill: { color: RED }, line: { type: "none" }, fontSize: 10, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    txt(s, it, { x: x + 0.47, y: y + 0.04, w: w - 0.55, h: h - 0.08, fontSize: 10.5, valign: "middle" });
    if (i < n - 1) txt(s, "›", { x: x + w, y: y + 0.08, w: gap, h: 0.4, fontSize: 16, color: G2, align: "center", valign: "middle" });
  });
}
// test line: the formal test behind a finding (effect size first, then the test)
function testline(s, x, y, w, h, body) {
  const lw = T(0.6, 0.55);
  s.addText(T("검정", "TEST"), { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x, y: y + 0.02, w: lw, h: 0.26, fill: { color: INK }, line: { color: INK, width: 1 }, fontSize: 9, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, charSpacing: 1, objectName: "test-label" });
  txt(s, body, { x: x + lw + 0.12, y, w: w - lw - 0.12, h, fontSize: 10.5, color: INK, objectName: "test-text" });
}
// inline label for a sentence: [가정] ...
const mk = (kind) => ({ text: `[${TAG[kind].t}] `, options: { bold: true, color: TAG[kind].color === WHITE ? INK : TAG[kind].color } });
function txt(s, text, o) { s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: INK, valign: "top" }, o)); }
// cards are white with the deck's one soft shadow; o.flat drops the shadow
function card(s, x, y, w, h, o = {}) {
  s.addShape(pres.shapes.RECTANGLE, Object.assign({ x, y, w, h, fill: { color: o.fill || WHITE }, line: o.line ? { color: o.line, width: o.lineW || 1.25 } : { color: "ECECEC", width: 0.5 } }, o.flat ? {} : { shadow: shadow() }, o.name ? { objectName: o.name } : {}));
}
// full-bleed photo with a dark overlay (transparency = how much photo shows through)
function bleed(s, key, overlayTransp) {
  s.addImage({ path: photoPath(key), x: 0, y: 0, w: SW, h: SH_, altText: credit(key), objectName: "photo" });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: SW, h: SH_, fill: { color: "000000", transparency: overlayTransp }, line: { type: "none" }, objectName: "overlay" });
}
function photoCredit(s, key, x, w, color) {
  txt(s, credit(key), { x, y: 7.12, w, h: 0.25, fontSize: 8, color: color || "D0D0D2", align: "right" });
}
// Part divider: text left, half-bleed photo right
function divider(num, title, desc, key, note, creditColor) {
  const s = pres.addSlide({ masterName: "PSECTION", sectionTitle: section });
  s.addImage({ path: photoPath(key), x: 6.9, y: 0, w: SW - 6.9, h: SH_, altText: credit(key), objectName: "photo" });
  s.addText(num, { placeholder: "num" });
  s.addText(title, { placeholder: "title" });
  s.addText(desc, { placeholder: "desc" });
  photoCredit(s, key, 6.9, SW - 6.9 - 0.25, creditColor);
  if (note) s.addNotes(note);
  return s;
}
function chartBase(extra) {
  return Object.assign({
    catAxisLabelColor: G1, valAxisLabelColor: G2, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    dataLabelFontFace: "+mn-lt", titleFontFace: "+mn-lt", legendFontFace: "+mn-lt",
    catAxisLabelFontSize: 10, valAxisLabelFontSize: 9, dataLabelFontSize: 10, dataLabelColor: INK,
    valGridLine: { color: "E6E6E6", size: 0.5 }, catGridLine: { style: "none" }, showLegend: false,
    catAxisLineShow: true, catAxisLineColor: G3, valAxisLineShow: false,
    titleColor: INK, titleFontSize: 12,
  }, extra);
}
// one visual series where chosen points are red: two overlapped clustered series, zeros hidden
function hiBars(labels, values, hiIdx, base, extraSeries) {
  const a = values.map((v, i) => (hiIdx.includes(i) ? 0 : v));
  const b = values.map((v, i) => (hiIdx.includes(i) ? v : 0));
  const data = [{ name: "base", labels, values: a }, { name: "hi", labels, values: b }];
  return data;
}
function table(s, rows, o) {
  const head = rows[0].map((c) => ({ text: c, options: { bold: true, fill: { color: BG2 }, color: INK } }));
  const body = rows.slice(1).map((r) => r.map((c) => (typeof c === "string" ? { text: c } : c)));
  s.addTable([head, ...body], Object.assign({ x: MX, y: 1.9, w: CW, fontSize: 11, color: INK, border: { type: "solid", pt: 0.5, color: LINE }, margin: [0.05, 0.08, 0.05, 0.08], valign: "middle" }, o));
}

// =================== SLIDES ===================
sec(T("표지", "Cover"));
STEP = null;
{
  const s = pres.addSlide({ masterName: "COVER", sectionTitle: section });
  bleed(s, "cover", 28);
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: 1.55, w: 0.16, h: 0.16, fill: { color: RED }, line: { type: "none" } });
  photoCredit(s, "cover", 7.5, SW - 7.5 - 0.25);
  s.addText(T("5601 DATA-DRIVEN DECISION MAKING · H&M 조별 프로젝트", "5601 DATA-DRIVEN DECISION MAKING · H&M GROUP PROJECT"), { placeholder: "kicker" });
  s.addText(T("신규 고객의\n‘두 번째 구매’를 되찾자", "Win back the new customer’s\nsecond purchase"), { placeholder: "title" });
  s.addText(T("H&M은 고객을 데려오고도 붙잡지 못하고 있다. 어디서 새는지 찾았고, 막을 방법 세 가지를 제안한다.", "H&M brings customers in but does not keep them. We found where they leak, and propose three ways to stop it."), { placeholder: "sub" });
  s.addText(T("Derek · Juan · Juha · Saddam  |  Kaggle H&M 거래 3,179만 행 + H&M 공식 보고서 43건  |  2026년 11월\nH&M과 무관한 학생 과제이며, H&M의 후원이나 승인을 받지 않았습니다.", "Derek · Juan · Juha · Saddam  |  31.8M Kaggle H&M transactions + 43 H&M reports  |  November 2026\nStudent coursework. Not affiliated with, sponsored or endorsed by H&M."), { placeholder: "foot" });
  notes(s, "cover");
}
sec(T("Part 1 회사와 문제", "Part 1 The company and its problem"));
divider("PART 1", T("회사와 문제", "The company and its problem"), T("H&M은 누구이고, 회사는 스스로 무엇을 걱정하나.", "Who H&M is, and what the company itself worries about."), "part1",
  T("첫 번째 파트는 회사와 문제입니다. H&M이 어떤 회사인지, 그리고 회사가 공식 보고서에서 스스로 무엇을 걱정하는지부터 보겠습니다.", "Part one is the company and its problem: who H&M is, and what it worries about in its own reports."));
STEP = "회사";
{
  const s = content(T("1 · H&M", "1 · H&M"), T("H&M, 얼마나 알고 있나요?", "How well do you know H&M?"), T("출처: H&M 연간보고서 FY2025 p.4·5·10·12 · 분기보고서 FY2024 Q1 p.4 · 분기 말 매장 수 analysis/hm_report_quarterly.csv", "Sources: H&M annual report FY2025 pp.4, 5, 10, 12 · interim report FY2024 Q1 p.4 · quarter-end store counts analysis/hm_report_quarterly.csv"), "intro");
  tags(s, ["data"]);
  const lw = T(0.88, 0.95);
  s.addText(T("회사 소개", "COMPANY"), { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: MX, y: 1.34, w: lw, h: 0.26, fill: { color: WHITE }, line: { color: INK, width: 1 }, fontSize: 9, bold: true, color: INK, align: "center", valign: "middle", margin: 0, charSpacing: 1 });
  txt(s, [{ text: T("세계 최대 패션 기업 중 하나. ", "One of the world’s largest fashion houses. "), options: { bold: true } }, { text: T("‘패션을 모두에게(Liberating fashion for the many)’를 내걸고 H&M, COS, Weekday, & Other Stories, ARKET, Sellpy 등을 운영한다. FY2025 매출 SEK 2,283억, 직원 약 13만 2천 명.", "Under the purpose ‘Liberating fashion for the many’ it runs H&M, COS, Weekday, & Other Stories, ARKET, Sellpy and more. FY2025 net sales SEK 228bn, about 132,000 employees.") }], { x: MX + lw + 0.14, y: 1.31, w: CW - lw - 0.14, h: 0.6, fontSize: 12.5, color: G1 });
  card(s, MX, 2.15, 5.6, 4.55, { fill: INK });
  txt(s, T("먼저 세 가지만 물어볼게요", "Three quick questions first"), { x: MX + 0.35, y: 2.4, w: 5, h: 0.4, fontSize: 14, bold: true, color: "C9C9CB" });
  const qs = [T("최근 1년 안에 H&M에서 옷을 산 적이 있나요?", "Have you bought from H&M in the past year?"), T("매장이었나요, 앱이나 웹이었나요?", "Was it in a store, or in the app or online?"), T("그 뒤에 또 샀나요?", "Did you buy again after that?")];
  qs.forEach((q, i) => {
    txt(s, String(i + 1), { x: MX + 0.35, y: 2.95 + i * 0.95, w: 0.5, h: 0.6, fontSize: 28, bold: true, color: RED, fontFace: "+mn-lt" });
    txt(s, q, { x: MX + 0.95, y: 3.05 + i * 0.95, w: 4.4, h: 0.8, fontSize: 17, bold: i === 2, color: WHITE });
  });
  txt(s, T("세 번째 질문이 오늘의 주제입니다.", "The third question is today’s topic."), { x: MX + 0.35, y: 6.05, w: 5, h: 0.4, fontSize: 14, color: RED, bold: true });
  const st = [
    ["81", T("개 시장, 매장 약 4,100개 (FY2025)", "markets and about 4,100 stores (FY2025)"), INK],
    [T("30%+", "30%+"), T("온라인 매출 비중, ‘30% 남짓’ (FY2025)", "of sales online, ‘just over 30%’ (FY2025)"), INK],
    [T("2억 명+", "200M+"), T("로열티 프로그램 고객 (FY2024 Q1)", "customers in the loyalty programme (FY2024 Q1)"), INK],
    ["5,076 → 4,023", T("분기 말 매장 수: FY2019 Q4 → FY2026 Q3", "stores at quarter end: FY2019 Q4 → FY2026 Q3"), RED],
  ];
  st.forEach((v, i) => {
    const x = 6.55 + (i % 2) * 3.14, y = 2.15 + Math.floor(i / 2) * 2.33;
    card(s, x, y, 2.98, 2.22);
    txt(s, v[0], { x: x + 0.25, y: y + 0.3, w: 2.6, h: 0.8, fontSize: i === 3 ? 23 : 34, bold: true, color: v[2], fontFace: "+mn-lt" });
    txt(s, v[1], { x: x + 0.25, y: y + 1.15, w: 2.5, h: 0.9, fontSize: 13, color: G1 });
  });
}
STEP = "문제";
{
  const s = content(T("1 · 증상: 회사 보고서가 말하는 것", "1 · THE SYMPTOM: WHAT H&M’S REPORTS SAY"), T("매출은 멈췄고, H&M은 매장을 닫는 것으로 대응하고 있다", "Sales have stalled, and H&M is responding by closing stores"), T("출처: H&M FY2025 연간실적 5개년 표 · FY2021–25 연간실적 · 2026년 계획: 개점 약 80, 폐점 약 160", "Sources: H&M FY2025 full-year report five-year table · full-year reports FY2021–25 · 2026 plan: about 80 openings, about 160 closures"), "situation");
  const yrs = ["FY21", "FY22", "FY23", "FY24", "FY25"];
  tags(s, ["data"]);
  s.addChart(pres.charts.BAR, hiBars(yrs, [12, 6, -1, 1, 2], [2, 3, 4]), chartBase({ x: MX, y: 1.85, w: 5.9, h: 3.7, barDir: "col", barOverlapPct: 100, barGapWidthPct: 60, chartColors: [G3, RED], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0;-0;;", showTitle: true, title: T("매출 성장률 (현지통화, %)", "Sales growth (local currencies, %)"), valAxisHidden: true, valGridLine: { style: "none" } }));
  s.addChart(pres.charts.BAR, [{ name: T("매장 수", "Stores"), labels: yrs, values: [4801, 4465, 4369, 4253, 4101] }], chartBase({ x: 6.83, y: 1.85, w: 5.9, h: 3.7, barDir: "col", barGapWidthPct: 60, chartColors: [G1], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "#,##0", showTitle: true, title: T("연말 매장 수", "Stores at year end"), valAxisHidden: true, valAxisMinVal: 0, valGridLine: { style: "none" } }));
  txt(s, [
    { text: T("매장 축소는 ", "Closing stores assumes that "), options: {} },
    { text: T("“닫은 매장의 고객은 온라인으로 따라온다”", "“customers of a closed store follow it online.”"), options: { bold: true } },
    { text: T("는 가정 위에 있다. 질문은 둘이다: ", " Two questions follow: "), options: {} },
    { text: T("고객은 어디서 새고 있나? 매장이 닫히면 정말 온라인으로 오나?", "where are customers leaking, and do store customers really move online?"), options: { bold: true, color: RED } },
  ], { x: MX, y: 5.85, w: CW, h: 0.8, fontSize: 16 });
}
{
  const s = content(T("1 · 회사가 직접 말하는 걱정", "1 · WHAT H&M ITSELF WORRIES ABOUT"), T("H&M은 고객이 갈아탈까 걱정하지만, 재구매율은 내놓지 않는다", "H&M fears customers will switch, but never reports repurchase"), T("요약은 우리 번역, 인용은 원문 그대로, 쪽 = PDF 쪽 · 보고서 43건에서 뽑은 진술 952건 중 · analysis/hm_report_statements_essential.csv", "Summaries are ours, quotes verbatim, page = PDF page · from 952 statements in 43 reports · analysis/hm_report_statements_essential.csv"), "concerns");
  tags(s, ["data"]);
  const Q = [
    [true, "Consumers are now more price-conscious and inclined to change", T("소비자는 가격에 더 민감해졌고 쉽게 갈아탄다", "Consumers have become more price-sensitive and switch easily"), "annual/2025.pdf p.9"],
    [true, "Excluding these closures, sales increased by 3 percent", T("매장을 닫으면 단기 매출이 준다. 2025 Q2 매장 4% 감소, 폐점 영향을 빼면 +3%였을 매출이 +1%", "Closing stores cuts short-term sales. 2025 Q2: 4% fewer stores; sales +1%, or +3% without the closures"), "quarterly/2025-6m.pdf p.3, 5"],
    [false, "the physical store is becoming more important than ever", T("디지털이 커져도 매장은 그 어느 때보다 중요하다", "As digital grows, the store matters more than ever"), "annual/2025.pdf p.13"],
    [false, "more returning customers", T("2018년 CEO: 재방문 고객이 늘었다. 하지만 숫자는 없다", "CEO, 2018: more returning customers, but no figure"), "annual/2018.pdf p.6"],
  ];
  Q.forEach((q, i) => {
    const x = MX + (i % 2) * 6.17, y = 1.95 + Math.floor(i / 2) * 1.95;
    card(s, x, y, 5.96, 1.8);
    s.addText(q[0] ? T("우려", "CONCERN") : T("평가", "ASSESSMENT"), { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.13, x: x + 0.25, y: y + 0.2, w: q[0] ? T(0.55, 0.9) : T(0.55, 1.1), h: 0.26, fill: { color: WHITE }, line: { color: q[0] ? RED : G1, width: 1 }, fontSize: 9, bold: true, color: q[0] ? RED : G1, align: "center", valign: "middle", margin: 0 });
    txt(s, q[3], { x: x + 2.9, y: y + 0.22, w: 2.8, h: 0.26, fontSize: 9, color: G2, align: "right" });
    txt(s, q[2], { x: x + 0.25, y: y + 0.58, w: 5.45, h: 0.68, fontSize: 15, bold: true });
    if (q[1]) txt(s, `“${q[1]}”`, { x: x + 0.25, y: y + 1.3, w: 5.45, h: 0.4, fontSize: 11, italic: true, color: G1 });
  });
  txt(s, [{ text: T("빠진 것: ", "What is missing: "), options: { bold: true } }, { text: T("멤버 수는 나와도, 재구매율이나 휴면율은 진술 952건 어디에서도 찾지 못했다. ", "member counts appear, but no repurchase or lapse rate in any of the 952 statements. ") }, { text: T("그래서 고객이 정말 돌아오는지, 거래 데이터로 직접 확인했다.", "So we checked in the transaction data whether customers really come back."), options: { bold: true, color: RED } }], { x: MX, y: 5.95, w: CW, h: 0.8, fontSize: 14 });
}
sec(T("Part 2 데이터와 단서", "Part 2 Data and the first clue"));
divider("PART 2", T("데이터와 단서", "Data and the first clue"), T("가진 데이터를 확인하고 둘러보다가, 고객이 다시 오지 않는다는 단서를 찾았다.", "We check the data, browse it, and find the clue: customers do not come back."), "part2",
  T("두 번째 파트는 데이터입니다. 무엇을 가지고 있는지 먼저 확인하고, 데이터를 둘러보다가 어떤 단서를 찾았는지 함께 보겠습니다.", "Part two is the data: what we have, and the clue we found while browsing it."));
STEP = "데이터";
{
  const s = content(T("2 · 우리가 가진 데이터", "2 · THE DATA WE HAVE"), T("구매 기록 3,179만 건: 무엇이 있고, 무엇이 없나", "31.8 million purchase records: what is there, and what is not"), T("Kaggle ‘H&M Personalized Fashion Recommendations’ (2022) · 비상업·학술 이용, 재배포 불가 · analysis/hm_data_dictionary.csv · hm_profile.py", "Kaggle ‘H&M Personalized Fashion Recommendations’ (2022) · non-commercial academic use, no redistribution · analysis/hm_data_dictionary.csv · hm_profile.py"), "datacard");
  tags(s, ["data", "asm"]);
  steps(s, T("데이터 프로파일링: 분석 전에 표와 열의 상태부터 확인했다", "Data profiling: check every table and column before analysing"), [T("세 표의 행 수·기간·연결 키 확인", "Rows, period and join keys of the three tables"), T("37개 열마다 유형·결측·고유값 세기", "Type, missing and distinct values for all 37 columns"), T("영수증이 없어 구매 1회 = 고객 × 날짜로 정의", "No receipt ID: one purchase = customer × day"), T("공식 정의가 없는 값은 ‘가정’으로 표시", "Values with no official definition marked as assumptions")]);
  const F = [
    ["transactions_train.csv", "31,788,324", T("1행 = 상품 1개 구매", "1 row = 1 item bought"), T("날짜 · 고객 · 상품 · 가격 · 채널\n2018-09-20 ~ 2020-09-22", "date · customer · item · price · channel\n2018-09-20 to 2020-09-22")],
    ["customers.csv", "1,371,980", T("1행 = 등록 고객 1명", "1 row = 1 registered customer"), T("나이 (1.2% 결측) · 멤버십 · 뉴스레터", "age (1.2% missing) · membership · newsletter")],
    ["articles.csv", "105,542", T("1행 = 상품 1개", "1 row = 1 article"), T("상품군 · 색상 · 라인 등 25개 열", "product group, colour, line: 25 columns")],
  ];
  F.forEach((f, i) => {
    const x = MX + i * 4.14;
    card(s, x, 2.4, 3.9, 2.0, i === 0 ? { fill: WHITE, line: INK, lineW: 1.5 } : {});
    txt(s, f[0], { x: x + 0.25, y: 2.52, w: 3.4, h: 0.3, fontSize: 12, bold: true, color: G1 });
    txt(s, f[1], { x: x + 0.25, y: 2.8, w: 3.4, h: 0.6, fontSize: 28, bold: true, fontFace: "+mn-lt" });
    txt(s, f[2], { x: x + 0.25, y: 3.38, w: 3.4, h: 0.3, fontSize: 12, bold: true, color: RED });
    txt(s, f[3], { x: x + 0.25, y: 3.7, w: 3.4, h: 0.65, fontSize: 11, color: G1 });
  });
  txt(s, T("상태와 처리", "State and handling"), { x: MX, y: 4.58, w: 5.9, h: 0.35, fontSize: 15, bold: true });
  const st = [
    ["data", T("결측은 거의 없다: 거래 0%, 나이 1.2%", "Almost no missing values: transactions 0%, age 1.2%")],
    ["asm", T("FN·Active는 65%가 빈칸 → 값이 1뿐이라 빈칸 = 0으로 읽음", "FN, Active 65% blank → only value is 1, so blank = 0")],
    ["data", T("영수증 번호가 없다 → 같은 고객의 같은 날 = 구매 1회 (908만 회)", "No receipt ID → same customer, same day = one purchase")],
    ["asm", T("채널 1·2의 공식 정의가 없다 → 2 = 온라인으로 가정", "Channels 1 and 2 are undefined → 2 is assumed online")],
    ["asm", T("가격은 변환값이다 → 금액이 아니라 비율로만 읽음", "Prices are transformed → read only as ratios")],
  ];
  st.forEach((r, i) => {
    pill(s, r[0], MX, 5.0 + i * 0.36);
    txt(s, r[1], { x: MX + T(0.85, 1.3), y: 4.98 + i * 0.36, w: T(5.05, 4.6), h: 0.35, fontSize: 12 });
  });
  txt(s, T("없는 것", "What is missing"), { x: 6.83, y: 4.58, w: 5.9, h: 0.35, fontSize: 15, bold: true });
  txt(s, T("매장·국가 (→ 개별 매장 폐점을 볼 수 없음) · 성별 · 실제 가격과 원가 (→ 마진은 판단 불가) · 마케팅 노출 · 2020-09 이후의 행동. 표본이라 온라인 비중(행의 70%)이 그룹 전체(약 30%)와 반대다.", "Store and country (→ no individual store closures) · gender · real prices and costs (→ no view of margins) · marketing exposure · behaviour after 2020-09. Being a sample, its online share (70% of rows) is the reverse of the group’s (about 30%)."), { x: 6.83, y: 5.0, w: 5.9, h: 1.7, fontSize: 12.5 });
}
{
  const s = content(T("2 · 데이터 둘러보기 ① 한눈에 보는 기술통계", "2 · BROWSING THE DATA ① DESCRIPTIVE STATISTICS AT A GLANCE"), T("여성복·온라인·35세 미만이 중심이고, 6월에 가장 많이 산다", "Womenswear, online and under-35s lead; June peaks"), T("가치 = 변환 가격의 합 (비율로만 읽음) · 2018-09, 2020-09는 일부 월이라 제외 · 나이 = customers.csv 등록 나이 · 상품군 = articles.csv index_group_name · hm_profile.py", "Value = sum of transformed price (ratios only) · 2018-09 and 2020-09 are partial months, left out · age = registered age in customers.csv · product group = index_group_name · hm_profile.py"), "browse0");
  tags(s, ["data"]);
  steps(s, T("기술통계: 열마다 분포를 그려 중심과 치우침을 먼저 본다", "Descriptive statistics: plot each column’s distribution to see its centre and skew"), [T("날짜 → 월별로 가치 합", "Date → value summed by month"), T("나이 → 구간별 고객 비중", "Age → share of customers by band"), T("채널 → 1·2별 거래 행 비중", "Channel → share of rows for 1 and 2"), T("상품 → 상품군별 거래 행 비중", "Article → share of rows by product group")]);
  const mo = ["18-10", "18-11", "18-12", "19-01", "19-02", "19-03", "19-04", "19-05", "19-06", "19-07", "19-08", "19-09", "19-10", "19-11", "19-12", "20-01", "20-02", "20-03", "20-04", "20-05", "20-06", "20-07", "20-08"];
  const val = [41.6, 39.0, 32.5, 33.4, 31.4, 37.5, 42.8, 43.4, 48.6, 40.4, 30.5, 40.3, 37.0, 38.9, 31.3, 28.8, 28.8, 30.3, 37.8, 37.1, 43.1, 32.4, 33.1];
  const W = 5.95, H = 2.15, X2 = MX + 6.18, Y1 = 2.42, Y2 = 4.67;
  s.addChart(pres.charts.LINE, [{ name: "value", labels: mo, values: val }], chartBase({ x: MX, y: Y1, w: W, h: H, chartColors: [INK], lineSize: 2, lineDataSymbol: "none", valAxisMinVal: 0, valAxisMaxVal: 55, valAxisLabelFontSize: 8, catAxisLabelFontSize: 8, showTitle: true, title: T("① 월별 가치 (천): 6월 정점, 2020-03 폐쇄 때 하락", "① Monthly value (k): June peaks, 2020-03 dip") }));
  s.addChart(pres.charts.BAR, [{ name: "age", labels: ["16–24", "25–34", "35–44", "45–54", "55–64", "65+"], values: [26.0, 28.7, 12.3, 18.5, 10.1, 3.2] }], chartBase({ x: X2, y: Y1, w: W, h: H, barDir: "col", barGapWidthPct: 50, chartColors: [G3], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", dataLabelFontSize: 9, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 35, showTitle: true, title: T("② 연령대별 고객 비중 (%): 중앙값 32세, 두 봉우리", "② Customers by age band (%): median 32, two peaks") }));
  s.addChart(pres.charts.BAR, [{ name: "channel", labels: [T("2 = 온라인(가정)", "2 = online (assumed)"), T("1 = 매장(가정)", "1 = store (assumed)")], values: [70.4, 29.6] }], chartBase({ x: MX, y: Y2, w: W, h: H, barDir: "bar", barGapWidthPct: 45, chartColors: [RED], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", dataLabelFontSize: 10, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 85, catAxisOrientation: "maxMin", showTitle: true, title: T("③ 채널별 거래 행 비중 (%): 그룹 전체(온라인 약 30%)와 반대", "③ Rows by channel (%): reverse of the group’s ~30% online") }));
  s.addChart(pres.charts.BAR, [{ name: "group", labels: ["Ladieswear", "Divided", "Menswear", "Sport", "Baby/Children"], values: [64.2, 22.5, 5.6, 3.9, 3.8] }], chartBase({ x: X2, y: Y2, w: W, h: H, barDir: "bar", barGapWidthPct: 40, chartColors: [G1], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", dataLabelFontSize: 9, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 78, catAxisOrientation: "maxMin", showTitle: true, title: T("④ 상품군별 거래 행 비중 (%): 여성복이 3분의 2", "④ Rows by product group (%): womenswear is two thirds") }));
}
{
  const s = content(T("2 · 데이터 둘러보기 ② 누가 얼마나 사나", "2 · BROWSING THE DATA ② WHO BUYS HOW OFTEN"), T("고객의 3분의 1은 한 번만 샀고, 가치의 39%는 8%의 고객에게서 나온다", "A third bought once; 8% of customers make 39% of value"), T("2년간 구매 횟수 (구매 = 고객×날짜) · 가치 = 변환 가격의 합 · C1_05_Frequency · 고객당 행 수: hm_profile.py", "Purchases over two years (purchase = customer × day) · value = sum of transformed price · C1_05_Frequency · rows per customer: hm_profile.py"), "browse1");
  tags(s, ["data"]);
  steps(s, T("기술통계 · 빈도 분포: 평균 대신 분포를 본다", "Descriptive statistics: the distribution, not the average"), [T("거래 3,179만 행을 구매 908만 회로 묶기", "Group 31.8M rows into 9.08M purchases"), T("고객마다 2년간 구매 횟수 세기", "Count each customer’s purchases over two years"), T("횟수 구간별로 고객 수와 가치(가격 합) 더하기", "Per count band, add up customers and value"), T("전체로 나눠 고객 비중과 가치 비중을 나란히", "Divide by totals; customer and value shares side by side")]);
  const bands = ["1", "2", "3–4", "5–9", "10–19", "20–49", "50+"];
  s.addChart(pres.charts.BAR, [{ name: T("고객 비중", "Share of customers"), labels: bands, values: [32.9, 13.4, 14.5, 17.6, 13.8, 7.1, 0.8] }, { name: T("가치 비중", "Share of value"), labels: bands, values: [4.8, 4.0, 7.4, 17.4, 27.9, 30.5, 8.0] }], chartBase({ x: MX, y: 2.4, w: 7.6, h: 4.4, barDir: "col", barGapWidthPct: 60, chartColors: [G3, RED], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", dataLabelFontSize: 9, showLegend: true, legendPos: "t", legendFontSize: 11, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 38, catAxisTitle: T("2년간 구매 횟수", "Purchases in two years"), showCatAxisTitle: true, catAxisTitleFontSize: 10, catAxisTitleColor: G2, showTitle: true, title: T("구매 횟수 구간별 고객·가치 비중 (%)", "Share of customers and of value by purchase count (%)") }));
  const pts = [
    [T("한 번만 산 고객", "Bought only once"), "32.9%", T("고객의 3분의 1, 가치는 4.8%", "a third of customers, 4.8% of value"), RED],
    [T("20회 이상 산 고객", "Bought 20+ times"), "7.8%", T("고객 7.8%가 가치 38.5%", "7.8% of customers make 38.5% of value"), INK],
    [T("고객당 거래 행", "Rows per customer"), T("중앙값 9", "median 9"), T("최대 1,895행: 평균이 숨기는 꼬리", "max 1,895: the tail an average hides"), INK],
  ];
  pts.forEach((p, i) => {
    const y = 2.45 + i * 1.22;
    txt(s, p[0], { x: 8.55, y, w: 4.2, h: 0.3, fontSize: 12, color: G1 });
    txt(s, p[1], { x: 8.55, y: y + 0.28, w: 4.2, h: 0.6, fontSize: 28, bold: true, color: p[3], fontFace: "+mn-lt" });
    txt(s, p[2], { x: 8.55, y: y + 0.85, w: 4.2, h: 0.35, fontSize: 12 });
  });
  txt(s, [{ text: T("단서: ", "Clue: "), options: { bold: true } }, { text: T("한 번 오고 끝나는 고객이 많다. 그럼 처음 온 고객은 얼마나 다시 올까?", "many customers come once and never return. So how many first-time customers come back?"), options: { color: RED, bold: true } }], { x: 8.55, y: 6.2, w: 4.2, h: 0.6, fontSize: 13 });
}
{
  const s = content(T("2 · 데이터 둘러보기 ③ 첫 단서", "2 · BROWSING THE DATA ③ THE FIRST CLUE"), T("처음 온 고객이 다음 달에 다시 오는 비율이 19.5%에서 12.7%로", "New customers buying again next month: 19.5% → 12.7%"), T("2018-09 ~ 2019-02 첫 구매는 기존 고객이 섞여 제외 · 다음 달 = 첫 구매 다음 달력 월 · C1_03_NewCustomers · C1_04_Cohorts", "First purchases in 2018-09 to 2019-02 mix in existing customers, so excluded · next month = the calendar month after the first purchase · C1_03_NewCustomers · C1_04_Cohorts"), "browse2");
  tags(s, ["data"]);
  steps(s, T("코호트 표: 같은 달에 처음 온 고객끼리 묶어 달마다 비교한다 (첫 번째로 해 본 거친 지표)", "Cohort table: customers who first bought in the same month, compared month by month (a rough first pass)"), [T("고객마다 첫 구매 날짜 찾기", "Find each customer’s first purchase date"), T("첫 구매 월로 묶기 (2018-09 ~ 2019-02는 제외)", "Group by that month (2018-09 to 2019-02 left out)"), T("다음 달력 월에 한 번이라도 산 고객 세기", "Count those who buy again the next calendar month"), T("÷ 그 달 신규 고객 = 다음 달 재구매율", "÷ that month’s new customers = next-month rate")]);
  const m = ["19-03", "19-04", "19-05", "19-06", "19-07", "19-08", "19-09", "19-10", "19-11", "19-12", "20-01", "20-02"];
  s.addChart(pres.charts.BAR, hiBars(m, [51.2, 49.9, 48.6, 52.1, 43.4, 27.9, 29.0, 31.6, 37.0, 30.6, 25.1, 25.1], [6, 7, 8, 9, 10, 11]), chartBase({ x: MX, y: 2.4, w: 5.9, h: 3.35, barDir: "col", barOverlapPct: 100, barGapWidthPct: 45, chartColors: ["DEDEDF", G2], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0;-0;;", dataLabelFontSize: 9, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 60, showTitle: true, title: T("월별 신규 고객 수 (천 명)", "New customers per month (thousands)") }));
  s.addChart(pres.charts.LINE, [{ name: "m1", labels: m.slice(0, 11), values: [19.5, 19.2, 20.5, 19.5, 13.5, 13.9, 16.0, 14.9, 14.2, 12.3, 12.7] }], chartBase({ x: 6.83, y: 2.4, w: 5.9, h: 3.35, chartColors: [RED], lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 5, showValue: true, dataLabelPosition: "t", dataLabelFormatCode: "0.0", dataLabelFontSize: 9, valAxisMinVal: 0, valAxisMaxVal: 25, valAxisHidden: true, valGridLine: { style: "none" }, showTitle: true, title: T("다음 달에 다시 산 비율 (%) · 2020-02 제외 (다음 달 폐쇄)", "Bought again next month (%) · 2020-02 out (next month = shutdown)") }));
  txt(s, [{ text: "■ ", options: { color: "DEDEDF" } }, { text: T("2019-03 ~ 08: 첫 구매 전 관측이 12개월 미만이라, 오래 쉬다 돌아온 기존 고객이 신규로 섞였을 수 있음   ", "2019-03 to 08: under 12 months of history, so lapsed customers may count as new   ") }, { text: "■ ", options: { color: G2 } }, { text: T("2019-09 이후: 12개월 이상", "2019-09 on: 12+ months") }], { x: MX, y: 5.78, w: CW, h: 0.28, fontSize: 10, color: G1 });
  txt(s, [{ text: T("단서: ", "Clue: "), options: { bold: true } }, { text: T("신규 고객 반토막(5.1만 → 2.5만)의 상당 부분은 착시다. 착시가 적은 2019-09 이후에도 다음 달 재구매율은 16.0% → 12.7%(2020-01)로 낮아진다. ", "much of the halving of new customers (51k → 25k) is an artefact. Even from 2019-09, next-month repurchase falls 16.0% → 12.7% (2020-01). ") }, { text: T("재구매가 약해지는 신호 → 맞는 방법으로 다시 잰다", "A signal that repurchase is weakening → measure it properly"), options: { color: RED, bold: true } }], { x: MX, y: 6.12, w: CW, h: 0.7, fontSize: 13 });
}
STEP = "단서";
{
  const s = content(T("2 · 단서에서 문제로", "2 · FROM CLUE TO PROBLEM"), T("매출을 쪼개 보니, 줄어든 것은 사는 고객 수와 장바구니였다", "Breaking sales down: fewer buying customers, smaller baskets"), T("가치 = 고객 수 × 고객당 방문 × 방문당 상품 수 × 상품당 가격 · 빈도는 나머지에서 역산 · C2_U1_SalesDecomp · 그룹: FY19 Q4, FY20 Q1", "Value = customers × visits per customer × items per visit × price per item · visits derived · C2_U1_SalesDecomp · group: FY19 Q4, FY20 Q1"), "diagnosis");
  tags(s, ["data"]);
  steps(s, T("매출 분해: 가치를 네 요인의 곱으로 쪼개 1년 전 같은 달과 비교했다", "Sales decomposition: value as the product of four factors, against a year earlier"), [T("코로나 전 5개월 vs 1년 전 같은 달", "Five pre-COVID months vs the same months a year earlier"), T("가치 = 고객 수 × 방문 빈도 × 방문당 상품 수 × 상품당 가격", "Value = customers × visits × items per visit × price"), T("요인마다 전년 대비 변화율 (빈도는 나머지로 역산)", "Change in each factor (visits derived from the rest)"), T("가장 크게 떨어진 요인 = 새는 곳", "The factor that fell most = the leak")]);
  card(s, MX, 2.4, 3.3, 2.74, { fill: INK });
  txt(s, T("Kaggle 표본, 코로나 전 5개월\n(2019-10 ~ 2020-02)", "Kaggle sample, five months before COVID (2019-10 to 2020-02)"), { x: MX + 0.3, y: 2.6, w: 2.7, h: 0.7, fontSize: 12, color: "C9C9CB" });
  txt(s, "−7.5%", { x: MX + 0.3, y: 3.28, w: 2.7, h: 0.9, fontSize: 48, bold: true, color: WHITE, fontFace: "+mn-lt" });
  txt(s, T("가치, 전년 같은 달 대비\n같은 기간 그룹 매출은 +5%", "value vs a year earlier;\ngroup sales +5% in the same months"), { x: MX + 0.3, y: 4.22, w: 2.7, h: 0.8, fontSize: 12, color: "C9C9CB" });
  txt(s, "=", { x: 4.05, y: 3.45, w: 0.4, h: 0.6, fontSize: 30, color: G2, align: "center" });
  const boxes = [
    [T("구매 고객 수", "Buying customers"), "−4.3%", T("→ 누가 안 돌아오나?", "→ who stopped coming back?"), true],
    [T("고객당 방문 빈도", "Visits per customer"), T("약 −1%", "about −1%"), T("거의 변화 없음", "almost unchanged"), false],
    [T("방문당 상품 수", "Items per visit"), "−6.5%", T("→ 장바구니가 작아짐", "→ baskets got smaller"), true],
    [T("상품당 가격", "Price per item"), "+4.1%", T("문제 아님", "not the problem"), false],
  ];
  boxes.forEach((b, i) => {
    const x = 4.6 + (i % 2) * 4.12, y = 2.4 + Math.floor(i / 2) * 1.42;
    card(s, x, y, 3.95, 1.32, { fill: WHITE, line: b[3] ? RED : LINE, lineW: b[3] ? 1.5 : 0.75 });
    txt(s, b[0], { x: x + 0.25, y: y + 0.12, w: 3.5, h: 0.3, fontSize: 12, color: G1 });
    txt(s, b[1], { x: x + 0.25, y: y + 0.4, w: 3.5, h: 0.5, fontSize: 26, bold: true, color: b[3] ? RED : INK });
    txt(s, b[2], { x: x + 0.25, y: y + 0.9, w: 3.5, h: 0.3, fontSize: 12, color: b[3] ? INK : G2 });
  });
  card(s, MX, 5.32, 3.95, 1.3, { fill: INK });
  txt(s, T("문제 정의", "THE PROBLEM"), { x: MX + 0.25, y: 5.42, w: 3.5, h: 0.28, fontSize: 10, bold: true, color: "C9C9CB", charSpacing: 1 });
  txt(s, T("처음 온 고객의 재구매가 약해지는 신호가 있다. 와도 덜 산다.", "Signs that first-time customers return less, and buy less when they do."), { x: MX + 0.25, y: 5.72, w: 3.5, h: 0.8, fontSize: 14, bold: true, color: WHITE });
  const QS = [
    [T("얼마나 덜 돌아오나?", "How much less do they return?"), T("발견 1 · 코호트", "Finding 1 · cohorts")],
    [T("언제까지가 기회인가?", "Until when is there a chance?"), T("발견 2 · 생존분석", "Finding 2 · survival")],
    [T("누가 다시 오나?", "What separates those who return?"), T("발견 3 · 첫 장바구니", "Finding 3 · first basket")],
    [T("매장이 닫히면 온라인으로 오나?", "Do store customers move online?"), T("발견 4 · 폐쇄 비교", "Finding 4 · shutdown")],
  ];
  QS.forEach((q, k) => {
    const qx = 4.75 + k * 2.02;
    card(s, qx, 5.32, 1.9, 1.3, { fill: WHITE, line: LINE, lineW: 0.75 });
    txt(s, `Q${k + 1}`, { x: qx + 0.15, y: 5.4, w: 1.6, h: 0.3, fontSize: 12, bold: true, color: RED });
    txt(s, q[0], { x: qx + 0.15, y: 5.68, w: 1.65, h: 0.55, fontSize: 11, bold: true });
    txt(s, q[1], { x: qx + 0.15, y: 6.25, w: 1.65, h: 0.28, fontSize: 9.5, color: G1 });
  });
}
sec(T("Part 3 방법과 분석", "Part 3 Method and analysis"));
divider("PART 3", T("방법과 분석", "Method and analysis"), T("질문마다 맞는 방법을 고르고, 핵심 발견 넷을 하나씩 함께 확인한다. 보조 분석 둘은 부록에.", "We choose a method for each question and check the four core findings one by one; two supporting analyses are in the appendix."), "part3",
  T("세 번째 파트는 방법과 분석입니다. 단서를 질문으로 바꾸고, 질문마다 결과 변수의 종류에 맞는 방법을 골랐습니다. 그다음 발견을 하나씩 같이 보겠습니다.", "Part three is method and analysis. We turned the clue into questions, chose a method for each from the type of outcome, and then walk through the findings together."), "6E6E70");
STEP = "방법";
{
  const s = content(T("3 · 방법 선택", "3 · CHOOSING THE METHOD"), T("질문마다 결과 변수의 종류와 관측 구조를 보고 방법을 골랐다", "Outcome type and data structure decided each method"), T("기준: Altin, ‘Choosing and Interpreting Analytical Methods’ 방법 선택 가이드 · 표본이 커서 p값은 거의 0이므로 효과 크기와 95% 신뢰구간으로 읽는다", "Guide: Altin, ‘Choosing and Interpreting Analytical Methods’ · with samples this large p values are near zero, so we read effect sizes and 95% CIs"), "methodsel");
  table(s, [
    [T("질문", "Question"), T("한 행 =", "One row ="), T("결과 변수 (종류)", "Outcome (type)"), T("설명 변수 · 통제", "Predictors · controls"), T("시작 방법", "Starting method"), T("짚을 함정", "Trap to name")],
    [T("1 재구매가 줄었나", "1 Did repurchase fall?"), T("신규 고객", "new customer"), T("90일 재구매 (이진)", "90-day repurchase (binary)"), T("첫 구매 월 · 통제: 장바구니, 채널, 나이, 라인", "first-purchase month · controls: basket, channel, age, line"), T("카이제곱 → 이진 로지스틱 회귀", "Chi-square → binary logistic regression"), T("고객 구성이 바뀌어(어린 고객 증가) 생긴 하락일 수 있음 → 통제", "a shift in customer mix could explain it → control")],
    [T("2 언제 돌아오나", "2 When do they return?"), T("신규 고객", "new customer"), T("재구매까지 일수 (관측이 잘림)", "days to repurchase (censored)"), T("첫 구매 후 경과 일수", "days since first purchase"), T("가이드 밖: 생존분석 (Kaplan–Meier)", "Beyond the guide: survival analysis (Kaplan–Meier)"), T("관측 기간이 고객마다 달라 로지스틱의 고정 기간을 쓸 수 없음", "follow-up differs by customer, so no fixed window")],
    [T("3 누가 돌아오나", "3 Who returns?"), T("신규 고객", "new customer"), T("90일 재구매 (이진)", "90-day repurchase (binary)"), T("첫 장바구니 · 첫 채널 · 나이 · 라인 · 월", "first basket · channel · age · line · month"), T("이진 로지스틱 회귀", "Binary logistic regression"), T("조정한 연관이지 개입 효과가 아님", "an adjusted association, not an intervention effect")],
    [T("4 폐쇄 때 옮겼나", "4 Did they switch in closures?"), T("고객", "customer"), T("폐쇄 중 온라인 구매 (이진)", "bought online in closures (binary)"), T("폐쇄 전 채널 유형 (범주)", "channel type before closures"), T("카이제곱 + 전년 동기 비율 차이", "Chi-square + prior-year difference"), T("1년 전 그룹과 고객이 겹쳐 완전히 독립은 아님", "the prior-year group overlaps, so not fully independent")],
    [T("A 누가 휴면하나", "A Who lapses?"), T("첫해 고객", "year-1 customer"), T("이듬해 구매 없음 (이진)", "no purchase in year 2 (binary)"), T("첫해 채널 유형 · 통제: 구매 횟수, 관측 개월, 나이", "year-1 channel · controls: purchases, months observed, age"), T("이진 로지스틱 회귀", "Binary logistic regression"), T("원래 활발한 고객이 채널을 늘렸을 수 있음 → 구매 횟수 통제", "active customers may add channels → control frequency")],
    [T("B 누가 매장에 기대나", "B Who relies on stores?"), T("고객", "customer"), T("매장 구매 비중 (수치)", "in-store share (numeric)"), T("연령대 (6개)", "age band (6)"), T("일원 분산분석 + Kruskal–Wallis", "One-way ANOVA + Kruskal–Wallis"), T("분포가 치우쳐 순위 검정으로도 확인", "skewed, so also a rank test")],
  ], { y: 1.95, colW: [1.75, 1.15, 1.95, 2.55, 2.2, 2.533], fontSize: 10, rowH: 0.66 });
}
{
  const s = content(T("3 · 방법 쉽게 읽기", "3 · READING THE METHODS"), T("수업에서 다루지 않았거나 낯선 방법 네 가지, 이렇게 읽는다", "Four less familiar methods, in plain terms"), T("자세한 식과 숫자별 계산: 부록 H · analysis/hm_eda_cycle2.py, hm_tests.py", "Full formulas and each number’s calculation: Appendix H · analysis/hm_eda_cycle2.py, hm_tests.py"), "explain");
  const E = [
    [T("코호트 재구매율", "Cohort repurchase rate"), T("같은 달에 처음 온 고객을 한 묶음(코호트)으로 보고, 묶음마다 몇 명이 다시 왔는지 센다. 달끼리 비교하면 ‘요즘 온 고객’이 예전보다 덜 오는지 보인다.", "Customers who first bought in the same month form one group (a cohort). Count how many in each come back, and compare months."),
      T("90일 재구매율(m월) = m월 첫 구매 고객 중 90일 안에 다시 산 고객 ÷ m월 첫 구매 고객 (90일을 다 지켜볼 수 있는 고객만)", "90-day rate (m) = buyers of m back within 90 days ÷ buyers of m (those observable for 90 days)"),
      T("예: 2019-03 첫 구매 고객 100명 중 43명이 90일 안에 다시 샀다 → 43%", "e.g. of 100 first-time buyers in 2019-03, 43 bought again within 90 days → 43%")],
    [T("생존분석 (Kaplan–Meier)", "Survival analysis (Kaplan–Meier)"), T("‘돌아오기’를 사건으로 보고, 아직 안 돌아온 고객의 비율 S(t)를 날마다 갱신한다. 관측이 끝난 고객도 끝난 날까지는 분모에 넣는다(중도 절단). 그래서 고객마다 관측 기간이 달라도 된다.", "Treat coming back as the event and update S(t), the share not back yet, day by day. Customers whose follow-up ends stay in the denominator until it ends (censoring)."),
      T("S(t) = Π (1 − 그날 돌아온 고객 ÷ 그날까지 안 돌아온 고객)\n다음 30일 복귀 확률 = 1 − S(t+30) ÷ S(t)", "S(t) = Π (1 − returned that day ÷ not back by that day)\nnext-30-day chance = 1 − S(t+30) ÷ S(t)"),
      T("예: 90일째까지 안 온 고객 100명 중 다음 30일에 돌아오는 사람은 약 11명 (10.6%)", "e.g. of 100 not back by day 90, about 11 return in 30 days (10.6%)")],
    [T("오즈비와 조정 확률 (로지스틱 회귀 읽기)", "Odds ratios and adjusted rates (reading a logit)"), T("오즈 = 일어날 확률 ÷ 안 일어날 확률. 오즈비 1.37은 다른 조건이 같을 때 오즈가 1.37배라는 뜻이다. 퍼센트로 읽기 쉽게, 모든 고객을 그 그룹이라고 놓고 예측해 평균 낸 값이 조정 확률이다.", "Odds = p ÷ (1 − p). An odds ratio of 1.37 means 1.37 times the odds, all else equal. The adjusted rate predicts every customer as if in that group and averages."),
      T("오즈비 = [p₁ ÷ (1 − p₁)] ÷ [p₀ ÷ (1 − p₀)]\n조정 확률 = 모든 고객을 그 그룹으로 놓은 예측 확률의 평균", "odds ratio = [p₁ ÷ (1 − p₁)] ÷ [p₀ ÷ (1 − p₀)]\nadjusted rate = mean prediction with everyone set to that group"),
      T("예: 첫 장바구니 7개 이상 40.8% vs 1개 33.5% (다른 조건이 같을 때)", "e.g. first basket of 7+ items 40.8% vs 1 item 33.5%, all else equal")],
    [T("효과 크기 (Cramér’s V, η²)", "Effect sizes (Cramér’s V, η²)"), T("표본이 수십만 명이면 아주 작은 차이도 p < 0.001이 된다. 그래서 차이가 ‘있나’보다 ‘얼마나 큰가’를 0–1 척도로 따로 본다. 0에 가까울수록 차이가 작다.", "With hundreds of thousands of customers, even tiny gaps give p < 0.001. So we read how big the gap is on a 0–1 scale; near 0 means small."),
      T("V = √[ χ² ÷ (n × (min(행, 열) − 1)) ]\nη² = 그룹 간 제곱합 ÷ 전체 제곱합", "V = √[ χ² ÷ (n × (min(rows, cols) − 1)) ]\nη² = between-group sum of squares ÷ total sum of squares"),
      T("예: 폐쇄 중 온라인 구매 V 0.28 · 연령별 매장 비중 η² 0.002 (거의 없음)", "e.g. shutdown online buying V 0.28 · in-store share by age η² 0.002")],
  ];
  E.forEach((e, i) => {
    const x = MX + (i % 2) * 6.18, y = 1.85 + Math.floor(i / 2) * 2.5, w = 5.95;
    card(s, x, y, w, 2.35);
    s.addText(String(i + 1), { shape: pres.shapes.OVAL, x: x + 0.22, y: y + 0.18, w: 0.36, h: 0.36, fill: { color: RED }, line: { type: "none" }, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    txt(s, e[0], { x: x + 0.72, y: y + 0.17, w: w - 0.95, h: 0.38, fontSize: 15, bold: true, valign: "middle" });
    txt(s, e[1], { x: x + 0.22, y: y + 0.62, w: w - 0.44, h: 0.62, fontSize: 10.5, color: G1 });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.22, y: y + 1.27, w: w - 0.44, h: 0.62, fill: { color: BG2 }, line: { type: "none" } });
    txt(s, e[2], { x: x + 0.34, y: y + 1.29, w: w - 0.68, h: 0.58, fontSize: 10.5, bold: true, valign: "middle" });
    txt(s, e[3], { x: x + 0.22, y: y + 1.95, w: w - 0.44, h: 0.32, fontSize: 10.5, color: RED });
  });
}
STEP = "분석";
{
  const s = content(T("3 · 발견 1 — 신규 고객이 덜 돌아온다 (RQ1.1)", "3 · FINDING 1 — NEW CUSTOMERS COME BACK LESS (RQ1.1)"), T("코로나 전, 그룹 매출이 늘던 때도 신규 고객 재구매는 낮아졌다", "New-customer repurchase fell before COVID"), T("끝점 2019-11 = 90일 창이 2020-02-28에 끝나는 마지막 코호트 · 하락 폭 5–12%p (12개월 버퍼면 2019-09 → 11, −4.8%p) · 깨끗한 코호트가 1년뿐이라 계절 효과는 배제 못 함 · 계산: 부록 H", "Endpoint 2019-11 = last cohort whose 90-day window ends 2020-02-28 · drop 5–12 pp (12-month buffer: 2019-09 → 11, −4.8 pp) · one clean year, so seasonality is not ruled out · method: Appendix H"), "f1");
  tags(s, ["data"]);
  method(s, T("코호트 재구매율 분석: 첫 구매 월별로 고객을 묶고, 90일 안에 다시 산 고객 ÷ 첫 구매 후 90일을 다 지켜볼 수 있는 고객", "Cohort analysis: customers grouped by first-purchase month; bought again within 90 days ÷ customers observable for 90 days"));
  const labels = ["19-03", "19-04", "19-05", "19-06", "19-07", "19-08", "19-09", "19-10", "19-11", "19-12", "20-01", "20-02", "20-03", "20-04", "20-05", "20-06"];
  const v = [43.4, 43.3, 42.5, 38.4, 35.0, 34.8, 35.8, 32.5, 31.0, 29.8, 30.8, 29.8, 32.8, 32.4, 36.3, 35.2];
  const pre = v.map((x, i) => (i > 0 && i < 8 ? x : 0)), end = v.map((x, i) => (i === 0 || i === 8 ? x : 0)), cov = v.map((x, i) => (i >= 9 ? x : 0));
  s.addChart(pres.charts.BAR, [{ name: "pre", labels, values: pre }, { name: "end", labels, values: end }, { name: "covid", labels, values: cov }], chartBase({ x: MX, y: 2.2, w: CW, h: 3.75, barDir: "col", barOverlapPct: 100, barGapWidthPct: 45, chartColors: [G2, RED, "D9D9DB"], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0;;;", dataLabelFontSize: 9, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 50 }));
  txt(s, T("첫 구매 월 코호트별 90일 재구매율 (%) · 같은 기간 그룹 분기 매출 현지통화 +4 ~ +8%", "90-day repurchase rate by first-purchase month cohort (%) · group quarterly sales over the same period: +4 to +8% (local currencies)"), { x: MX, y: 1.8, w: CW, h: 0.35, fontSize: 13, color: G1 });
  txt(s, [{ text: "■ ", options: { color: G2 } }, { text: T("90일 창이 폐쇄 전에 끝남   ", "90-day window ends before closures   ") }, { text: "■ ", options: { color: RED } }, { text: T("비교 끝점 (2019-03, 2019-11)   ", "Compared endpoints (2019-03, 2019-11)   ") }, { text: "■ ", options: { color: "C4C4C6" } }, { text: T("90일 창이 2020년 폐쇄와 겹침 (비교 제외)", "90-day window overlaps the 2020 closures (not compared)") }], { x: MX, y: 6.0, w: CW, h: 0.35, fontSize: 11, color: G1 });
  testline(s, MX, 6.4, CW, 0.5, T("카이제곱: 깨끗한 9개 코호트 χ²(8) = 3,143, Cramér’s V = 0.09 · 로지스틱 회귀로 장바구니·채널·나이·라인을 통제해도 43.0% → 31.6% (2019-11 vs 2019-03 오즈비 0.61, 95% CI 0.59–0.63). 고객 구성이 바뀐 탓만은 아니다", "Chi-square across 9 clean cohorts: χ²(8) = 3,143, V = 0.09 · logistic regression controlling basket, channel, age and line still gives 43.0% → 31.6% (2019-11 vs 2019-03 OR 0.61, 95% CI 0.59–0.63). Not just a change in customer mix"));
}
{
  const s = content(T("3 · 발견 2 — 기회는 첫 90일 (RQ1.2)", "3 · FINDING 2 — THE WINDOW IS THE FIRST 90 DAYS (RQ1.2)"), T("90일이 지나면 돌아올 확률이 급격히 줄어든다", "After day 90 the chance of coming back drops sharply"), T("Kaplan–Meier, 2019-03 이후 신규 고객, 15일 간격, 미복귀 고객은 관측 끝에서 절단 · C2_U2_Repurchase · 계산: 부록 H", "Kaplan–Meier, new customers from 2019-03, 15-day grid, customers not yet back censored at end of data · C2_U2_Repurchase · method: Appendix H"), "f2");
  tags(s, ["data"]);
  method(s, T("생존분석(Kaplan–Meier): 아직 안 돌아온 고객도 빼지 않고 셈. 오른쪽 선 = d일까지 안 온 고객이 다음 30일 안에 돌아올 조건부 확률, 1 − S(d+30) ÷ S(d)", "Survival analysis (Kaplan–Meier): customers not back yet are kept, not dropped. Right line = chance that a customer not back by day d returns in the next 30 days, 1 − S(d+30) ÷ S(d)"));
  const days = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 365].map(String);
  const ret = [15.5, 21.5, 26.1, 29.8, 33.0, 35.8, 38.2, 40.2, 42.0, 43.7, 45.1, 46.5, 47.8, 49.0, 50.1, 51.1, 52.0, 52.9, 53.8, 54.6, 55.4, 56.2, 57.0, 57.8, 58.1];
  const nxt = [12.6, 10.6, 9.4, 8.5, 7.7, 6.8, 6.2, 5.8, 5.4, 5.1, 4.9, 4.7, 4.4, 4.0, 3.9, 3.7, 3.6, 3.6, 3.6, 3.6, 3.6, 3.7, 3.7, 3.6, 3.4];
  const lineOpts = (color, title, max) => chartBase({ x: 0, y: 0, w: 5.9, h: 3.55, chartColors: [color], lineSize: 2.5, lineDataSymbol: "none", showTitle: true, title, valAxisMinVal: 0, valAxisMaxVal: max, catAxisLabelFrequency: 3, catAxisTitle: T("첫 구매 후 일수", "Days since first purchase"), showCatAxisTitle: true, catAxisTitleFontSize: 9, catAxisTitleColor: G2 });
  s.addChart(pres.charts.LINE, [{ name: "ret", labels: days, values: ret }], Object.assign(lineOpts(G1, T("d일까지 돌아온 비율 (%)", "Share returned by day d (%)"), 70), { x: MX, y: 1.85 }));
  s.addChart(pres.charts.LINE, [{ name: "nxt", labels: days, values: nxt }], Object.assign(lineOpts(RED, T("아직 안 온 고객이 다음 30일에 올 확률 (%)", "Chance a customer not yet back returns in the next 30 days (%)"), 14), { x: 6.83, y: 1.85 }));
  txt(s, T("30일 21.5% · 90일 35.8% · 365일 58.1%", "Day 30: 21.5% · day 90: 35.8% · day 365: 58.1%"), { x: MX + 0.1, y: 5.45, w: 5.7, h: 0.35, fontSize: 13, bold: true });
  txt(s, T("30일째 10.6% → 90일째 6.8% → 270일째 3.6%", "At day 30: 10.6% → day 90: 6.8% → day 270: 3.6%"), { x: 6.93, y: 5.45, w: 5.7, h: 0.35, fontSize: 13, bold: true, color: RED });
  txt(s, [{ text: T("의미: ", "Meaning: "), options: { bold: true } }, { text: T("재구매 유도는 첫 90일 안에 해야 한다. 돌아온 고객의 중앙값은 47일, 80%가 154일 안에 왔다. ", "the prompt has to land inside the first 90 days. Returning customers came back after a median of 47 days; 80% within 154 days. ") }, { text: T("이 곡선은 언제 돌아오는지를 보여 줄 뿐, 언제 영구히 떠났는지는 알려 주지 않는다.", "The curve shows when customers return, not when they are lost for good."), options: { color: G1 } }], { x: MX, y: 6.0, w: CW, h: 0.75, fontSize: 14 });
}
{
  const s = content(T("3 · 발견 3 — 레버는 첫 장바구니 (RQ1.3)", "3 · FINDING 3 — THE LEVER IS THE FIRST BASKET (RQ1.3)"), T("첫 장바구니 크기는 일관되고, 품목군은 기간에 따라 흔들린다", "First-basket size is consistent; product group is not"), T("2019-03 이후 신규 고객 · 품목군은 90일 관측 가능 1,000명 이상 · 수영복: 90일 1위(38.1%) → 365일 중간(61.8%) · C2_U2_Repurchase · 계산: 부록 H", "New customers from 2019-03 · product groups with 1,000+ observable at 90 days · Swimwear: 1st at 90 days (38.1%) → mid-table at 365 (61.8%) · C2_U2_Repurchase · method: Appendix H"), "f3");
  tags(s, ["data"]);
  method(s, T("세그먼트 비교 + 이진 로지스틱 회귀: 첫 구매일 상품 수별 90일 재구매율을 첫 채널·나이·라인·첫 구매 월을 통제해 비교", "Segment comparison + binary logistic regression: 90-day repurchase by first-basket size, controlling first channel, age, line and first month"));
  const cats = [T("1개", "1 item"), T("2–3개", "2–3"), T("4–6개", "4–6"), T("7개 이상", "7+")];
  s.addChart(pres.charts.BAR, hiBars(cats, [32.4, 35.9, 38.2, 40.7], [3]), chartBase({ x: MX, y: 1.85, w: 5.3, h: 3.9, barDir: "col", barOverlapPct: 100, barGapWidthPct: 55, chartColors: [G2, RED], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0;;;", valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 48, showTitle: true, title: T("첫 장바구니 상품 수별 90일 재구매율 (%)", "90-day repurchase by first-basket size (%)") }));
  table(s, [
    [T("첫 구매의 특징", "First purchase"), T("90일", "90 days"), T("365일", "365 days"), T("일관성", "Consistency")],
    [T("장바구니 크기", "Basket size"), "32.4 → 40.7%", "58.1 → 65.2%", { text: T("단계마다 순서 유지", "order holds at every step"), options: { bold: true, color: RED } }],
    [T("품목군 (10개)", "Product group (10)"), "29.2–38.1%", "58.0–63.8%", T("폭 축소, 순위 바뀜", "range narrows, ranking changes")],
    [T("첫 채널: 매장 vs 온라인", "First channel: store vs online"), "41.4 vs 34.2%", "67.0 vs 59.5%", T("유지", "holds")],
    [T("연령대 (6개)", "Age band (6)"), "31.7–38.0%", "52.9–64.8%", T("65+가 가장 낮음", "65+ lowest")],
  ], { x: 6.2, y: 2.1, w: 6.53, colW: [2.0, 1.35, 1.35, 1.83], fontSize: 11, rowH: 0.62 });
  txt(s, [{ text: T("해석: ", "Reading: "), options: { bold: true } }, { text: T("순서가 지켜지는 유일한 요인이라 실행 레버로 쓰기 좋다. 다만 큰 장바구니가 원인인지, 원래 관심 많은 고객의 표시인지는 이 데이터로 가를 수 없다.", "the only factor whose order holds at every step, so it makes a good lever. But this data cannot tell whether a big basket causes return visits or marks a keen customer.") }], { x: 6.2, y: 5.55, w: 6.53, h: 1.1, fontSize: 13 });
  testline(s, MX, 5.9, 5.3, 1.0, T("로지스틱 회귀 (통제: 첫 채널·나이·라인·첫 구매 월): 7개 이상 vs 1개 오즈비 1.37 (95% CI 1.35–1.40), 조정 재구매율 33.5% → 40.8% · 매장 첫 구매 vs 온라인 오즈비 1.34. 설명력은 낮다 (McFadden R² 0.016, AUC 0.59): 개인 예측이 아니라 차이의 방향과 크기를 보는 모형", "Logistic regression (controls: first channel, age, line, first month): 7+ vs 1 item OR 1.37 (95% CI 1.35–1.40), adjusted repurchase 33.5% → 40.8% · store vs online first purchase OR 1.34. Low explanatory power (McFadden R² 0.016, AUC 0.59): not a model of individuals"));
}

{
  const s = content(T("3 · 발견 4 — 2020년 일시 폐쇄 때의 채널 이동 (RQ2.1)", "3 · FINDING 4 — CHANNEL MOVES IN THE 2020 SHUTDOWN (RQ2.1)"), T("일시 폐쇄 때 매장 고객은 온라인으로 옮기지 않고 기다렸다", "In the 2020 shutdown, store customers did not go online"), T("재개장 후 = 2020-06-01 ~ 09-22 · 기준선 = 1년 앞당겨 같은 방식으로 정의한 그룹의 2019-06-01 ~ 09-22 · C2_U4_ChannelShift · 계산: 부록 H", "After reopening = 2020-06-01 to 09-22 · baseline = groups defined the same way a year earlier, buying 2019-06-01 to 09-22 · C2_U4_ChannelShift · method: Appendix H"), "f5");
  tags(s, ["data", "asm"]);
  method(s, T("전년 동기 비교(단순화한 이중차분): 폐쇄 전 채널 유형별 고객의 폐쇄 중·재개장 후 구매율을, 1년 앞당겨 같은 방식으로 정의한 그룹과 비교", "Prior-year comparison (simplified difference-in-differences): buying during closures and after reopening, by channel type before closures, against groups defined the same way a year earlier"));
  card(s, MX, 1.95, 3.9, 2.0);
  txt(s, "19.8%", { x: MX + 0.3, y: 2.1, w: 3.3, h: 0.85, fontSize: 44, bold: true, color: RED, fontFace: "+mn-lt" });
  txt(s, T("폐쇄 전 매장 전용 고객 중 폐쇄 기간에 온라인으로 산 비율", "of pre-closure store-only customers bought online during the closures"), { x: MX + 0.3, y: 3.0, w: 3.3, h: 0.8, fontSize: 13 });
  card(s, MX, 4.15, 3.9, 2.0);
  txt(s, "77%", { x: MX + 0.3, y: 4.3, w: 3.3, h: 0.85, fontSize: 44, bold: true, color: INK, fontFace: "+mn-lt" });
  txt(s, T("재개장 후 이들의 구매 중 여전히 매장에서 산 비율", "of their purchases after reopening were still in stores"), { x: MX + 0.3, y: 5.2, w: 3.3, h: 0.8, fontSize: 13 });
  const cats = [T("매장 전용", "Store only"), T("온라인 전용", "Online only"), T("옴니", "Omni")];
  s.addChart(pres.charts.BAR, [{ name: T("1년 전 같은 기간", "Same period a year earlier"), labels: cats, values: [47.3, 44.5, 80.3] }, { name: T("재개장 후 다시 구매", "Bought again after reopening"), labels: cats, values: [55.4, 44.9, 79.9] }], chartBase({ x: 4.85, y: 1.85, w: 7.88, h: 3.9, barDir: "col", barGapWidthPct: 70, chartColors: [G3, RED], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", showLegend: true, legendPos: "t", legendFontSize: 11, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 95, showTitle: true, title: T("폐쇄 전 채널 유형별 재개장 후 구매율 (%)", "Bought after reopening, by channel type before closures (%)") }));
  txt(s, [{ text: T("시사점: ", "Implication: "), options: { bold: true } }, { text: T("매장 전용 고객은 온라인으로 가지 않고 재개장을 기다렸다(전년보다 8.1%p 더 돌아옴). ", "store-only customers did not go online; they waited for reopening (8.1 pp more came back than a year earlier)."), options: { breakLine: true } }, mk("asm"), { text: T("데이터에는 개별 매장 폐점이 없다. 재개장이 예정된 전면 폐쇄였으므로, 영구 폐점에서도 같다는 것은 가정이다.", "the data have no individual store closures. This was a temporary, chain-wide shutdown, so assuming the same for permanent closures is an assumption."), options: { color: G1 } }], { x: 4.85, y: 5.85, w: 7.88, h: 0.95, fontSize: 12.5 });
  testline(s, MX, 6.25, 3.9, 0.7, T("카이제곱 χ²(2) = 51,121, Cramér’s V = 0.28 · 재개장 후 +8.1%p (95% CI 7.8–8.4). 두 해 그룹에 같은 고객 6.7만 명이 겹쳐 구간은 근사치", "Chi-square χ²(2) = 51,121, V = 0.28 · reopening +8.1 pp (95% CI 7.8–8.4); 67k customers are in both groups, so approximate"));
}


sec(T("Part 4 해결과 한계", "Part 4 Solution and limits"));
divider("PART 4", T("해결과 한계", "Solution and limits"), T("발견마다 하나씩 제안하고, 효과의 크기와 이 분석이 말할 수 없는 것을 정리한다.", "One proposal per finding, the size of the effect, and what this analysis cannot say."), "part4",
  T("마지막 파트는 해결과 한계입니다. 발견마다 제안을 하나씩 만들고, 효과의 크기를 재고, 이 분석이 말할 수 없는 것을 솔직하게 정리했습니다.", "The last part is the solution and its limits: one proposal per finding, the size of the prize, and an honest list of what the analysis cannot say."));
STEP = "해결";
{
  const s = content(T("4 · 제안", "4 · PROPOSALS"), T("발견마다 하나씩, 대상과 시점까지 정한 세 가지 제안", "Three proposals, one per finding, each with a target and timing"), T("괄호 = 근거가 된 발견 (A, B = 부록의 보조 분석) · 지표 기준선은 2019–20 표본", "Brackets = supporting findings (A, B = supporting analyses in the appendix) · metric baselines come from the 2019–20 sample"), "proposal");
  const P = [
    [T("두 번째 구매 유도", "Prompt a second purchase"), T("개인화 추천, 기한 있는 혜택", "Personalised picks, time-limited offer"), T("아직 안 돌아온 신규 고객", "New customers not yet back"), T("첫 구매 후 30–60일", "Days 30–60 after first purchase"), T("90일이 지나면 30일 내 복귀 확률 10.6% → 6.8% → 3.6% (1, 2)", "After day 90 the 30-day return chance falls 10.6% → 6.8% → 3.6% (1, 2)"), T("90일 재구매율", "90-day repurchase rate")],
    [T("첫 장바구니 키우기", "Grow the first basket"), T("코디 번들, 무료배송 기준", "Outfit bundles, free-shipping threshold"), T("첫 구매 고객", "First-time buyers"), T("첫 구매 시점", "At the first purchase"), T("1개 32.4% → 7개 이상 40.7%, 90·365일 모두 순서 유지 (3)", "1 item 32.4% → 7+ items 40.7%; order holds at 90 and 365 days (3)"), T("첫 장바구니 상품 수, 90일 재구매율", "First-basket items; 90-day rate")],
    [T("폐점 전 두 채널 전환", "Convert to two channels before closing"), T("앱 가입, 클릭앤콜렉트, 매장 반품", "App sign-up, click-and-collect, in-store returns"), T("폐점 예정 매장의 매장 전용 고객, 65세 이상 우선", "Store-only customers of stores due to close; 65+ first"), T("폐점 3–6개월 전", "3–6 months before closing"), T("일시 폐쇄 때 19.8%만 온라인 구매 (4) · 한 채널 고객은 구매 횟수를 통제해도 휴면율이 약 5%p 높다 (A, B)", "Only 19.8% bought online in the shutdown (4); single-channel lapse is about 5 pp higher even after controlling purchases (A, B)"), T("폐점 후 12개월 잔존율", "12-month retention after closing")],
  ];
  tags(s, ["data", "asm"]);
  const L = [T("대상", "Target"), T("시점", "Timing"), T("근거", "Evidence"), T("지표", "Metric")];
  P.forEach((p, i) => {
    const x = MX + i * 4.14;
    card(s, x, 1.9, 3.85, 4.1);
    s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 2.1, w: 0.55, h: 0.55, fill: { color: RED }, line: { type: "none" } });
    txt(s, String(i + 1), { x: x + 0.3, y: 2.1, w: 0.55, h: 0.55, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle" });
    txt(s, p[0], { x: x + 1.0, y: 2.1, w: 2.65, h: 0.6, fontSize: 16, bold: true, valign: "middle" });
    txt(s, p[1], { x: x + 0.3, y: 2.85, w: 3.3, h: 0.5, fontSize: 12, color: G1, italic: true });
    let y = 3.35;
    [p[2], p[3], p[4], p[5]].forEach((v, j) => {
      const h = j === 2 ? 1.0 : 0.6;
      txt(s, [{ text: L[j] + "  ", options: { bold: true, color: RED } }, { text: v }], { x: x + 0.3, y, w: 3.3, h, fontSize: 12 });
      y += h + 0.05;
    });
  });
  txt(s, [{ text: T("공통 원칙: ", "Common rule: "), options: { bold: true } }, { text: T("근거가 상관관계이고, ③은 일시 폐쇄 결과가 영구 폐점에도 맞는다는 가정 위에 있다. 그래서 무작위 대조군을 둔 A/B 테스트로 효과를 재고, 확인된 것만 확대한다.", "the evidence is correlational, and ③ assumes the shutdown result holds for permanent closures. So each starts as an A/B test with a random control group, and only what works is scaled.") }], { x: MX, y: 6.15, w: CW, h: 0.6, fontSize: 13 });
}
{
  const s = content(T("4 · 기대 효과", "4 · EXPECTED IMPACT"), T("두 번째 구매 한 번이 첫해 가치를 2.7배로 만든다", "One second purchase makes first-year value 2.7 times higher"), T("2019-03 ~ 09 신규 코호트 292,217명 (365일 관측 가능) · 전체 = 신규 첫해 가치 변화 × 28.4% · 이번 발표를 위해 전체 거래로 계산", "New cohorts 2019-03 to 09, 292,217 customers observable for 365 days · total = change in first-year value × 28.4% · computed on all transactions"), "impact");
  tags(s, ["data", "est", "asm"]);
  s.addChart(pres.charts.BAR, hiBars([T("90일 안에 돌아옴", "Came back within 90 days"), T("안 돌아옴", "Did not come back")], [0.49, 0.18], [0]), chartBase({ x: MX, y: 1.85, w: 5.2, h: 3.4, barDir: "col", barOverlapPct: 100, barGapWidthPct: 70, chartColors: [G3, RED], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.00;;;", dataLabelFontSize: 14, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 0.6, showTitle: true, title: T("신규 고객 첫해 가치 (상대값)", "New-customer first-year value (relative)") }));
  txt(s, T("첫 구매 금액은 거의 같다 (0.113 vs 0.103). 차이는 두 번째 구매에서 온다.", "Their first purchase was almost the same (0.113 vs 0.103); the gap comes from the second purchase."), { x: MX, y: 5.35, w: 5.2, h: 0.7, fontSize: 13, color: G1 });
  txt(s, [mk("est"), { text: T("90일 재구매율을 올리면", "If 90-day repurchase rises by") }], { x: 6.3, y: 1.95, w: 6.4, h: 0.4, fontSize: 16, bold: true });
  table(s, [
    [T("시나리오", "Scenario"), T("신규 첫해 가치", "New-customer first-year value"), T("표본 전체 가치", "Total sample value")],
    ["+1%p".replace("%p", T("%p", " pp")), "+1.0%", T("약 +0.3%", "about +0.3%")],
    ["+3%p".replace("%p", T("%p", " pp")), "+3.1%", { text: T("약 +0.9%", "about +0.9%"), options: { bold: true, color: RED } }],
    [T("+6%p (2019-09 수준 회복)", "+6 pp (back to 2019-09 level)"), "+6.1%", T("약 +1.7%", "about +1.7%")],
  ], { x: 6.3, y: 2.45, w: 6.43, colW: [2.6, 2.0, 1.83], fontSize: 13, rowH: 0.5 });
  txt(s, [{ text: "28.4%  ", options: { bold: true, color: RED, fontSize: 20 } }, { text: T("표본의 최근 1년 가치 중 2019-03 이후 처음 산 고객의 몫. 표본 비율이라 H&M 그룹 매출과 직접 비교하지 않는다.", "share of the sample’s last-year value from customers first seen from 2019-03. A sample ratio, so not compared directly with H&M group sales.") }], { x: 6.3, y: 4.65, w: 6.43, h: 0.8, fontSize: 13 });
  txt(s, [mk("asm"), { text: T("상한 추정: ", "Upper bound: "), options: { bold: true } }, { text: T("혜택으로 돌아온 고객은 스스로 온 고객보다 덜 살 수 있고, 표본 비율을 그룹에 적용하는 것도 가정이다. 실제 크기는 A/B 테스트로 잰다.", "customers brought back by an offer may buy less than those who return on their own, and applying sample ratios to the group is an assumption. An A/B test measures the real size.") }], { x: 6.3, y: 5.6, w: 6.43, h: 0.95, fontSize: 12, color: G1 });
}
{
  const s = content(T("4 · 결론 한 장", "4 · CONCLUSION ON ONE PAGE"), T("가장 뚜렷한 신호는 신규 고객이 두 번째로 덜 온다는 것이다", "The clearest signal: new customers come back less"), T("효과는 표본 기준 상한 추정 · 출처: H&M FY2021–25 연간실적, Kaggle 거래 전체", "Impact is an upper-bound estimate on the sample · Sources: H&M FY2021–25 full-year reports; all Kaggle transactions"), "exec");
  const rows = [
    [T("상황", "Situation"), T("H&M 매출은 3년째 정체(−1%, 1%, 2%)인데 매장은 700곳 줄었고 2026년에 약 160곳을 더 닫는다.", "H&M sales have been flat for three years (−1%, 1%, 2%), it has 700 fewer stores, and it will close about 160 more in 2026.")],
    [T("문제", "Problem"), T("코로나 전에도 신규 고객 90일 재구매가 43% → 31%로 낮아졌다(보수적으로 −5%p). 2020년 일시 폐쇄 때 매장 고객의 80%는 온라인에서 사지 않았다.", "Before COVID, new-customer 90-day repurchase fell 43% → 31% (conservatively −5 pp), and 80% of store customers did not buy online in the 2020 shutdown.")],
    [T("제안", "Proposal"), T("① 첫 구매 후 30–60일 두 번째 구매 유도  ② 첫 장바구니 키우기  ③ 폐점 전 매장 고객을 두 채널 고객으로 전환. 효과는 아직 가설이라 모두 A/B 테스트로 시작.", "① Prompt a second purchase 30–60 days after the first  ② Grow the first basket  ③ Convert store customers to two channels before closing. The effects are hypotheses, so each starts as an A/B test.")],
    [T("효과", "Impact"), T("90일 재구매 +3%p → 신규 고객 첫해 가치 +3%, 표본 전체 가치 약 +0.9% (상한). 금액과 비용은 A/B 테스트로 잰다.", "+3 pp on 90-day repurchase → +3% first-year value from new customers, about +0.9% of sample value (upper bound). Money and cost are measured in an A/B test.")],
  ];
  const rowTags = [["data"], ["data"], ["asm"], ["est", "asm"]];
  rows.forEach((r, i) => {
    const y = 1.95 + i * 1.18;
    s.addShape(pres.shapes.LINE, { x: MX, y, w: CW, h: 0, line: { color: i === 0 ? INK : LINE, width: i === 0 ? 1.25 : 0.75 } });
    rowTags[i].forEach((k, j) => pill(s, k, MX, y + 0.58 + j * 0.32));
    txt(s, r[0], { x: MX, y: y + 0.18, w: 1.9, h: 0.5, fontSize: 16, bold: true, color: RED });
    txt(s, r[1], { x: MX + 2.1, y: y + 0.18, w: CW - 2.1, h: 0.9, fontSize: 14, color: INK, lineSpacingMultiple: 1.1 });
  });
  s.addShape(pres.shapes.LINE, { x: MX, y: 1.95 + 4 * 1.18, w: CW, h: 0, line: { color: INK, width: 1.25 } });
}
{
  const s = content(T("4 · 한계", "4 · LIMITS"), T("이 분석이 말할 수 없는 것", "What this analysis cannot say"), T("전체 목록: analysis/hm_eda_results.xlsx Z_Limitations 시트 · 부록 참고", "Full list: analysis/hm_eda_results.xlsx, Z_Limitations sheet · see appendix"), "limits");
  const L = [
    [T("표본이 온라인에 쏠림", "Sample leans online"), T("수준 수치를 H&M 전체로 일반화할 수 없다", "Levels cannot be generalised to all of H&M"), T("H&M 내부 전체 데이터", "H&M internal full data")],
    [T("2020-09 이후 데이터 없음", "Nothing after 2020-09"), T("지금도 같은 메커니즘인지 확인되지 않았다", "Not confirmed that the mechanism still holds"), T("최신 코호트로 재검증", "Re-test on recent cohorts")],
    [T("가격이 변환값", "Prices are transformed"), T("금액 단위 ROI를 바로 계산할 수 없다", "No ROI in currency directly"), T("보고서 수치로 환산 (가정)", "Convert with report figures (assumption)")],
    [T("상관관계 결과", "Correlational results"), T("옴니, 장바구니, 뉴스레터 효과를 인과로 말할 수 없다", "No causal claims on omni, basket or newsletter"), T("A/B 테스트", "A/B tests")],
    [T("계절 효과를 배제 못 함", "Seasonality not ruled out"), T("깨끗한 신규 코호트가 2019-03 ~ 11 한 해뿐이라, 하락이 추세인지 계절인지 가를 수 없다", "Clean new cohorts cover one year (2019-03 to 11), so trend and season cannot be separated"), T("다음 해 같은 달 코호트와 비교", "Compare with the same months a year later")],
    [T("전체 고객 재방문은 그대로", "All-customer repeat held"), T("전체 고객의 90일 재구매는 10–12월 기준 전년과 비슷하다(73–75%). 약해진 것은 신규 고객이다", "All-customer 90-day repeat matched the prior year in Oct–Dec (73–75%); the weakness is in new customers"), T("유입과 유지의 크기를 내부 데이터로 분해", "Split acquisition vs retention with internal data")],
  ];
  L.forEach((l, i) => {
    const x = MX + (i % 3) * 4.1, y = 1.9 + Math.floor(i / 3) * 2.45;
    card(s, x, y, 3.93, 2.3);
    txt(s, l[0], { x: x + 0.25, y: y + 0.2, w: 3.45, h: 0.4, fontSize: 15, bold: true });
    txt(s, l[1], { x: x + 0.25, y: y + 0.68, w: 3.45, h: 0.95, fontSize: 12, color: G1 });
    txt(s, [{ text: T("보완  ", "Close it  "), options: { bold: true, color: RED } }, { text: l[2] }], { x: x + 0.25, y: y + 1.68, w: 3.45, h: 0.5, fontSize: 11.5 });
  });
}
STEP = null;
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: section });
  bleed(s, "closing", 24);
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: 0.47, w: 0.12, h: 0.12, fill: { color: RED }, line: { type: "none" } });
  photoCredit(s, "closing", 7.5, SW - 7.5 - 0.25, "8A8A8D");
  s.addText(T("결론", "CONCLUSION"), { placeholder: "eyebrow" });
  s.addText(T("H&M은 고객을 데려오고도 붙잡지 못하고 있다.\n두 번째 구매를 되찾는 것이 가장 먼저 시험할 성장 레버다.", "H&M brings customers in but does not keep them.\nWinning back the second purchase is the first growth lever to test."), { placeholder: "title" });
  const acts = [
    [T("첫 90일", "First 90 days"), T("30–60일째 두 번째 구매 유도", "Prompt a second purchase at days 30–60")],
    [T("첫 장바구니", "First basket"), T("번들과 무료배송 기준으로 크게", "Grow it with bundles and a shipping threshold")],
    [T("폐점 전", "Before closing"), T("매장 고객을 두 채널 고객으로", "Turn store customers into two-channel customers")],
  ];
  acts.forEach((a, i) => {
    const x = MX + i * 4.14;
    s.addShape(pres.shapes.LINE, { x, y: 3.95, w: 3.8, h: 0, line: { color: "4A4A4D", width: 1 } });
    txt(s, String(i + 1).padStart(2, "0"), { x, y: 4.1, w: 1, h: 0.6, fontSize: 28, bold: true, color: RED, fontFace: "+mn-lt" });
    txt(s, a[0], { x, y: 4.75, w: 3.8, h: 0.45, fontSize: 18, bold: true, color: WHITE });
    txt(s, a[1], { x, y: 5.22, w: 3.8, h: 0.9, fontSize: 14, color: "C9C9CB" });
  });
  txt(s, T("모든 제안은 A/B 테스트로 시작한다. 데이터가 알려 주는 것은 어디에 실험을 걸지다.", "Every proposal starts as an A/B test. The data tells us where to place the experiments."), { x: MX, y: 6.35, w: CW, h: 0.4, fontSize: 13, color: "A0A0A3" });
  notes(s, T("=마무리입니다. H&M의 문제는 고객을 데려오지 못하는 것이 아니라 데려온 고객이 두 번째로 오지 않는 것입니다. 해야 할 일은 세 가지입니다. 첫 90일 안에, 특히 30일에서 60일 사이에 두 번째 구매를 유도하고, 첫 장바구니를 키우고, 매장을 닫기 전에 매장 고객을 두 채널 고객으로 바꿔 두는 것입니다. 세 가지 모두 근거가 상관관계이므로 A/B 테스트로 시작해 효과가 확인된 것만 확대하자는 것이 우리의 제안입니다. 질문 받겠습니다.", "=To close. H&M’s problem is not failing to bring customers in; it is that those customers do not come back for a second purchase. Three things to do: prompt a second purchase inside the first 90 days, especially between day 30 and day 60; grow the first basket; and turn store customers into two-channel customers before a store closes. All three rest on correlation, so we propose starting each as an A/B test and scaling only what works. We are happy to take questions."));
}
sec(T("부록", "Appendix"));
{
  const s = pres.addSlide({ masterName: "SECTION", sectionTitle: section });
  s.addText(T("부록", "Appendix"), { placeholder: "num" });
  s.addText(T("데이터와 방법론 상세", "Data and method details"), { placeholder: "title" });
  s.addText(T("A RQ별 답 · B 정정 사항 · C 데이터 출처 · D 스키마 · E 데이터 딕셔너리 · F 데이터 품질 · G 주류 방법론과 사용한 방법 · H 숫자별 계산 방법 · I 분석 절차 · J 출처 · K–Q 본편에서 뺀 슬라이드 (정의, 방법 점검, 보조 A·B, 실행 순서, 피드백 반영, 시간 차)", "A Answers by RQ · B Corrections · C Data sources · D Schema · E Data dictionary · F Data quality · G Standard methods vs ours · H How each number was computed · I Analysis process · J References"), { placeholder: "desc" });
  notes(s, "appendix");
}
{
  const s = content(T("부록 A · RQ별 답", "APPENDIX A · ANSWERS BY RQ"), T("여섯 개 연구 질문과 데이터가 준 답", "Six research questions and what the data answered"), T("출처: Kaggle H&M Personalized Fashion Recommendations 거래 전체 (2018-09-20 ~ 2020-09-22), analysis/hm_eda_results.xlsx", "Source: all Kaggle H&M Personalized Fashion Recommendations transactions (2018-09-20 to 2020-09-22), analysis/hm_eda_results.xlsx"), "summary");
  table(s, [
    ["RQ", T("질문", "Question"), T("답 (전체 데이터)", "Answer (full data)")],
    ["1.1", T("신규 고객이 다시 사는가", "Do new customers buy again?"), T("90일 재구매 43.4% (2019-03) → 31.0% (2019-11), 코로나 전부터 하락", "90-day repurchase 43.4% (2019-03) → 31.0% (2019-11), falling before COVID")],
    ["1.2", T("언제 돌아오는가", "When do they come back?"), T("90일 안에 35.8% 복귀, 이후 다음 30일 복귀 확률 10.6% → 3.5%", "35.8% return within 90 days; next-30-day chance then falls 10.6% → 3.5%")],
    ["1.3", T("무엇이 재구매를 가르는가", "What separates those who return?"), T("첫 장바구니가 클수록 꾸준히 높음 (1개 32.4% → 7개 이상 40.7%), 품목군 순위는 바뀜", "Bigger first basket, steadily higher (1 item 32.4% → 7+ 40.7%); product-group ranking shifts")],
    ["2.1", T("매장이 닫히면 온라인으로 가는가", "Do customers move online when stores close?"), T("매장 전용 고객 중 19.8%만 온라인 구매, 재개장 후 55.4% 재구매 (전년 47.3%)", "Only 19.8% of store-only customers bought online; 55.4% bought after reopening (47.3% a year earlier)")],
    ["2.2", T("채널 유형별 가치", "Value by channel type"), T("고객당 가치 옴니 1.24, 온라인 전용 0.37, 매장 전용 0.20 (상관)", "Value per customer: omni 1.24, online only 0.37, store only 0.20 (correlation)")],
    ["2.3", T("어느 연령이 매장에 의존하나", "Which ages rely most on stores?"), T("65세 이상 36.6%로 최고, 55–64세(32.5%)는 16–24세(33.2%)보다 낮음", "65+ highest at 36.6%; 55–64 (32.5%) below 16–24 (33.2%)")],
  ], { colW: [0.7, 3.6, 7.833], fontSize: 12, rowH: 0.62 });
}
{
  const s = content(T("부록 B · 제출본(Phase 1–3) 정정 사항", "APPENDIX B · CORRECTIONS TO PHASES 1–3"), T("보고서 원문과 원자료로 다시 확인해 고칠 것", "Rechecked against the reports and the raw data"), T("그 외: Phase 1 일부 수치는 앞 100만 행(22일) 기준 → 전체로 교체 · Ladieswear 37.7% · Step 3 RQ1.3 항목 빈칸 · 결측 나이 라벨 통일", "Also: Phase 1 figures from the first 1M rows (22 days) → full data · Ladieswear 37.7% · empty RQ1.3 list in Step 3 · one missing-age label"), "corrections");
  table(s, [
    [T("항목", "Item"), T("제출본", "Submitted"), T("정정", "Corrected"), T("근거", "Evidence")],
    [T("매장·시장 수", "Stores and markets"), T("FY25와 2026-08 수치 혼재", "FY25 and Aug 2026 mixed"), T("FY25: 4,101개, H&M 브랜드 3,660개, 매장 81 · 온라인 61개 시장", "FY25: 4,101 stores; H&M brand 3,660; 81 store / 61 online markets"), T("FY2025 연간실적", "FY2025 full-year report")],
    [T("공식 온라인 비중", "Reported online share"), "26–30%", T("14.5% (FY18) ~ 28% (FY20), FY19 미기재", "14.5% (FY18) to 28% (FY20); not stated for FY19"), T("연간·분기 보고서", "Full-year and quarterly reports")],
    [T("55세 이상 매장 의존", "55+ rely on stores"), T("55–64세 포함", "Includes 55–64"), T("65세 이상만 뚜렷", "Only 65+ stands out"), T("전체 거래 재계산", "Full transaction data")],
    [T("가격 범위", "Price range"), T("대부분 0.01–0.50", "Mostly 0.01–0.50"), T("대부분 0.10 이하 (p99 0.100)", "Mostly below 0.10 (p99 0.100)"), T("전체 거래", "Full transaction data")],
    [T("변수명", "Variable name"), "index_name", T("index_group_name (Sport 포함 5개)", "index_group_name (five values incl. Sport)"), "articles.csv"],
    [T("온라인 주문 금액 근거", "Online order value"), T("매출 비중 > 거래 비중", "Revenue share > volume share"), T("주문당 상품 수 4.09 vs 2.55가 주 근거", "Main reason: 4.09 vs 2.55 items per order"), "C1_07_Basket"],
  ], { colW: [2.3, 2.6, 4.6, 2.633], fontSize: 12, rowH: 0.62 });
}
{
  const s = content(T("부록 C · 데이터 출처", "APPENDIX C · DATA SOURCES"), T("행동은 Kaggle에서, 맥락은 보고서에서", "Behaviour from Kaggle, context from reports"), T("kaggle.com/competitions/h-and-m-personalized-fashion-recommendations · hmgroup.com 투자자 보고서 (저장소 data/hm/reports)", "kaggle.com/competitions/h-and-m-personalized-fashion-recommendations · hmgroup.com investor reports (repo data/hm/reports)"), "sources");
  const cols = [
    [T("Kaggle H&M 거래 데이터", "Kaggle H&M transactions"), [T("H&M이 2022년 추천 대회용으로 공개한 회원 거래 표본", "Member sample H&M released for a 2022 recommendation competition"), T("2018-09-20 ~ 2020-09-22, 734일, 일 단위", "2018-09-20 to 2020-09-22, 734 days, daily"), T("거래 31,788,324행 · 고객 1,371,980명 · 상품 105,542개", "31,788,324 transactions · 1,371,980 customers · 105,542 articles"), T("볼 수 있음: 재구매, 간격, 장바구니, 채널", "Shows: repurchase, gaps, baskets, channels"), T("볼 수 없음: 실제 금액, 국가, 매장 위치, 반품, 2020-09 이후", "Cannot show: real money, country, store location, returns, after 2020-09"), T("이용 조건: 비상업적 학술·교육 목적만, 원자료 재배포 금지", "Terms: non-commercial academic and education use only; no redistribution")]],
    [T("H&M 공식 보고서 43건", "43 official H&M reports"), [T("연차보고서 8 · 연간실적 8 · 분기보고서 27 (PDF 원문)", "8 annual · 8 full-year · 27 quarterly reports (original PDFs)"), T("FY2018 ~ FY2026 9개월 (회계연도 12월 ~ 11월)", "FY2018 to FY2026 nine months (fiscal year Dec–Nov)"), T("그룹 전체 수치: 매출 성장률, 매장 수, 온라인 비중, 회원 수", "Group figures: sales growth, stores, online share, members"), T("볼 수 있음: 2023–2026년의 정체와 매장 축소", "Shows: 2023–2026 stall and store cuts"), T("볼 수 없음: 고객 개인 행동, 재구매, 세그먼트", "Cannot show: individual behaviour, repurchase, segments")]],
  ];
  cols.forEach((c, i) => {
    const x = MX + i * 6.17;
    card(s, x, 1.9, 5.96, 3.75);
    txt(s, c[0], { x: x + 0.3, y: 2.1, w: 5.4, h: 0.45, fontSize: 18, bold: true, color: i === 0 ? INK : RED });
    txt(s, c[1].map((b, j) => ({ text: b, options: { bullet: true, breakLine: j < c[1].length - 1, paraSpaceAfter: 8 } })), { x: x + 0.3, y: 2.7, w: 5.4, h: 2.85, fontSize: 14 });
  });
  txt(s, [{ text: T("설계 원칙: ", "Design rule: "), options: { bold: true } }, { text: T("고객 행동의 메커니즘은 Kaggle에서, 문제의 크기와 현재성은 보고서에서 가져온다. 한쪽 수치로 다른 쪽을 대신하지 않는다.", "the mechanism comes from Kaggle; the size and recency of the problem from the reports. Neither substitutes for the other.") }], { x: MX, y: 5.95, w: CW, h: 0.6, fontSize: 14 });
}
{
  const s = content(T("부록 D · 스키마", "APPENDIX D · SCHEMA"), T("거래 1행 = 상품 1개, 두 차원 테이블과 N:1로 연결", "One row = one item, linked N:1 to two tables"), T("출처: analysis/hm_data_dictionary.csv, analysis/hm_data_inventory.md", "Source: analysis/hm_data_dictionary.csv, analysis/hm_data_inventory.md"), "schema");
  const B = [
    ["customers", T("1행 = 등록 고객 · 1,371,980행 · 7열", "1 row = customer · 1,371,980 rows · 7 cols"), "customer_id (PK)\nage · club_member_status\nfashion_news_frequency\nFN · Active · postal_code", G1],
    ["transactions_train", T("1행 = 상품 1개 구매 · 31,788,324행 · 5열", "1 row = one item bought · 31,788,324 rows · 5 cols"), T("t_dat (날짜, 시각 없음)\ncustomer_id (FK)\narticle_id (FK)\nprice (변환값)\nsales_channel_id (1, 2)", "t_dat (date, no time)\ncustomer_id (FK)\narticle_id (FK)\nprice (transformed)\nsales_channel_id (1, 2)"), RED],
    ["articles", T("1행 = 상품 · 105,542행 · 25열", "1 row = article · 105,542 rows · 25 cols"), T("article_id (PK)\nproduct_group_name\nindex_name · index_group_name\ngarment_group_name 외", "article_id (PK)\nproduct_group_name\nindex_name · index_group_name\ngarment_group_name and more"), G1],
  ];
  const xs = [MX, 4.85, 9.1], ws = [3.63, 3.63, 3.63];
  B.forEach((b, i) => {
    card(s, xs[i], 1.95, ws[i], 2.75, { fill: WHITE, line: b[3], lineW: 1.5 });
    txt(s, b[0], { x: xs[i] + 0.25, y: 2.1, w: ws[i] - 0.5, h: 0.4, fontSize: 16, bold: true, color: b[3] === RED ? RED : INK, fontFace: "Courier New" });
    txt(s, b[1], { x: xs[i] + 0.25, y: 2.55, w: ws[i] - 0.5, h: 0.55, fontSize: 11, color: G1 });
    txt(s, b[2], { x: xs[i] + 0.25, y: 3.1, w: ws[i] - 0.5, h: 1.5, fontSize: 12, lineSpacingMultiple: 1.15 });
  });
  [[4.23, "1 : N"], [8.48, "N : 1"]].forEach(([x, l]) => {
    s.addShape(pres.shapes.LINE, { x, y: 3.5, w: 0.62, h: 0, line: { color: G2, width: 1.5 } });
    txt(s, l, { x: x - 0.1, y: 3.05, w: 0.82, h: 0.35, fontSize: 11, bold: true, color: G1, align: "center" });
  });
  card(s, MX, 5.0, CW, 1.4);
  txt(s, [{ text: T("파생 테이블 (분석이 실제로 쓰는 단위): ", "Derived tables (the units the analysis uses): "), options: { bold: true } }, { text: T("구매 기회 = 고객 × 날짜 (9,080,179건) → 고객 단위 요약 (첫 구매일, 채널 유형, 재구매 여부). 같은 날 같은 상품을 여러 개 사면 행이 반복되고(수량 열 없음), article_id는 앞자리 0을 살리려고 문자로 읽는다.", "occasion = customer × day (9,080,179) → customer-level summary (first purchase date, channel type, repurchase). Buying the same item twice in a day repeats the row (no quantity column); article_id is read as text to keep its leading zero.") }], { x: MX + 0.3, y: 5.15, w: CW - 0.6, h: 1.15, fontSize: 13 });
}
{
  const s = content(T("부록 E · 데이터 딕셔너리", "APPENDIX E · DATA DICTIONARY"), T("열마다 함정이 있고, 해석 규칙을 먼저 정했다", "Every column has a trap; we set reading rules first"), T("전체 딕셔너리: analysis/hm_data_dictionary.csv (37열, 한·영 설명, 결측률, 고유값 수, 사용처)", "Full dictionary: analysis/hm_data_dictionary.csv (37 columns, Korean and English, missing rates, distinct counts, usage)"), "dictionary");
  table(s, [
    [T("열", "Column"), T("의미", "Meaning"), T("함정", "Trap"), T("해석 규칙", "Reading rule")],
    ["t_dat", T("구매 날짜", "Purchase date"), T("시각 없음, 첫·끝 달은 일부", "No time; first and last months partial"), T("고객 × 날짜 = 구매 기회", "customer × day = occasion")],
    ["customer_id", T("익명 고객 키", "Anonymous customer key"), T("한 계정을 여럿이 쓸 수 있음", "One account may be shared"), T("고객 단위 집계의 키", "Key for customer totals")],
    ["price", T("변환된 가격", "Transformed price"), T("실제 통화 아님", "Not real currency"), T("비율과 변화로만 해석", "Ratios and changes only")],
    ["sales_channel_id", T("판매 채널 1, 2", "Channel 1, 2"), T("공식 정의 없음", "No official definition"), T("2 = 온라인, 1 = 매장 (가정)", "2 = online, 1 = store (assumed)")],
    ["age", T("등록 나이", "Registered age"), T("1.2% 결측", "1.2% missing"), T("16–99세, 결측은 별도 라벨", "16–99 only; missing labelled")],
    ["club_member_status", T("회원 상태", "Membership status"), T("시점 모르는 스냅샷", "Snapshot of unknown date"), T("보조 지표, 상관만", "Supporting only; correlation")],
    ["fashion_news_frequency", T("뉴스레터 구독", "Newsletter"), T("시점 모르는 스냅샷", "Snapshot of unknown date"), T("보조 지표, 상관만", "Supporting only; correlation")],
    ["index_group_name", T("상위 라인 5개", "Five top-level lines"), T("index_name(10개)과 혼동", "Confused with index_name (10)"), T("라인 비중 (Ladieswear 37.7%)", "Line shares (Ladieswear 37.7%)")],
    ["product_group_name", T("상품군", "Product group"), T("첫 장바구니에 여러 군 섞임", "First basket can mix groups"), T("첫 장바구니의 주 상품군", "Main group of first basket")],
  ], { colW: [2.75, 2.4, 3.4, 3.583], fontSize: 11, rowH: 0.46 });
}
{
  const s = content(T("부록 F · 데이터 품질", "APPENDIX F · DATA QUALITY"), T("발견한 문제와 각각의 처리", "Problems found and how each was handled"), T("전체 거래로 재계산 · analysis/hm_eda_results.xlsx Z_Limitations 시트", "Recomputed on all transactions · analysis/hm_eda_results.xlsx, Z_Limitations sheet"), "quality");
  table(s, [
    [T("점검", "Check"), T("발견", "Finding"), T("처리", "Handling")],
    [T("가격 분포", "Price spread"), T("99%가 0.10 이하 (p1 0.004, 최대 0.59), 9.9%는 0.01 미만", "99% at or below 0.10 (p1 0.004, max 0.59); 9.9% below 0.01"), T("금액이 아닌 비율·변화로 비교", "Compare ratios and changes, not amounts")],
    [T("채널 의미", "Channel meaning"), T("값 1, 2뿐. 매장 폐쇄 달(2020-04)에 채널 2가 100%", "Only 1 and 2; channel 2 is 100% in April 2020, when stores were shut"), T("2 = 온라인으로 가정하고 근거 명시", "Assume 2 = online and state the evidence")],
    [T("나이", "Age"), T("1.2% 결측, 21세와 51세에 봉우리", "1.2% missing; peaks at 21 and 51"), T("16–99세만, 결측은 따로 표시", "16–99 only; missing shown separately")],
    [T("우편번호", "Postcode"), T("한 코드가 120,303개 계정에 붙음 (플레이스홀더)", "One code on 120,303 accounts (placeholder)"), T("지역 분석에서 제외", "Excluded from regional analysis")],
    [T("관측 시작", "Start of data"), T("2018-09-20 이전 이력 없음", "No history before 2018-09-20"), T("신규 = 2019-03-01 이후 첫 구매", "New = first purchase from 2019-03-01")],
    [T("관측 끝", "End of data"), T("2020-09-22 이후 없음", "Nothing after 2020-09-22"), T("N일 관측 가능 고객만 + Kaplan–Meier", "Observable-for-N-days only + Kaplan–Meier")],
    [T("표본 추출", "Sampling"), T("앞 100만 행 = 22일치 (2018-09-20 ~ 10-11)", "First 1M rows = 22 days (2018-09-20 to 10-11)"), { text: T("전체 3,179만 행으로 재계산", "Recomputed on all 31.8M rows"), options: { bold: true, color: RED } }],
  ], { colW: [2.0, 5.6, 4.533], fontSize: 12, rowH: 0.56 });
}
{
  const s = content(T("부록 G · 주류 방법론과 사용한 방법", "APPENDIX G · STANDARD METHODS VS OURS"), T("질문마다 표준 방법을 놓고, 쓸지 말지를 이유와 함께 정했다", "Standard methods, and why we used them or not"), T("참고: Kaplan & Meier (1958) · Fader, Hardie & Lee (2005), Marketing Science 24(2) · Hughes (1994) RFM", "References: Kaplan & Meier (1958) · Fader, Hardie & Lee (2005), Marketing Science 24(2) · Hughes (1994) RFM"), "methods");
  table(s, [
    [T("질문 유형", "Question type"), T("주류 방법론", "Standard method"), T("사용한 방법", "What we used"), T("선택 이유", "Why")],
    [T("재구매 추이", "Repurchase trend"), T("코호트 리텐션 분석", "Cohort retention analysis"), T("첫 구매 월 코호트별 30·90·365일 재구매율", "30/90/365-day repurchase by first-purchase month"), T("정의가 투명하고 바로 읽힘", "Clear definition; easy to read")],
    [T("재구매까지 시간", "Time to repurchase"), T("생존분석: Kaplan–Meier, Cox", "Survival analysis: Kaplan–Meier, Cox"), T("KM 곡선 + 다음 30일 재구매 확률", "KM curve + next-30-day return chance"), T("아직 안 온 고객을 버리지 않음", "Keeps customers not yet back")],
    [T("고객 가치 예측", "Value forecasting"), "BTYD: BG/NBD, Pareto/NBD", T("사용 안 함 (확장 과제)", "Not used (extension)"), T("목적은 진단, 가격이 변환값", "Aim is diagnosis; prices transformed")],
    [T("세분화", "Segmentation"), T("RFM, 군집분석", "RFM, clustering"), T("사전 정의 그룹 비교", "Predefined group comparisons"), T("연구 질문에 직접 대응", "Maps to the RQs")],
    [T("폐쇄의 영향", "Effect of closures"), T("이중차분(DiD), 대조군", "Difference-in-differences"), T("전년 같은 달 기준선과 비교", "Prior-year same-month baseline"), T("무작위 배정 불가, 계절성 통제", "No randomisation; controls season")],
    [T("매출 변화 원인", "Cause of sales change"), T("요인 분해", "Factor decomposition"), T("고객 × 빈도 × 장바구니 × 단가", "customers × frequency × basket × price"), T("어느 요인이 하락을 이끄는지", "Shows which factor drives it")],
    [T("재구매 요인", "Drivers of repurchase"), T("로지스틱 회귀 (요인 통제)", "Logistic regression (controls)"), T("요인별 구간 비교", "Comparison by segment"), T("상관관계로만 표시", "Reported as correlation only")],
  ], { colW: [2.2, 3.2, 3.6, 3.133], fontSize: 12, rowH: 0.58 });
}
{
  const s = content(T("부록 H · 숫자별 계산 방법", "APPENDIX H · HOW EACH NUMBER WAS COMPUTED"), T("발견마다 누구를, 어떤 공식으로, 왜 그렇게 셌나", "For each finding: who was counted, with what formula, and why"), T("같은 고객의 같은 날 거래 = 구매 1회 · 신규 = 첫 구매 2019-03-01 이후 · 데이터 끝 2020-09-22 · 코드: analysis/hm_eda_cycle2.py, hm_profile.py", "Same customer, same day = one purchase · new = first purchase on or after 2019-03-01 · data end 2020-09-22 · code: analysis/hm_eda_cycle2.py, hm_profile.py"), "calc");
  table(s, [
    [T("발견", "Finding"), T("누구를 셌나", "Who was counted"), T("공식", "Formula"), T("왜 이 방법 · 쓰지 않은 대안", "Why this method · alternatives not used")],
    [T("1 재구매율", "1 Repurchase"), T("신규 고객 중 첫 구매 후 N일이 데이터 안에 드는 고객 (2019-03 코호트 90일: 51,185명)", "New customers whose first N days fall inside the data (2019-03 cohort, 90 days: 51,185)"), T("N일 안에 두 번째 구매가 있는 고객 ÷ 관측 가능 고객", "customers with a 2nd purchase within N days ÷ observable customers"), T("아직 안 온 최근 고객을 이탈로 세지 않음. 1차의 달력 월 코호트(M+k)는 관측 기간이 고르지 않아 N일 기준으로 바꿈", "Recent customers not yet back are not counted as lost. Calendar-month cohorts (M+k) give uneven windows, so we switched to N days")],
    [T("2 생존곡선", "2 Survival"), T("같은 신규 고객 전원. 안 돌아온 고객은 2020-09-22에서 절단", "All the same new customers; those not back are censored at 2020-09-22"), T("S(t) = Π(1 − dᵢ ÷ nᵢ)\n다음 30일 복귀 = 1 − S(t+30) ÷ S(t)", "S(t) = Π(1 − dᵢ ÷ nᵢ)\nnext 30 days = 1 − S(t+30) ÷ S(t)"), T("Kaplan–Meier: 최근 고객도 버리지 않음. Cox 회귀·BG/NBD는 쓰지 않음 (목적이 예측이 아닌 진단)", "Kaplan–Meier keeps recent customers. Cox and BG/NBD not used: the aim is diagnosis, not forecasting")],
    [T("3 첫 장바구니", "3 First basket"), T("같은 신규 고객, 첫 구매일 상품 수 1 / 2–3 / 4–6 / 7+", "Same new customers, items on the first day: 1 / 2–3 / 4–6 / 7+"), T("구간별 90일 재구매율", "90-day repurchase by band"), T("다른 요인을 회귀로 통제하지 않아 상관관계로 표시", "No regression controls, so reported as correlation")],
    [T("4 일시 폐쇄", "4 Shutdown"), T("2019-09-20 ~ 2020-02-29 채널로 나눈 고객 (매장만 191,328명)", "Customers grouped by channel, 2019-09-20 to 2020-02-29 (store only: 191,328)"), T("폐쇄(03-15 ~ 05-31) 중 온라인 구매율 · 재개장 후(06-01 ~ 09-22) 구매율 vs 1년 전 같은 방식", "online buying in closures (03-15 to 05-31) · buying after reopening (06-01 to 09-22) vs the same a year earlier"), T("전년 동기 비교 = 단순화한 이중차분. 대조 시장이 없어 인과 추정은 아님", "Prior-year comparison = simplified DiD. No control market, so not causal")],
    [T("A 휴면", "A Lapse"), T("첫해(2018-09-20 ~ 2019-09-19) 채널 유형별 고객", "Customers by year-1 channel type (2018-09-20 to 2019-09-19)"), T("둘째 해 구매가 없는 고객 ÷ 첫해 고객", "no purchase in year 2 ÷ year-1 customers"), T("영구 이탈은 관측할 수 없어 ‘휴면’으로 정의. 상관관계", "Permanent loss cannot be observed, hence ‘lapsed’. Correlation")],
    [T("B 매장 비중", "B Store share"), T("전체 거래 행, 나이 없는 행(0.4%) 제외", "All transaction rows, excluding rows with no age (0.4%)"), T("연령대별 채널 1 행 ÷ 그 연령대 전체 행", "channel-1 rows ÷ all rows, by age band"), T("행 기준이라 많이 사는 고객의 비중이 큼. 고객별 평균이면 25–34세 31.4% (행 기준 25.2%). 65세 이상이 가장 높은 것은 같음", "Row-based, so heavy buyers weigh more. Averaged per customer, 25–34 is 31.4% (25.2% by row); 65+ is highest either way")],
  ], { colW: [1.45, 3.1, 3.3, 4.283], fontSize: 10, rowH: 0.7 });
}
{
  const s = content(T("부록 I · 분석 절차", "APPENDIX I · ANALYSIS PROCESS"), T("두 번의 사이클: 넓게 훑고, 질문을 좁혀 깊게 판다", "Two cycles: scan widely, then narrow the question and dig deep"), "Tukey (1977) · Chapman et al. (2000) CRISP-DM · Peng & Matsui (2015) · Gelman & Loken (2013) · Kerr (1998)", "process");
  const st = [[T("읽기", "Read"), T("스키마, 딕셔너리, 품질", "Schema, dictionary, quality")], [T("정의", "Define"), T("구매 기회, 신규, 재구매, 채널", "Occasion, new, repurchase, channel")], [T("사이클 1", "Cycle 1"), T("기초 표 14개", "14 base tables")], [T("질문 통합", "Merge"), T("이상 신호 → 심화 9개", "Signals → 9 topics")], [T("사이클 2", "Cycle 2"), T("심화 분석 U1–U9", "Deep dives U1–U9")], [T("좁히기", "Narrow"), T("핵심 4 + 보조 2만 남김", "Keep 4 core + 2 supporting")], [T("검증", "Verify"), T("재계산, 보고서 대조, 계보표", "Recompute, check, lineage")]];
  st.forEach((p, i) => {
    const x = MX + i * 1.745, hl = i === 2 || i === 4;
    card(s, x, 1.95, 1.62, 1.75, hl ? { fill: WHITE, line: i === 4 ? RED : INK, lineW: 1.5 } : {});
    txt(s, `${i + 1}  ${p[0]}`, { x: x + 0.13, y: 2.1, w: 1.4, h: 0.4, fontSize: 13, bold: true, color: i === 4 ? RED : INK });
    txt(s, p[1], { x: x + 0.13, y: 2.55, w: 1.4, h: 1.05, fontSize: 11, color: G1 });
  });
  const B = [
    [T("왜 두 사이클인가", "Why two cycles"), T("Tukey의 탐색적 자료분석, CRISP-DM의 반복 루프, Peng & Matsui의 ‘에피사이클’은 모두 같은 구조다: 기대를 세우고, 데이터와 비교하고, 기대를 고친다.", "Tukey’s exploratory analysis, the CRISP-DM loop and Peng & Matsui’s “epicycles” share one structure: set expectations, compare with data, revise.")],
    [T("갈림길의 함정을 막는 장치", "Guarding against forking paths"), T("정의와 연구 질문을 결과 전에 고정, 탐색 결과는 가설로만 표시, 모든 수치에 코드·시트 계보를 남김 (Gelman & Loken 2013, Kerr 1998).", "Definitions and RQs fixed before results; exploratory patterns labelled as hypotheses; code and sheet lineage for every figure (Gelman & Loken 2013; Kerr 1998).")],
  ];
  B.forEach((b, i) => {
    const x = MX + i * 6.17;
    txt(s, b[0], { x, y: 4.05, w: 5.9, h: 0.45, fontSize: 17, bold: true });
    txt(s, b[1], { x, y: 4.55, w: 5.9, h: 2.0, fontSize: 14, color: G1 });
  });
}
{
  const s = content(T("부록 J · 출처", "APPENDIX J · REFERENCES"), T("데이터, 방법론, 저작권, 재현 경로", "Data, methods, rights and how to reproduce"), T("H&M 상표는 H&M의 자산이며, 이 자료는 H&M과 무관한 비상업적 학생 과제입니다.", "H&M is a trademark of H&M. This is non-commercial student coursework, not affiliated with H&M."), "refs");
  txt(s, T("데이터", "Data"), { x: MX, y: 1.9, w: 5.6, h: 0.35, fontSize: 15, bold: true, color: RED });
  txt(s, T("H&M Group (2022). H&M Personalized Fashion Recommendations. Kaggle. 이용 조건: 비상업적 학술·교육 목적, 원자료 재배포 금지.\nH&M Group. 연차보고서 FY2018–25, 연간실적 FY2018–25, 분기보고서 FY2018 3M – FY2026 9M.", "H&M Group (2022). H&M Personalized Fashion Recommendations. Kaggle. Terms: non-commercial academic and education use; no redistribution.\nH&M Group. Annual reports FY2018–25, full-year reports FY2018–25, quarterly reports FY2018 3M to FY2026 9M."), { x: MX, y: 2.3, w: 5.6, h: 1.8, fontSize: 12, paraSpaceAfter: 6 });
  txt(s, T("재현과 저작권", "Reproduce and rights"), { x: MX, y: 4.2, w: 5.6, h: 0.35, fontSize: 15, bold: true, color: RED });
  txt(s, T("저장소 analysis/: hm_eda_cycle1.py, hm_eda_cycle2.py, hm_eda_results.xlsx (L_Lineage 시트에 수치별 계보).\n차트는 모두 직접 계산해 다시 그렸다. H&M 로고·사진·전용 글꼴은 쓰지 않았다. 포인트 컬러 #E30415는 FY2025 연차보고서 로고에서 추출했다.\n사진: Unsplash 라이선스 (무료, 출처 표기 선택) — Bernd Dittrich, Tim Mossholder, Kiko Camaclang, Andrej Lišakov, Ashim D’Silva, Charlota Blunarova. 흑백 변환·자르기만 했다.", "Repo analysis/: hm_eda_cycle1.py, hm_eda_cycle2.py, hm_eda_results.xlsx (L_Lineage traces each figure).\nAll charts are our own calculations. No H&M logo, photos or proprietary fonts are used. Accent #E30415 is sampled from the FY2025 annual report logo.\nPhotos: Unsplash License (free; credit optional) — Bernd Dittrich, Tim Mossholder, Kiko Camaclang, Andrej Lišakov, Ashim D’Silva, Charlota Blunarova. Cropped and converted to black and white only."), { x: MX, y: 4.6, w: 5.6, h: 2.25, fontSize: 11.5, paraSpaceAfter: 6 });
  txt(s, T("방법론", "Methods"), { x: 6.6, y: 1.9, w: 6.1, h: 0.35, fontSize: 15, bold: true, color: RED });
  const refs = ["Kaplan, E. L. & Meier, P. (1958). JASA 53(282), 457–481.", "Fader, P., Hardie, B. & Lee, K. L. (2005). Marketing Science 24(2), 275–286.", "Shadish, W., Cook, T. & Campbell, D. (2002). Experimental and Quasi-Experimental Designs.", "Tukey, J. W. (1977). Exploratory Data Analysis.", "Chapman, P. et al. (2000). CRISP-DM 1.0.", "Peng, R. & Matsui, E. (2015). The Art of Data Science.", "Gelman, A. & Loken, E. (2013). The garden of forking paths.", "Kerr, N. L. (1998). HARKing. PSPR 2(3), 196–217.", "Hughes, A. M. (1994). Strategic Database Marketing."];
  txt(s, refs.map((r, i) => ({ text: r, options: { breakLine: i < refs.length - 1, paraSpaceAfter: 4 } })), { x: 6.6, y: 2.3, w: 6.13, h: 4.4, fontSize: 11.5 });
}

{
  const s = content(T("부록 K · 정의: 이렇게 셌다", "APPENDIX K · DEFINITIONS: HOW WE COUNTED"), T("발견을 읽기 전에: 무엇을 한 번의 구매, 재구매, 장바구니로 셌나", "Before the findings: what counts as a repurchase and a basket"), T("코드: analysis/hm_eda_common.py, hm_eda_cycle1.py, hm_eda_cycle2.py · 왼쪽·오른쪽 절단 처리는 Part 3", "Code: analysis/hm_eda_common.py, hm_eda_cycle1.py, hm_eda_cycle2.py · left and right censoring: see Part 3"), "units");
  const F = [[T("원자료 행 = 상품 1개", "Raw row = one item"), "31.8M", INK], [T("구매 기회 = 고객 × 날짜", "Occasion = customer × day"), "9.08M", RED], [T("구매 고객", "Buying customers"), "1.36M", INK]];
  F.forEach((f, i) => {
    const x = MX + i * 4.14;
    card(s, x, 1.85, 3.55, 1.2, i === 1 ? { line: RED, lineW: 1.5 } : {});
    txt(s, f[0], { x: x + 0.3, y: 1.97, w: 3.0, h: 0.3, fontSize: 12, color: G1 });
    txt(s, f[1], { x: x + 0.3, y: 2.3, w: 3.0, h: 0.6, fontSize: 30, bold: true, color: f[2], fontFace: "+mn-lt" });
    if (i < 2) s.addShape(pres.shapes.CHEVRON, { x: x + 3.7, y: 2.25, w: 0.3, h: 0.4, fill: { color: G3 }, line: { type: "none" } });
  });
  const D = [
    [T("신규 고객", "New customer"), T("첫 구매가 2019-03-01 이후 (그 전 6개월 구매 없음을 확인하는 버퍼)", "first purchase on or after 2019-03-01 (a six-month buffer checks there was no earlier purchase)")],
    [T("N일 재구매율", "N-day repurchase rate"), T("첫 구매 후 N일 안에 두 번째 구매 기회가 있는 비율. 분모는 N일을 관측할 수 있는 신규 고객만", "share with a second occasion within N days of the first; the denominator is only new customers observable for N days")],
    [T("장바구니", "Basket"), T("한 구매 기회(고객 × 날짜)에 담긴 상품 수. 수량 열이 없어 같은 상품 반복 행도 1개씩 셈", "items in one occasion (customer × day); with no quantity column, repeated rows count one each")],
    [T("휴면", "Lapsed"), T("다음 12개월 동안 구매 없음. 영구 이탈 시점은 이 데이터로 알 수 없다", "no purchase in the next 12 months. When a customer is lost for good cannot be seen in this data")],
    [T("채널 유형", "Channel type"), T("매장 전용 · 온라인 전용 · 옴니(둘 다). 채널 2 = 온라인은 가정", "store only · online only · omni (both). Channel 2 = online is an assumption")],
    [T("매장 폐쇄", "Store closure"), T("2020-03 ~ 05 코로나 일시·전면 폐쇄만. 개별 매장 폐점은 데이터에 없다", "only the temporary, chain-wide 2020-03 to 05 shutdown. Individual store closures are not in the data")],
    [T("가치", "Value"), T("price의 합. 변환된 상대값이라 비율로만 비교하며, 이익·마진이 아니다", "sum of price; transformed and relative, compared as ratios only. Not profit or margin")],
    [T("연령대", "Age bands"), T("16–24, 25–34, 35–44, 45–54, 55–64, 65+ (나이 결측 1.2%는 별도)", "16–24, 25–34, 35–44, 45–54, 55–64, 65+ (1.2% with no age kept apart)")],
  ];
  D.forEach((d, i) => {
    const x = MX + (i % 2) * 6.17, y = 3.35 + Math.floor(i / 2) * 0.88;
    txt(s, [{ text: d[0] + "  ", options: { bold: true, color: RED } }, { text: d[1] }], { x, y, w: 5.9, h: 0.8, fontSize: 13 });
  });
}
{
  const s = content(T("부록 L · 방법 점검: 절단·민감도·타당성", "APPENDIX L · METHOD CHECK: CENSORING, SENSITIVITY, VALIDITY"), T("하락은 버퍼를 늘려도 남지만 크기는 5–12%p 범위다", "The drop survives a longer buffer, but its size is 5–12 pp"), T("민감도 분석은 이번 발표를 위해 전체 거래로 재계산 · 코호트 n = 25,060 ~ 51,185 · 타당성 유형: Shadish, Cook & Campbell (2002)", "Sensitivity recomputed on all transactions for this deck · cohort n = 25,060 to 51,185 · validity types: Shadish, Cook & Campbell (2002)"), ["censoring", "validity"]);
  tags(s, ["data", "est"]);
  txt(s, T("신규 고객 버퍼에 따른 90일 재구매 하락", "90-day repurchase drop by new-customer buffer"), { x: MX, y: 1.9, w: 5.6, h: 0.35, fontSize: 14, bold: true });
  table(s, [
    [T("버퍼 (첫 코호트)", "Buffer (first cohort)"), T("첫 코호트", "First cohort"), "2019-11", T("변화", "Change")],
    [T("6개월 (2019-03, 기본)", "6 months (2019-03, default)"), "43.4%", "31.0%", T("−12.4%p", "−12.4 pp")],
    [T("12개월 (2019-09, 민감도)", "12 months (2019-09, sensitivity)"), "35.8%", "31.0%", { text: T("−4.8%p", "−4.8 pp"), options: { bold: true, color: RED } }],
  ], { x: MX, y: 2.35, w: 5.6, colW: [2.3, 1.1, 1.1, 1.1], fontSize: 12, rowH: 0.5 });
  txt(s, T("왼쪽 절단(오래 쉬던 기존 고객이 신규로 보임)은 6개월 버퍼로, 오른쪽 절단(아직 안 왔을 뿐)은 관측 가능 고객 제한과 Kaplan–Meier로 다뤘다. 2019년 봄 코호트는 6월 세일 효과도 받을 수 있어, 보수적 추정은 −5%p다. 끝점은 90일 창이 폐쇄 전에 끝나는 2019-11 코호트다.", "Left censoring (lapsed customers looking new) is handled by the six-month buffer; right censoring (not back yet) by observable-only populations and Kaplan–Meier. Spring 2019 cohorts may also catch the June sale, so the conservative estimate is −5 pp. The endpoint is 2019-11, the last cohort whose window ends before the closures."), { x: MX, y: 4.05, w: 5.6, h: 1.9, fontSize: 12, color: G1 });
  table(s, [
    [T("타당성", "Validity"), T("처리", "What we did"), T("남은 위험", "Remaining risk")],
    [T("외적", "External"), T("수준 대신 방향, 크기는 보고서", "Direction, not level; size from reports"), { text: T("높음: 온라인 쏠림", "High: online skew"), options: { bold: true, color: RED } }],
    [T("시간적", "Temporal"), T("작업 가설 + 반증 조건", "Working hypothesis + rejection rule"), { text: T("높음: 코로나 후 변화", "High: post-COVID shift"), options: { bold: true, color: RED } }],
    [T("구성", "Construct"), T("폐쇄 달 채널 2 = 100% 확인, 가격은 비율만", "Channel 2 = 100% in closure month; price as ratios"), T("중간", "Medium")],
    [T("내적", "Internal"), T("버퍼, 관측 가능 고객, KM, 전년 기준선", "Buffer, observable-only, KM, prior-year baseline"), T("중간", "Medium")],
    [T("통계적", "Statistical"), T("코호트 2.5만–5만, 표준오차 약 0.3%p", "Cohorts 25k–50k; SE about 0.3 pp"), T("낮음", "Low")],
    [T("인과", "Causal"), T("상관으로만 서술, A/B 제안", "Correlation only; A/B proposed"), T("중간", "Medium")],
  ], { x: 6.6, y: 1.9, w: 6.13, colW: [1.2, 3.13, 1.8], fontSize: 11, rowH: 0.52 });
  txt(s, [{ text: T("핵심: ", "Key point: "), options: { bold: true } }, { text: T("표본이 커서 우연은 문제가 아니다. 문제는 편향이고, 대수의 법칙은 편향을 줄여 주지 않는다.", "with a sample this large, chance is not the problem; bias is. The law of large numbers does not remove bias.") }], { x: 6.6, y: 5.85, w: 6.13, h: 0.8, fontSize: 13 });
}
{
  const s = content(T("부록 M · 보조 A — 한 채널 고객의 휴면 (RQ2.2)", "APPENDIX M · SUPPORTING A — SINGLE-CHANNEL CUSTOMERS LAPSE (RQ2.2)"), T("한 채널 고객이 더 휴면하지만, 대부분은 적게 사서다", "Single-channel lapse is mostly about buying less"), T("휴면 = 관측 첫해 채널 유형별로 둘째 해 구매 없음 · 가치 = 전 기간 채널 유형 기준 · C1_06_ChannelType · C2_U4_ChannelShift · 계산: 부록 H", "Lapsed = no purchase in year 2, by year-1 channel type · value = channel type over the full period · C1_06_ChannelType · C2_U4_ChannelShift · method: Appendix H"), "f4");
  tags(s, ["data"]);
  method(s, T("고객 이동 분석 + 이진 로지스틱 회귀: 첫해 채널 유형별 이듬해 휴면 여부를, 첫해 구매 횟수·관측 개월·나이를 통제해 비교", "Customer flow + binary logistic regression: year-2 lapse by year-1 channel type, controlling year-1 purchases, months observed and age"));
  const cards = [
    [T("매장 전용", "Store only"), "47.4%", "0.20", RED],
    [T("온라인 전용", "Online only"), "48.2%", "0.37", RED],
    [T("두 채널 (옴니)", "Both channels (omni)"), "11.4%", "1.24", INK],
  ];
  cards.forEach((c, i) => {
    const x = MX + i * 4.14;
    card(s, x, 1.95, 3.85, 2.75);
    txt(s, c[0], { x: x + 0.3, y: 2.15, w: 3.3, h: 0.35, fontSize: 15, bold: true, color: G1 });
    txt(s, c[1], { x: x + 0.3, y: 2.6, w: 3.3, h: 0.9, fontSize: 48, bold: true, color: c[3], fontFace: "+mn-lt" });
    txt(s, T("이듬해 구매 없음", "bought nothing the next year"), { x: x + 0.3, y: 3.55, w: 3.3, h: 0.3, fontSize: 12, color: G1 });
    txt(s, T("고객당 가치(전 기간) ", "Value per customer (all period) ") + c[2], { x: x + 0.3, y: 4.05, w: 3.3, h: 0.35, fontSize: 13, bold: true });
  });
  txt(s, [{ text: T("옴니 고객은 35.5%지만 가치의 ", "Omni customers are 35.5% of customers but ") }, { text: "67.7%", options: { bold: true } }, { text: T("를 만든다. 차이는 방문 횟수(13.0회 vs 약 3회)에서 온다. 매장 전용에서 옴니로 바뀐 고객은 가치 +79%, 매장 전용에 머문 고객은 −19%.", " of value. The gap comes from visits (13.0 vs about 3). Store-only customers who became omni: value +79%; those who stayed store only: −19%.") }], { x: MX, y: 5.0, w: CW, h: 0.8, fontSize: 15 });
  testline(s, MX, 5.85, CW, 0.9, T("통제 전 휴면 오즈비는 약 7 (옴니 11.4% vs 한 채널 47–48%). 첫해 구매 횟수·관측 개월·나이를 통제하면 오즈비 1.32–1.37 (95% CI 1.30–1.40), 조정 휴면율 32.5% vs 37.1–37.7%. 차이 36%p 중 약 5%p만 채널에 남는다 → 제안 ③의 효과는 작게 잡고 A/B 테스트로 확인한다. 휴면이지 영구 이탈은 아니다.", "Before controls the lapse odds ratio is about 7 (omni 11.4% vs single-channel 47–48%). Controlling year-1 purchases, months observed and age: OR 1.32–1.37 (95% CI 1.30–1.40), adjusted lapse 32.5% vs 37.1–37.7%. Only about 5 of the 36 points stay with the channel → size proposal ③ small and test it. Lapsed, not lost for good."));
}
{
  const s = content(T("부록 N · 보조 B — 누구를 먼저 지킬 것인가 (RQ2.3)", "APPENDIX N · SUPPORTING B — WHOM TO PROTECT FIRST (RQ2.3)"), T("65세 이상이 매장 비중이 가장 높지만, 연령 차이 자체는 작다", "65+ relies most on stores, but age differences are small"), T("거래 행 기준, 나이 없는 행(0.4%) 제외 · 고객별 평균으로 내면 25–34세 31.4% · analysis/hm_profile.py · 계산: 부록 H", "By transaction row, excluding rows with no age (0.4%) · averaged per customer, 25–34 is 31.4% · analysis/hm_profile.py · method: Appendix H"), "f6");
  tags(s, ["data"]);
  method(s, T("비중 분석 + 일원 분산분석: 연령대별 매장(채널 1) 구매 비중. 막대는 거래 행 기준, 검정은 고객별 비중 기준", "Share analysis + one-way ANOVA: in-store (channel 1) share by age band. Bars by transaction row; the test uses each customer’s share"));
  const ages = ["16–24", "25–34", "35–44", "45–54", "55–64", "65+"];
  s.addChart(pres.charts.BAR, hiBars(ages, [33.2, 25.2, 27.8, 33.3, 32.5, 36.6], [5]), chartBase({ x: MX, y: 1.85, w: 7.0, h: 4.6, barDir: "col", barOverlapPct: 100, barGapWidthPct: 50, chartColors: [G3, RED], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0;;;", valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 42, showTitle: true, title: T("연령대별 매장 구매 비중 (거래 행 기준, %)", "In-store share by age band (transaction rows, %)") }));
  const pts = [
    ["65+", T("매장 비중 36.6%로 최고. 품목당 18.8% 더 비싸게 사지만, 고객당 가치는 0.41로 25–34세(0.83)의 절반", "highest in-store share at 36.6%; pays 18.8% more per item, yet value per customer is 0.41, half of 25–34 (0.83)"), RED],
    ["55–64", T("32.5%로 16–24세(33.2%), 45–54세(33.3%)보다 낮다. “55세 이상이 매장에 의존”은 지지되지 않는다", "32.5%, below 16–24 (33.2%) and 45–54 (33.3%). “Shoppers 55+ rely on stores” is not supported"), INK],
    [T("규모", "Scale"), T("16–34세가 나이를 아는 구매 고객의 55.3%", "ages 16–34 are 55.3% of buyers with a known age"), INK],
  ];
  pts.forEach((p, i) => {
    const y = 2.1 + i * 1.45;
    txt(s, p[0], { x: 8.0, y, w: 4.7, h: 0.4, fontSize: 18, bold: true, color: p[2] });
    txt(s, p[1], { x: 8.0, y: y + 0.42, w: 4.7, h: 0.95, fontSize: 13, color: INK });
  });
  testline(s, 8.0, 6.05, 4.7, 0.85, T("일원 분산분석 F = 657, η² = 0.002: 연령이 고객별 매장 비중 차이의 0.2%만 설명. Kruskal–Wallis도 같은 결론. 표본이 커서 유의할 뿐, 실무상 작은 차이", "One-way ANOVA F = 657, η² = 0.002: age explains 0.2% of the variation in customer in-store share. Kruskal–Wallis agrees. Significant only because the sample is large; small in practice"));
}
{
  const s = content(T("부록 O · 실행 순서", "APPENDIX O · NEXT STEPS"), T("발견을 결정으로: 크기를 재고, 실험으로 확인한다", "From findings to decisions: size it, then test it"), T("Δp 시나리오 값은 가정이며 확정 수치가 아님 · Phase 4 개요: 팀 공유 Google Doc", "Scenario values are assumptions, not final figures · Phase 4 outline: shared Google Doc"), "next");
  tags(s, ["est", "asm"]);
  const steps = [
    [T("금액으로 환산", "Convert to money"), T("ΔRevenue = N(신규) × Δp(90일) × V(두 번째 구매) − 비용. 표본 비율을 매출·회원 수로 환산해 비용과 비교", "ΔRevenue = N(new) × Δp(90 days) × V(second purchase) − cost. Translate sample ratios with revenue and member counts")],
    [T("A/B 테스트 설계", "Design the A/B tests"), T("30–60일 재구매 제안, 첫 장바구니 번들. 1차 지표 90일 재구매율. 무작위 배정으로 상관과 인과를 가른다", "Offer at days 30–60 and first-basket bundles. Primary metric: 90-day repurchase. Random assignment separates correlation from cause")],
    [T("최신 데이터로 반증 시도", "Try to disprove it"), T("2023–25 코호트에서 90일 재구매가 회복됐다면 연결 가설을 기각한다", "If 90-day repurchase has recovered in 2023–25 cohorts, reject the link hypothesis")],
    [T("방법 확장", "Extend the methods"), T("BG/NBD로 고객별 예상 구매 수, Cox 모형으로 여러 요인을 함께 통제", "BG/NBD for expected purchases per customer; a Cox model to control several factors at once")],
  ];
  steps.forEach((st, i) => {
    const x = MX + i * 3.08;
    s.addShape(pres.shapes.OVAL, { x, y: 2.05, w: 0.7, h: 0.7, fill: { color: i === 1 ? RED : INK }, line: { type: "none" } });
    txt(s, String(i + 1), { x, y: 2.05, w: 0.7, h: 0.7, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle" });
    if (i < 3) s.addShape(pres.shapes.LINE, { x: x + 0.85, y: 2.4, w: 2.08, h: 0, line: { color: G3, width: 1, endArrowType: "triangle" } });
    txt(s, st[0], { x, y: 3.0, w: 2.85, h: 0.6, fontSize: 16, bold: true });
    txt(s, st[1], { x, y: 3.65, w: 2.85, h: 2.4, fontSize: 13, color: G1 });
  });
  card(s, MX, 5.95, CW, 0.75);
  txt(s, T("지금 단계의 결론은 실행 결정이 아니라 실험 결정이다. 데이터가 말해 주는 것은 어디에 실험을 걸어야 하는지다.", "Today’s conclusion is a decision to test, not to roll out. The data tells us where to place the experiments."), { x: MX + 0.3, y: 6.1, w: CW - 0.6, h: 0.5, fontSize: 14, bold: true });
}
{
  const s = content(T("부록 P · Phase 3 피드백 반영", "APPENDIX P · ACTING ON THE PHASE 3 FEEDBACK"), T("피드백의 지적과 제안을 하나씩 이렇게 반영했다", "How we acted on each point of the feedback"), T("출처: Phase 1–3 평가 의견 (45/50) · 표시 규칙은 본편 모든 분석 슬라이드 오른쪽 위에 적용", "Source: Phase 1–3 assessment (45/50) · labels appear top right on every analysis slide"), "feedback");
  table(s, [
    [T("지적", "Feedback"), T("반영", "What we changed"), T("어디서", "Where")],
    [T("표본의 온라인 비중은 H&M 전체가 아니다", "Sample online share is not H&M’s"), T("수준이 아닌 방향만 비교. 효과는 ‘표본 기준’으로 쓰고 그룹 성장률과의 직접 비교를 뺐다", "Compare direction, not level. Impact is stated ‘in the sample’; the direct comparison with group growth is removed"), T("기대 효과, 시간 차", "Impact, time gap")],
    [T("높은 단가가 높은 마진은 아니다", "Higher price is not higher margin"), T("가치 = price 합(상대값)이며 이익이 아니라고 정의. 비용·ROI는 A/B 테스트에서 측정", "Value = sum of price (relative), not profit. Cost and ROI are measured in the A/B test"), T("정의, 실행 순서", "Definitions, next steps")],
    [T("2018–20 데이터 vs 2025–26 문제", "2018–20 data vs 2025–26 problem"), T("연결은 작업 가설로 두고, 최신 코호트에서 회복했다면 기각하는 조건을 명시", "The link is a working hypothesis, rejected if recent cohorts have recovered"), T("시간 차", "Time gap")],
    [T("구매 간격으로 영구 이탈을 알 수 없다", "Purchase gaps do not show permanent loss"), T("‘이탈’ 대신 ‘휴면(이듬해 구매 없음)’. KM은 복귀 시점만 해석", "‘Lapsed’ (no purchase next year) instead of ‘churn’; KM read only as time to return"), T("정의, 발견 2, 보조 A", "Definitions, finding 2, supporting A")],
    [T("개별 매장 폐점은 식별되지 않는다", "Individual closures are not identified"), T("2020년 일시·전면 폐쇄만 분석. 영구 폐점 적용은 가정으로 표시", "Only the temporary 2020 shutdown is analysed; applying it to permanent closures is marked as an assumption"), T("발견 4, 제안 ③", "Finding 4, proposal ③")],
    [T("신규·재구매·장바구니 정의", "Define new, repurchase, basket"), T("부록에서 본편 정의 슬라이드로 올림", "Moved from the appendix to a main definitions slide"), T("Part 2 첫 장", "Start of Part 2")],
    [T("적게, 확실하게", "Fewer, well-executed analyses"), T("핵심 발견 4개 + 보조 분석 2개로 정리", "Four core findings plus two supporting analyses"), "Part 2"],
  ], { y: 1.85, colW: [3.3, 6.2, 2.633], fontSize: 11.5, rowH: 0.56 });
  txt(s, T("주장마다 근거 수준을 표시했다:", "Every claim carries its level of evidence:"), { x: MX, y: 6.42, w: 4.6, h: 0.3, fontSize: 12, bold: true, valign: "middle" });
  let x = MX + T(3.0, 3.35);
  [["data", T("데이터가 보여 준 것", "what the data show")], ["est", T("데이터로 계산한 추정", "estimated from the data")], ["asm", T("검증 안 된 가정", "untested assumption")]].forEach(([k, l]) => {
    pill(s, k, x, 6.44);
    txt(s, l, { x: x + TAG[k].w + 0.1, y: 6.42, w: 1.8, h: 0.3, fontSize: 11, color: G1, valign: "middle" });
    x += TAG[k].w + 1.95;
  });
}
{
  const s = content(T("부록 Q · 왜 믿을 수 있나: 시간 차", "APPENDIX Q · WHY TRUST IT: THE TIME GAP"), T("행동 데이터는 2020년에 끝나고, 문제는 2023년부터 보인다", "Behaviour data ends in 2020; the problem shows from 2023"), T("회계연도 = 전년 12월 ~ 11월 · 출처: H&M 연간실적·분기보고서 (analysis/hm_report_quarterly.csv), Kaggle 데이터 날짜 범위", "Fiscal year = December to November · Sources: H&M full-year and quarterly reports (analysis/hm_report_quarterly.csv), Kaggle date range"), ["timeline", "timeuse"]);
  tags(s, ["data", "asm"]);
  const fy = ["FY18", "FY19", "FY20", "FY21", "FY22", "FY23", "FY24", "FY25", "FY26"], bw = CW / 9;
  fy.forEach((f, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: MX + i * bw, y: 1.9, w: bw - 0.04, h: 0.38, fill: { color: BG2 }, line: { type: "none" } });
    txt(s, f, { x: MX + i * bw, y: 1.9, w: bw - 0.04, h: 0.38, fontSize: 11, bold: true, align: "center", valign: "middle" });
  });
  const X = (fyIdx) => MX + fyIdx * bw;
  const bar = (x0, x1, y, color, label, lc, inside) => {
    s.addShape(pres.shapes.RECTANGLE, { x: X(x0), y, w: X(x1) - X(x0), h: 0.36, fill: { color }, line: { type: "none" } });
    txt(s, label, inside ? { x: X(x0) + 0.12, y, w: X(x1) - X(x0) - 0.2, h: 0.36, fontSize: 11, color: lc, valign: "middle", bold: true } : { x: X(x1) + 0.12, y, w: 7, h: 0.36, fontSize: 11, color: lc, valign: "middle" });
  };
  bar(0.806, 2.811, 2.45, G1, T("Kaggle 거래 2018-09-20 ~ 2020-09-22", "Kaggle transactions 2018-09-20 to 2020-09-22"), INK, false);
  bar(2.25, 2.5, 2.95, RED, T("매장 폐쇄 2020-03 ~ 05: 자연 실험", "Store closures 2020-03 to 05: natural experiment"), INK, false);
  bar(0, 8.75, 3.45, G3, T("H&M 보고서 43건: FY2018 ~ FY2026 9개월", "43 H&M reports: FY2018 to FY2026 nine months"), INK, true);
  bar(5, 8, 3.95, RED, T("매출 정체 −1%, 1%, 2%", "Flat sales −1%, 1%, 2%"), WHITE, true);
  const rules = [
    [T("① 역할 분리", "① Separate roles"), T("Kaggle은 메커니즘, 보고서는 크기와 현재성. 서로 대신하지 않는다", "Kaggle gives the mechanism; reports give size and recency")],
    [T("② 달력 정렬", "② Align the calendar"), T("겹치는 7개 분기(FY19 전체 + FY20 Q1–Q3)를 회계 분기로 맞춰 비교", "Compare the seven overlapping quarters (FY19 + FY20 Q1–Q3) on fiscal quarters")],
    [T("③ 수준이 아닌 방향", "③ Direction, not level"), T("표본 온라인 70.4% vs 그룹 14.5–28%. 표본 수준을 그룹으로 옮기지 않는다", "Sample online 70.4% vs group 14.5–28%; sample levels are not carried over")],
    [T("④ 연결 가정은 명시", "④ State the bridge"), T("“2019년 약화가 2023–25 정체의 한 원인”은 가설. 최신 데이터에서 회복했다면 기각", "“2019 weakening is one cause of the 2023–25 stall” is a hypothesis, rejected if recent data shows recovery")],
  ];
  rules.forEach((r, i) => {
    const x = MX + i * 3.08;
    card(s, x, 4.65, 2.9, 2.1);
    txt(s, r[0], { x: x + 0.2, y: 4.8, w: 2.5, h: 0.4, fontSize: 14, bold: true, color: i === 3 ? RED : INK });
    txt(s, r[1], { x: x + 0.2, y: 5.25, w: 2.5, h: 1.4, fontSize: 12, color: G1 });
  });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
