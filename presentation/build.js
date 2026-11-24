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
function content(eyebrow, title, source, noteKeys) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(eyebrow, { placeholder: "eyebrow" });
  s.addText(title, { placeholder: "title" });
  if (source) s.addText(source, { placeholder: "source" });
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
sec(T("표지와 요약", "Cover and summary"));
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
{
  const s = content(T("한 장 요약", "ONE-PAGE SUMMARY"), T("문제는 유입이 아니라 유지다", "The problem is keeping customers, not finding them"), T("효과는 표본 기준 상한 추정 · 출처: H&M FY2021–25 연간실적, Kaggle 거래 전체", "Impact is an upper-bound estimate on the sample · Sources: H&M FY2021–25 full-year reports; all Kaggle transactions"), "exec");
  const rows = [
    [T("상황", "Situation"), T("H&M 매출은 3년째 정체(−1%, 1%, 2%)인데 매장은 700곳 줄었고 2026년에 약 160곳을 더 닫는다.", "H&M sales have been flat for three years (−1%, 1%, 2%), it has 700 fewer stores, and it will close about 160 more in 2026.")],
    [T("문제", "Problem"), T("코로나 전부터 돌아오는 고객이 줄었다. 신규 고객 90일 재구매 43% → 30%, 한 채널 고객의 절반은 이듬해 구매 없음, 2020년 일시 폐쇄 때 매장 고객의 80%는 온라인에서 사지 않았다.", "Returning customers fell before COVID: new-customer 90-day repurchase 43% → 30%, half of single-channel customers bought nothing the next year, and 80% of store customers did not buy online during the 2020 shutdown.")],
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

sec(T("Part 1 증상과 진단", "Part 1 Symptom and diagnosis"));
divider("PART 1", T("증상과 진단", "Symptom and diagnosis"), T("매출은 멈췄고 매장은 닫히고 있다. 숫자를 쪼개 어디서 새는지 찾는다.", "Sales have stalled and stores are closing. We break the numbers down to find the leak."), "part1",
  T("첫 번째 파트는 증상과 진단입니다. 회사 보고서가 보여 주는 증상을 먼저 보고, 매출을 요인별로 쪼개 문제가 어디에 있는지 좁혀 가겠습니다.", "Part one is the symptom and the diagnosis. First what H&M’s own reports show, then we break sales into factors to narrow down where the problem sits."));
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
  const s = content(T("1 · 문제를 어디서 찾았나", "1 · WHERE WE FOUND THE PROBLEM"), T("매출을 쪼개 내려가니, 새는 곳은 ‘돌아오는 고객’이었다", "Breaking sales down shows the leak is in returning customers"), T("가치 = 고객 수 × 고객당 방문 × 방문당 상품 수 × 상품당 가격 · 빈도는 나머지에서 역산 · C2_U1_SalesDecomp · 그룹: FY19 Q4, FY20 Q1", "Value = customers × visits per customer × items per visit × price per item · visits derived · C2_U1_SalesDecomp · group: FY19 Q4, FY20 Q1"), "diagnosis");
  tags(s, ["data"]);
  card(s, MX, 1.95, 3.3, 3.0, { fill: INK });
  txt(s, T("Kaggle 표본, 코로나 전 5개월\n(2019-10 ~ 2020-02)", "Kaggle sample, five months before COVID (2019-10 to 2020-02)"), { x: MX + 0.3, y: 2.2, w: 2.7, h: 0.7, fontSize: 12, color: "C9C9CB" });
  txt(s, "−7.5%", { x: MX + 0.3, y: 2.95, w: 2.7, h: 0.9, fontSize: 48, bold: true, color: WHITE, fontFace: "+mn-lt" });
  txt(s, T("가치, 전년 같은 달 대비\n같은 기간 그룹 매출은 +5%", "value vs a year earlier;\ngroup sales +5% in the same months"), { x: MX + 0.3, y: 3.95, w: 2.7, h: 0.8, fontSize: 12, color: "C9C9CB" });
  txt(s, "=", { x: 4.05, y: 3.05, w: 0.4, h: 0.6, fontSize: 30, color: G2, align: "center" });
  const boxes = [
    [T("구매 고객 수", "Buying customers"), "−4.3%", T("→ 누가 안 돌아오나?", "→ who stopped coming back?"), true],
    [T("고객당 방문 빈도", "Visits per customer"), T("약 −1%", "about −1%"), T("거의 변화 없음", "almost unchanged"), false],
    [T("방문당 상품 수", "Items per visit"), "−6.5%", T("→ 장바구니가 작아짐", "→ baskets got smaller"), true],
    [T("상품당 가격", "Price per item"), "+4.1%", T("문제 아님", "not the problem"), false],
  ];
  boxes.forEach((b, i) => {
    const x = 4.6 + (i % 2) * 4.12, y = 1.95 + Math.floor(i / 2) * 1.55;
    card(s, x, y, 3.95, 1.42, { fill: WHITE, line: b[3] ? RED : LINE, lineW: b[3] ? 1.5 : 0.75 });
    txt(s, b[0], { x: x + 0.25, y: y + 0.15, w: 3.5, h: 0.3, fontSize: 12, color: G1 });
    txt(s, b[1], { x: x + 0.25, y: y + 0.45, w: 3.5, h: 0.5, fontSize: 26, bold: true, color: b[3] ? RED : INK });
    txt(s, b[2], { x: x + 0.25, y: y + 0.98, w: 3.5, h: 0.3, fontSize: 12, color: b[3] ? INK : G2 });
  });
  card(s, MX, 5.3, 5.95, 1.3);
  card(s, 6.78, 5.3, 5.95, 1.3);
  txt(s, [{ text: T("고객 수 → ", "Customers → "), options: { bold: true } }, { text: T("신규 고객이 두 번째로 오지 않는다 (발견 1, 2), 한 채널 고객은 이듬해 구매가 끊긴다 (보조 A)", "new customers do not make a second purchase (findings 1, 2); single-channel customers lapse the next year (supporting A)") }], { x: MX + 0.25, y: 5.5, w: 5.45, h: 1.0, fontSize: 14 });
  txt(s, [{ text: T("장바구니 → ", "Basket → "), options: { bold: true } }, { text: T("첫 장바구니가 큰 고객이 더 잘 돌아온다 (발견 3)", "customers with a bigger first basket come back more often (finding 3)") }], { x: 7.03, y: 5.5, w: 5.45, h: 1.0, fontSize: 14 });
}

sec(T("Part 2 발견", "Part 2 Findings"));
divider("PART 2", T("발견: 어디서 새는가", "Findings: where customers leak"), T("핵심 발견 넷: 두 번째 구매, 첫 90일, 첫 장바구니, 2020년 일시 폐쇄. 보조 분석 둘: 채널 유형, 연령.", "Four core findings: the second purchase, the first 90 days, the first basket and the 2020 shutdown. Two supporting analyses: channel type and age."), "part2",
  T("두 번째 파트는 발견입니다. 넓게 다 답하기보다, 데이터가 확실히 받쳐 주는 네 가지 분석에 집중했습니다. 나머지 둘은 상관관계 수준이라 보조 분석으로 내렸습니다. 먼저 숫자를 어떻게 셌는지부터 정의하겠습니다.", "Part two is the findings. Rather than answer everything, we focus on four analyses the data clearly support; the other two are correlational, so we present them as supporting analyses. First, how we counted."));
{
  const s = content(T("2 · 정의: 이렇게 셌다", "2 · DEFINITIONS: HOW WE COUNTED"), T("발견을 읽기 전에: 무엇을 한 번의 구매, 재구매, 장바구니로 셌나", "Before the findings: what counts as a repurchase and a basket"), T("코드: analysis/hm_eda_common.py, hm_eda_cycle1.py, hm_eda_cycle2.py · 왼쪽·오른쪽 절단 처리는 Part 4", "Code: analysis/hm_eda_common.py, hm_eda_cycle1.py, hm_eda_cycle2.py · left and right censoring: see Part 4"), "units");
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
  const s = content(T("2 · 발견 1 — 신규 고객이 덜 돌아온다 (RQ1.1)", "2 · FINDING 1 — NEW CUSTOMERS COME BACK LESS (RQ1.1)"), T("재구매 약화는 코로나 전, 그룹 매출이 늘던 때 시작됐다", "Repurchase fell before COVID, while group sales grew"), T("365일 기준도 66.2% (2019-03) → 57.3% (2019-09) · 하락 폭은 민감도 분석상 6–14%p · C2_U2_Repurchase · 계산: 부록 H", "365-day rate also fell: 66.2% (2019-03) → 57.3% (2019-09) · size of drop 6–14 pp after sensitivity check · C2_U2_Repurchase · method: Appendix H"), "f1");
  tags(s, ["data"]);
  method(s, T("코호트 재구매율 분석: 첫 구매 월별로 고객을 묶고, 90일 안에 다시 산 고객 ÷ 첫 구매 후 90일을 다 지켜볼 수 있는 고객", "Cohort analysis: customers grouped by first-purchase month; bought again within 90 days ÷ customers observable for 90 days"));
  const labels = ["19-03", "19-04", "19-05", "19-06", "19-07", "19-08", "19-09", "19-10", "19-11", "19-12", "20-01", "20-02", "20-03", "20-04", "20-05", "20-06"];
  const v = [43.4, 43.3, 42.5, 38.4, 35.0, 34.8, 35.8, 32.5, 31.0, 29.8, 30.8, 29.8, 32.8, 32.4, 36.3, 35.2];
  const pre = v.map((x, i) => (i > 0 && i < 11 ? x : 0)), end = v.map((x, i) => (i === 0 || i === 11 ? x : 0)), cov = v.map((x, i) => (i >= 12 ? x : 0));
  s.addChart(pres.charts.BAR, [{ name: "pre", labels, values: pre }, { name: "end", labels, values: end }, { name: "covid", labels, values: cov }], chartBase({ x: MX, y: 2.2, w: CW, h: 4.0, barDir: "col", barOverlapPct: 100, barGapWidthPct: 45, chartColors: [G2, RED, "D9D9DB"], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0;;;", dataLabelFontSize: 9, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 50 }));
  txt(s, T("첫 구매 월 코호트별 90일 재구매율 (%) · 같은 기간 그룹 분기 매출 현지통화 +4 ~ +8%", "90-day repurchase rate by first-purchase month cohort (%) · group quarterly sales over the same period: +4 to +8% (local currencies)"), { x: MX, y: 1.8, w: CW, h: 0.35, fontSize: 13, color: G1 });
  txt(s, [{ text: "■ ", options: { color: G2 } }, { text: T("코로나 전 첫 구매   ", "First purchase before COVID   ") }, { text: "■ ", options: { color: RED } }, { text: T("비교 끝점 (2019-03, 2020-02)   ", "Compared endpoints (2019-03, 2020-02)   ") }, { text: "■ ", options: { color: "C4C4C6" } }, { text: T("2020-03 이후 첫 구매 (매장 폐쇄, 비교 제외)", "First purchase from 2020-03 (closures, not compared)") }], { x: MX, y: 6.35, w: CW, h: 0.35, fontSize: 11, color: G1 });
}
{
  const s = content(T("2 · 발견 2 — 기회는 첫 90일 (RQ1.2)", "2 · FINDING 2 — THE WINDOW IS THE FIRST 90 DAYS (RQ1.2)"), T("90일이 지나면 돌아올 확률이 급격히 줄어든다", "After day 90 the chance of coming back drops sharply"), T("Kaplan–Meier, 2019-03 이후 신규 고객, 15일 간격, 미복귀 고객은 관측 끝에서 절단 · C2_U2_Repurchase · 계산: 부록 H", "Kaplan–Meier, new customers from 2019-03, 15-day grid, customers not yet back censored at end of data · C2_U2_Repurchase · method: Appendix H"), "f2");
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
  const s = content(T("2 · 발견 3 — 레버는 첫 장바구니 (RQ1.3)", "2 · FINDING 3 — THE LEVER IS THE FIRST BASKET (RQ1.3)"), T("첫 장바구니 크기는 일관되고, 품목군은 기간에 따라 흔들린다", "First-basket size is consistent; product group is not"), T("2019-03 이후 신규 고객 · 품목군은 90일 관측 가능 1,000명 이상 · 수영복: 90일 1위(38.1%) → 365일 중간(61.8%) · C2_U2_Repurchase · 계산: 부록 H", "New customers from 2019-03 · product groups with 1,000+ observable at 90 days · Swimwear: 1st at 90 days (38.1%) → mid-table at 365 (61.8%) · C2_U2_Repurchase · method: Appendix H"), "f3");
  tags(s, ["data"]);
  method(s, T("세그먼트 비교: 첫 구매일에 산 상품 수로 신규 고객을 나눠 90일 재구매율을 비교. 다른 요인은 통제하지 않아 상관관계", "Segment comparison: new customers split by items bought on the first day, 90-day repurchase compared. No other factors controlled, so correlation"));
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
}
{
  const s = content(T("2 · 발견 4 — 2020년 일시 폐쇄 때의 채널 이동 (RQ2.1)", "2 · FINDING 4 — CHANNEL MOVES IN THE 2020 SHUTDOWN (RQ2.1)"), T("일시 폐쇄 때 매장 고객은 온라인으로 옮기지 않고 기다렸다", "In the 2020 shutdown, store customers did not go online"), T("재개장 후 = 2020-06-01 ~ 09-22 · 기준선 = 1년 앞당겨 같은 방식으로 정의한 그룹의 2019-06-01 ~ 09-22 · C2_U4_ChannelShift · 계산: 부록 H", "After reopening = 2020-06-01 to 09-22 · baseline = groups defined the same way a year earlier, buying 2019-06-01 to 09-22 · C2_U4_ChannelShift · method: Appendix H"), "f5");
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
}
{
  const s = content(T("2 · 보조 A — 한 채널 고객의 휴면 (RQ2.2)", "2 · SUPPORTING A — SINGLE-CHANNEL CUSTOMERS LAPSE (RQ2.2)"), T("한 채널만 쓰는 고객의 절반은 이듬해 한 번도 사지 않았다", "Half of single-channel customers bought nothing the next year"), T("휴면 = 관측 첫해 채널 유형별로 둘째 해 구매 없음 · 가치 = 전 기간 채널 유형 기준 · C1_06_ChannelType · C2_U4_ChannelShift · 계산: 부록 H", "Lapsed = no purchase in year 2, by year-1 channel type · value = channel type over the full period · C1_06_ChannelType · C2_U4_ChannelShift · method: Appendix H"), "f4");
  tags(s, ["data"]);
  method(s, T("고객 이동 분석: 같은 고객을 첫해 채널 유형(매장만·온라인만·옴니)으로 나누고, 둘째 해에 한 번도 사지 않은 비율을 셈", "Customer flow analysis: the same customers grouped by year-1 channel type (store only, online only, omni); share who bought nothing in year 2"));
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
  txt(s, T("주의: ① 휴면이지 영구 이탈이 아니다. 데이터가 끝난 뒤 돌아왔을 수 있다. ② 상관관계다. 원래 활발한 고객이 채널을 늘렸을 수 있다 → 제안 ③은 A/B 테스트로 확인한다.", "Caution: ① lapsed, not lost for good; they may have returned after the data ends. ② Correlation only: already-active customers may be the ones who added a channel → proposal ③ is tested with an A/B test."), { x: MX, y: 5.9, w: CW, h: 0.75, fontSize: 13, color: G1 });
}
{
  const s = content(T("2 · 보조 B — 누구를 먼저 지킬 것인가 (RQ2.3)", "2 · SUPPORTING B — WHOM TO PROTECT FIRST (RQ2.3)"), T("매장 의존은 U자형이고, 뚜렷한 건 65세 이상뿐이다", "Store reliance is U-shaped: only the 65+ group stands out"), T("거래 행 기준, 나이 없는 행(0.4%) 제외 · 고객별 평균으로 내면 25–34세 31.4% · analysis/hm_profile.py · 계산: 부록 H", "By transaction row, excluding rows with no age (0.4%) · averaged per customer, 25–34 is 31.4% · analysis/hm_profile.py · method: Appendix H"), "f6");
  tags(s, ["data"]);
  method(s, T("비중 분석: 연령대별 거래 행 중 매장(채널 1) 행의 비율. 거래 행 기준이라 많이 사는 고객의 비중이 큼", "Share analysis: in-store (channel 1) rows as a share of all rows, by age band. Row-based, so heavy buyers weigh more"));
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
}

sec(T("Part 3 제안", "Part 3 Proposals"));
divider("PART 3", T("제안: 빈 자리 채우기", "Proposals: three ways to fill the gap"), T("발견마다 하나씩, 대상·시점·지표를 정한 제안과 그 효과의 크기.", "One proposal per finding, each with a target, timing and metric, and the size of the prize."), "part3",
  T("세 번째 파트는 제안입니다. 앞의 발견마다 하나씩 제안을 만들었고, 효과가 어느 정도인지 크기도 재 보았습니다.", "Part three is the proposals: one for each finding, with a sizing of what they could be worth."), "6E6E70");
{
  const s = content(T("3 · 제안", "3 · PROPOSALS"), T("발견마다 하나씩, 대상과 시점까지 정한 세 가지 제안", "Three proposals, one per finding, each with a target and timing"), T("괄호 = 근거가 된 발견 (A, B = 보조 분석) · 지표 기준선은 2019–20 표본", "Brackets = supporting findings (A, B = supporting analyses) · metric baselines come from the 2019–20 sample"), "proposal");
  const P = [
    [T("두 번째 구매 유도", "Prompt a second purchase"), T("개인화 추천, 기한 있는 혜택", "Personalised picks, time-limited offer"), T("아직 안 돌아온 신규 고객", "New customers not yet back"), T("첫 구매 후 30–60일", "Days 30–60 after first purchase"), T("90일이 지나면 30일 내 복귀 확률 10.6% → 6.8% → 3.6% (1, 2)", "After day 90 the 30-day return chance falls 10.6% → 6.8% → 3.6% (1, 2)"), T("90일 재구매율", "90-day repurchase rate")],
    [T("첫 장바구니 키우기", "Grow the first basket"), T("코디 번들, 무료배송 기준", "Outfit bundles, free-shipping threshold"), T("첫 구매 고객", "First-time buyers"), T("첫 구매 시점", "At the first purchase"), T("1개 32.4% → 7개 이상 40.7%, 90·365일 모두 순서 유지 (3)", "1 item 32.4% → 7+ items 40.7%; order holds at 90 and 365 days (3)"), T("첫 장바구니 상품 수, 90일 재구매율", "First-basket items; 90-day rate")],
    [T("폐점 전 두 채널 전환", "Convert to two channels before closing"), T("앱 가입, 클릭앤콜렉트, 매장 반품", "App sign-up, click-and-collect, in-store returns"), T("폐점 예정 매장의 매장 전용 고객, 65세 이상 우선", "Store-only customers of stores due to close; 65+ first"), T("폐점 3–6개월 전", "3–6 months before closing"), T("일시 폐쇄 때 19.8%만 온라인 구매, 한 채널 고객 절반 이듬해 구매 없음 vs 옴니 11.4% (4, A, B)", "Only 19.8% bought online in the shutdown; half of single-channel customers lapse vs 11.4% of omni (4, A, B)"), T("폐점 후 12개월 잔존율", "12-month retention after closing")],
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
  const s = content(T("3 · 기대 효과", "3 · EXPECTED IMPACT"), T("두 번째 구매 한 번이 첫해 가치를 2.7배로 만든다", "One second purchase makes first-year value 2.7 times higher"), T("2019-03 ~ 09 신규 코호트 292,217명 (365일 관측 가능) · 전체 = 신규 첫해 가치 변화 × 28.4% · 이번 발표를 위해 전체 거래로 계산", "New cohorts 2019-03 to 09, 292,217 customers observable for 365 days · total = change in first-year value × 28.4% · computed on all transactions"), "impact");
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
  const s = content(T("3 · 실행 순서", "3 · NEXT STEPS"), T("발견을 결정으로: 크기를 재고, 실험으로 확인한다", "From findings to decisions: size it, then test it"), T("Δp 시나리오 값은 가정이며 확정 수치가 아님 · Phase 4 개요: 팀 공유 Google Doc", "Scenario values are assumptions, not final figures · Phase 4 outline: shared Google Doc"), "next");
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

sec(T("Part 4 왜 믿을 수 있나", "Part 4 Why trust it"));
divider("PART 4", T("왜 믿을 수 있나", "Why trust it"), T("2020년에 끝나는 데이터로 2023년의 문제를 말하는 방법, 절단과 민감도, 그리고 한계.", "How 2020 data can speak to a 2023 problem, how we handled censoring and sensitivity, and the limits."), "part4",
  T("마지막 파트는 이 결과를 왜 믿을 수 있는지입니다. 데이터의 시간 차를 어떻게 다뤘는지, 그리고 이 분석이 말할 수 없는 것을 솔직하게 정리했습니다.", "The last part is why you can trust this: how we handled the time gap in the data, and an honest list of what the analysis cannot say."));
{
  const s = content(T("4 · Phase 3 피드백 반영", "4 · ACTING ON THE PHASE 3 FEEDBACK"), T("피드백의 지적과 제안을 하나씩 이렇게 반영했다", "How we acted on each point of the feedback"), T("출처: Phase 1–3 평가 의견 (45/50) · 표시 규칙은 본편 모든 분석 슬라이드 오른쪽 위에 적용", "Source: Phase 1–3 assessment (45/50) · labels appear top right on every analysis slide"), "feedback");
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
  const s = content(T("4 · 왜 믿을 수 있나 ① 시간 차", "4 · WHY TRUST IT ① THE TIME GAP"), T("행동 데이터는 2020년에 끝나고, 문제는 2023년부터 보인다", "Behaviour data ends in 2020; the problem shows from 2023"), T("회계연도 = 전년 12월 ~ 11월 · 출처: H&M 연간실적·분기보고서 (analysis/hm_report_quarterly.csv), Kaggle 데이터 날짜 범위", "Fiscal year = December to November · Sources: H&M full-year and quarterly reports (analysis/hm_report_quarterly.csv), Kaggle date range"), ["timeline", "timeuse"]);
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
{
  const s = content(T("4 · 왜 믿을 수 있나 ② 절단·민감도·타당성", "4 · WHY TRUST IT ② CENSORING, SENSITIVITY, VALIDITY"), T("하락은 버퍼를 늘려도 남지만 크기는 6–14%p 범위다", "The drop survives a longer buffer, but its size is 6–14 pp"), T("민감도 분석은 이번 발표를 위해 전체 거래로 재계산 · 코호트 n = 25,060 ~ 51,185 · 타당성 유형: Shadish, Cook & Campbell (2002)", "Sensitivity recomputed on all transactions for this deck · cohort n = 25,060 to 51,185 · validity types: Shadish, Cook & Campbell (2002)"), ["censoring", "validity"]);
  tags(s, ["data", "est"]);
  txt(s, T("신규 고객 버퍼에 따른 90일 재구매 하락", "90-day repurchase drop by new-customer buffer"), { x: MX, y: 1.9, w: 5.6, h: 0.35, fontSize: 14, bold: true });
  table(s, [
    [T("버퍼 (첫 코호트)", "Buffer (first cohort)"), T("첫 코호트", "First cohort"), "2020-02", T("변화", "Change")],
    [T("6개월 (2019-03, 기본)", "6 months (2019-03, default)"), "43.4%", "29.8%", T("−13.6%p", "−13.6 pp")],
    [T("12개월 (2019-09, 민감도)", "12 months (2019-09, sensitivity)"), "35.8%", "29.8%", { text: T("−6.0%p", "−6.0 pp"), options: { bold: true, color: RED } }],
  ], { x: MX, y: 2.35, w: 5.6, colW: [2.3, 1.1, 1.1, 1.1], fontSize: 12, rowH: 0.5 });
  txt(s, T("왼쪽 절단(오래 쉬던 기존 고객이 신규로 보임)은 6개월 버퍼로, 오른쪽 절단(아직 안 왔을 뿐)은 관측 가능 고객 제한과 Kaplan–Meier로 다뤘다. 2019년 봄 코호트는 6월 세일 효과도 받을 수 있어, 보수적 추정은 −6%p다.", "Left censoring (lapsed customers looking new) is handled by the six-month buffer; right censoring (not back yet) by observable-only populations and Kaplan–Meier. Spring 2019 cohorts may also catch the June sale, so the conservative estimate is −6 pp."), { x: MX, y: 4.05, w: 5.6, h: 1.9, fontSize: 12, color: G1 });
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
  const s = content(T("4 · 한계", "4 · LIMITS"), T("이 분석이 말할 수 없는 것", "What this analysis cannot say"), T("전체 목록: analysis/hm_eda_results.xlsx Z_Limitations 시트 · 부록 참고", "Full list: analysis/hm_eda_results.xlsx, Z_Limitations sheet · see appendix"), "limits");
  const L = [
    [T("표본이 온라인에 쏠림", "Sample leans online"), T("수준 수치를 H&M 전체로 일반화할 수 없다", "Levels cannot be generalised to all of H&M"), T("H&M 내부 전체 데이터", "H&M internal full data")],
    [T("2020-09 이후 데이터 없음", "Nothing after 2020-09"), T("지금도 같은 메커니즘인지 확인되지 않았다", "Not confirmed that the mechanism still holds"), T("최신 코호트로 재검증", "Re-test on recent cohorts")],
    [T("가격이 변환값", "Prices are transformed"), T("금액 단위 ROI를 바로 계산할 수 없다", "No ROI in currency directly"), T("보고서 수치로 환산 (가정)", "Convert with report figures (assumption)")],
    [T("상관관계 결과", "Correlational results"), T("옴니, 장바구니, 뉴스레터 효과를 인과로 말할 수 없다", "No causal claims on omni, basket or newsletter"), T("A/B 테스트", "A/B tests")],
  ];
  L.forEach((l, i) => {
    const x = MX + (i % 2) * 6.17, y = 1.95 + Math.floor(i / 2) * 2.4;
    card(s, x, y, 5.96, 2.2);
    txt(s, l[0], { x: x + 0.3, y: y + 0.25, w: 5.4, h: 0.45, fontSize: 18, bold: true });
    txt(s, l[1], { x: x + 0.3, y: y + 0.8, w: 5.4, h: 0.6, fontSize: 14, color: G1 });
    txt(s, [{ text: T("보완  ", "Close it  "), options: { bold: true, color: RED } }, { text: l[2] }], { x: x + 0.3, y: y + 1.5, w: 5.4, h: 0.45, fontSize: 13 });
  });
}
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
  s.addText(T("A RQ별 답 · B 정정 사항 · C 데이터 출처 · D 스키마 · E 데이터 딕셔너리 · F 데이터 품질 · G 주류 방법론과 사용한 방법 · H 분석 절차 · I 출처", "A Answers by RQ · B Corrections · C Data sources · D Schema · E Data dictionary · F Data quality · G Standard methods vs ours · H Analysis process · I References"), { placeholder: "desc" });
  notes(s, "appendix");
}
{
  const s = content(T("부록 A · RQ별 답", "APPENDIX A · ANSWERS BY RQ"), T("여섯 개 연구 질문과 데이터가 준 답", "Six research questions and what the data answered"), T("출처: Kaggle H&M Personalized Fashion Recommendations 거래 전체 (2018-09-20 ~ 2020-09-22), analysis/hm_eda_results.xlsx", "Source: all Kaggle H&M Personalized Fashion Recommendations transactions (2018-09-20 to 2020-09-22), analysis/hm_eda_results.xlsx"), "summary");
  table(s, [
    ["RQ", T("질문", "Question"), T("답 (전체 데이터)", "Answer (full data)")],
    ["1.1", T("신규 고객이 다시 사는가", "Do new customers buy again?"), T("90일 재구매 43.4% (2019-03) → 29.8% (2020-02), 코로나 전부터 하락", "90-day repurchase 43.4% (2019-03) → 29.8% (2020-02), falling before COVID")],
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

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
