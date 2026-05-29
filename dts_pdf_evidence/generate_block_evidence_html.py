#!/usr/bin/env python3
import html
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "dts_pdf_evidence"
DTS = ROOT / "orig" / "linux_kernel" / "imx93-11x11-frdm.dts"
MD = OUT / "imx93_frdm_dts_pdf_evidence.md"
LINE_MATRIX = OUT / "line_matrix.tsv"
YAML = OUT / "evidence.yaml"
HTML = OUT / "block_index.html"

PDF_PATH = {
    "FRDM": "FRDM-IMX93-DESIGNFILES/PDF/SPF-94611_B2.pdf",
}
ALLOWED_PDFS = {"FRDM"}

KIND_LABEL = {
    "i2c": "I2C device",
    "pinmux": "Pinmux / signal",
    "power": "Power / regulator",
    "peripheral": "Peripheral",
}

GPIO_CHAINS = {
    ("pcal6524", "2"): [
        ("E02", "I2C2 上的 PCAL6524 GPIO expander"),
        ("E58", "DTS offset 2 = PCAL6524 P0_2，PDF net 為 PCIE_nWAKE"),
        ("E14", "此 DTS block 宣告的是 VEXP_3V3 rail；和 P0_2/PCIE_nWAKE 的鏈條不完全吻合，需人工確認"),
    ],
    ("pcal6524", "8"): [
        ("E02", "I2C2 上的 PCAL6524 GPIO expander"),
        ("E59", "DTS offset 8 = PCAL6524 P1_0，PDF net 為 EXP_PWREN"),
        ("E15", "VEXP_5V power switch/rail"),
    ],
    ("pcal6524", "13"): [
        ("E02", "I2C2 上的 PCAL6524 GPIO expander"),
        ("E60", "DTS offset 13 = PCAL6524 P1_5，PDF net 為 EXT1_PWREN"),
        ("E18", "EXT1/M.2 power path must be checked against the connector page"),
    ],
    ("pcal6524", "18"): [
        ("E02", "I2C2 上的 PCAL6524 GPIO expander"),
        ("E61", "DTS offset 18 = PCAL6524 P2_2，PDF net 為 SD3_nRST"),
        ("E18", "SD3/M.2 Wi-Fi reset path"),
    ],
    ("pcal6524", "20"): [
        ("E02", "I2C2 上的 PCAL6524 GPIO expander"),
        ("E62", "DTS offset 20 = PCAL6524 P2_4，PDF 顯示於 M.2 disable/reset group"),
        ("E18", "M.2 Key-E Wi-Fi/BT connector path"),
    ],
    ("pcal6524", "23"): [
        ("E02", "I2C2 上的 PCAL6524 GPIO expander"),
        ("E52", "DTS offset 23 = PCAL6524 P2_7，PDF net 為 CAN_STBY"),
        ("E12", "CAN transceiver standby input"),
    ],
    ("adp5585", "0"): [
        ("E57", "ADP5585 offset 0 的證據在非 FRDM PDF，已排除"),
    ],
    ("adp5585", "1"): [
        ("E54", "ADP5585 offset 1 的證據在非 FRDM PDF，已排除"),
    ],
    ("adp5585", "9"): [
        ("E56", "ADP5585 offset 9 的證據在非 FRDM PDF，已排除"),
    ],
}


def esc(text):
    return html.escape(str(text), quote=True)


def parse_evidence():
    data = yaml.safe_load(YAML.read_text())
    return {
        item["id"]: item
        for item in data["evidence"]
        if item.get("pdf") in ALLOWED_PDFS
    }


def parse_line_matrix():
    if LINE_MATRIX.exists():
        rows = {}
        for raw in LINE_MATRIX.read_text().splitlines():
            first = raw.split("\t", 1)
            if len(first) != 2 or not first[0].isdigit():
                continue
            parts = first[1].rsplit("\t", 2)
            if len(parts) != 3:
                continue
            rows[int(first[0])] = {
                "text": parts[0],
                "evidence": [part for part in parts[1].split(",") if part] or ["SW"],
                "note": parts[2],
            }
        return rows

    rows = {}
    in_matrix = False
    for line in MD.read_text().splitlines():
        if line.startswith("## Full DTS Line Coverage Matrix"):
            in_matrix = True
            continue
        if in_matrix and line.startswith("## "):
            break
        if not in_matrix or not line.startswith("| "):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) != 4 or not cols[0].isdigit():
            continue
        line_no = int(cols[0])
        evidence = re.findall(r"`(E\d+|SW|DOC)`", cols[2])
        rows[line_no] = {
            "text": re.sub(r"^`|`$", "", cols[1]),
            "evidence": evidence or ["SW"],
            "note": cols[3],
        }
    return rows


def label_from_open(line):
    label = line.split("{", 1)[0].strip()
    label = re.sub(r"\s+", " ", label)
    return label or "{"


def parse_blocks(lines):
    blocks = []
    stack = []
    for idx, line in enumerate(lines, start=1):
        code = line.split("//", 1)[0]
        opens = code.count("{")
        closes = code.count("}")
        if opens:
            for _ in range(opens):
                label = label_from_open(code)
                parent_path = stack[-1]["path"] if stack else ""
                path = f"{parent_path} / {label}" if parent_path else label
                stack.append({
                    "start": idx,
                    "label": label,
                    "path": path,
                    "depth": len(stack),
                })
        if closes:
            for _ in range(closes):
                if not stack:
                    continue
                block = stack.pop()
                block["end"] = idx
                blocks.append(block)
    blocks.sort(key=lambda b: (b["start"], -(b["end"] - b["start"])))
    return blocks


def evidence_badges(ids, evidence):
    out = []
    for eid in ids:
        if eid == "SW":
            out.append('<span class="badge sw">SW</span>')
            continue
        item = evidence.get(eid)
        if not item:
            out.append(f'<span class="badge">{esc(eid)}</span>')
            continue
        kind = item.get("kind", "peripheral")
        title = f'{eid}: {item["pdf"]} p.{item["page"]} {item["term"]}'
        out.append(f'<button class="badge {esc(kind)}" data-eid="{esc(eid)}" title="{esc(title)}">{esc(eid)}</button>')
    return "".join(out)

def gpio_chain_for_text(text):
    chains = []
    for controller, offset in re.findall(r"&([A-Za-z0-9_]+)\s+(\d+)\s+GPIO_", text):
        key = (controller, offset)
        if key in GPIO_CHAINS:
            chains.append({
                "controller": controller,
                "offset": offset,
                "steps": GPIO_CHAINS[key],
            })
    return chains


def ids_for_line(line_no, row, source_line, evidence):
    ids = [eid for eid in row["evidence"] if eid == "SW" or eid.startswith("E")] if row else []
    for chain in gpio_chain_for_text(source_line):
        for eid, _label in chain["steps"]:
            if eid not in ids:
                ids.append(eid)
    filtered = [eid for eid in ids if eid == "SW" or eid in evidence]
    filtered = [eid for eid in filtered if eid != "SW"]
    return filtered or ["SW"]


def note_for_line(row, ids, evidence):
    original = row["evidence"] if row else []
    dropped = [eid for eid in original if eid.startswith("E") and eid not in evidence]
    if ids == ["SW"] and dropped:
        return "非 FRDM-IMX93-DESIGNFILES/PDF 的 evidence 已排除；此行目前沒有可用的 FRDM PDF 證據。"
    if dropped:
        return row["note"] + "；另有非 FRDM PDF evidence 已排除：" + ", ".join(dropped)
    return row["note"] if row else "No FRDM PDF evidence assigned."


def block_summary(block, line_rows, evidence):
    ids = []
    notes = Counter()
    for line_no in range(block["start"], block["end"] + 1):
        row = line_rows.get(line_no)
        if not row:
            continue
        ids.extend([eid for eid in ids_for_line(line_no, row, "", evidence) if eid != "SW"])
        if row["note"]:
            notes[row["note"]] += 1
    unique_ids = list(dict.fromkeys(ids))
    if unique_ids:
        phrases = []
        for eid in unique_ids[:4]:
            item = evidence[eid]
            phrases.append(f'{eid} {item["term"]} ({item["pdf"]} p.{item["page"]})')
        more = f"；另有 {len(unique_ids) - 4} 個 evidence" if len(unique_ids) > 4 else ""
        return "此 block 主要對應：" + "、".join(phrases) + more + "。"
    common = notes.most_common(1)
    if common:
        return "此 block 屬於軟體/SoC 設定或尚未找到直接 schematic 物件：" + common[0][0]
    return "此 block 沒有 coverage matrix 對應行，保留原始碼供人工檢查。"


def code_for_block(lines, start, end):
    width = len(str(end))
    rendered = []
    for line_no in range(start, end + 1):
        rendered.append(f"{line_no:>{width}}  {lines[line_no - 1]}")
    return "\n".join(rendered)


def render_evidence_data(evidence):
    entries = []
    for eid, item in evidence.items():
        crop = f"crops/{eid}.png"
        page = f"annotated_{item['pdf']}_p{int(item['page']):02d}.png"
        pdf = PDF_PATH.get(item["pdf"], "")
        entries.append(
            f'"{eid}":{{'
            f'"id":"{esc(eid)}","pdf":"{esc(item["pdf"])}","pdfPath":"{esc(pdf)}",'
            f'"page":"{esc(item["page"])}","term":"{esc(item["term"])}",'
            f'"kind":"{esc(item.get("kind", ""))}","dts":"{esc(item.get("dts", ""))}",'
            f'"summary":"{esc(item.get("summary", ""))}",'
            f'"crop":"{esc(crop)}","pageImage":"{esc(page)}"'
            f"}}"
        )
    return "{\n" + ",\n".join(entries) + "\n}"


def render():
    evidence = parse_evidence()
    line_rows = parse_line_matrix()
    lines = DTS.read_text().splitlines()
    blocks = parse_blocks(lines)

    by_depth = defaultdict(int)
    for block in blocks:
        by_depth[block["depth"]] += 1

    block_html = []
    for idx, block in enumerate(blocks, start=1):
        line_ids = []
        table_rows = []
        for line_no in range(block["start"], block["end"] + 1):
            row = line_rows.get(line_no)
            if not row:
                continue
            ids = ids_for_line(line_no, row, lines[line_no - 1], evidence)
            line_ids.extend([eid for eid in ids if eid != "SW"])
            chains = gpio_chain_for_text(lines[line_no - 1])
            chain_html = ""
            if chains:
                chain_bits = []
                for chain in chains:
                    steps = []
                    for eid, label in chain["steps"]:
                        if eid not in evidence:
                            continue
                        steps.append(f'<span>{evidence_badges([eid], evidence)} {esc(label)}</span>')
                    if not steps:
                        continue
                    chain_bits.append(
                        f'<div class="chain"><strong>&amp;{esc(chain["controller"])} offset {esc(chain["offset"])}</strong>'
                        f'{"<em>→</em>".join(steps)}</div>'
                    )
                chain_html = "".join(chain_bits)
            table_rows.append(
                "<tr>"
                f"<td>{line_no}</td>"
                f"<td><code>{esc(row['text'])}</code></td>"
                f"<td>{evidence_badges(ids, evidence)}</td>"
                f"<td>{esc(note_for_line(row, ids, evidence))}{chain_html}</td>"
                "</tr>"
            )
        unique_ids = list(dict.fromkeys(line_ids))
        dominant_kind = "sw"
        if unique_ids:
            dominant_kind = evidence[unique_ids[0]].get("kind", "peripheral")
        source = "、".join(
            f"{eid} {evidence[eid]['pdf']} p.{evidence[eid]['page']}"
            for eid in unique_ids[:6]
        ) or "SW / SoC"
        more = f" +{len(unique_ids) - 6}" if len(unique_ids) > 6 else ""
        open_attr = " open" if idx == 1 else ""
        block_html.append(
            f'<details class="block {esc(dominant_kind)}" id="block-{idx}" data-evidence="{esc(",".join(unique_ids))}"{open_attr}>'
            "<summary>"
            f'<span class="line-range">L{block["start"]}-L{block["end"]}</span>'
            f'<span class="block-title">{esc(block["label"])}</span>'
            f'<span class="source">{esc(source + more)}</span>'
            "</summary>"
            f'<p class="why">{esc(block_summary(block, line_rows, evidence))}</p>'
            f'<pre class="code"><code>{esc(code_for_block(lines, block["start"], block["end"]))}</code></pre>'
            '<div class="evidence-strip">'
            f"{evidence_badges(unique_ids or ['SW'], evidence)}"
            "</div>"
            "<table>"
            "<thead><tr><th>行</th><th>DTS 內容</th><th>PDF evidence</th><th>為什麼這樣寫 / coverage note</th></tr></thead>"
            f"<tbody>{''.join(table_rows)}</tbody>"
            "</table>"
            "</details>"
        )

    html_doc = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FRDM-IMX93 DTS Block Evidence</title>
<style>
:root {{
  color-scheme: light;
  --bg: #f5f6f2;
  --panel: #ffffff;
  --ink: #22303a;
  --muted: #637282;
  --line: #d8ded7;
  --i2c: #1e63c7;
  --pinmux: #208a53;
  --power: #b86112;
  --peripheral: #6846bb;
  --sw: #59636e;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--ink); }}
header {{ position: sticky; top: 0; z-index: 5; padding: 16px 20px; background: #fff; border-bottom: 1px solid var(--line); }}
h1 {{ margin: 0; font-size: 22px; line-height: 1.2; }}
.meta {{ margin-top: 8px; display: flex; flex-wrap: wrap; gap: 10px; color: var(--muted); font-size: 13px; }}
.meta a {{ color: #245e86; text-decoration: none; }}
main {{ display: grid; grid-template-columns: minmax(560px, 58vw) 1fr; min-height: calc(100vh - 80px); }}
.left {{ padding: 16px 18px 40px; }}
.toolbar {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }}
.toolbar input, .toolbar select {{ border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; background: #fff; color: var(--ink); font-size: 13px; }}
.toolbar input {{ flex: 1; min-width: 260px; }}
.block {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; margin: 0 0 10px; overflow: hidden; }}
.block[open] {{ box-shadow: 0 2px 16px rgba(32, 42, 50, .08); }}
summary {{ display: grid; grid-template-columns: 92px minmax(200px, 1fr) minmax(160px, 32%); gap: 10px; align-items: center; padding: 10px 12px; cursor: pointer; list-style: none; }}
summary::-webkit-details-marker {{ display: none; }}
.line-range {{ color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; }}
.block-title {{ font-weight: 700; overflow-wrap: anywhere; }}
.source {{ color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }}
.why {{ margin: 0; padding: 10px 12px; border-top: 1px solid var(--line); color: #394956; line-height: 1.45; font-size: 13px; }}
.code {{ margin: 0; padding: 12px; max-height: 280px; overflow: auto; background: #fbfcfa; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); font-size: 12px; line-height: 1.45; }}
code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
.evidence-strip {{ display: flex; flex-wrap: wrap; gap: 6px; padding: 10px 12px; border-bottom: 1px solid var(--line); }}
.badge {{ border: 1px solid var(--line); border-radius: 999px; padding: 3px 8px; background: #fff; color: var(--ink); font-size: 12px; cursor: pointer; }}
.badge.i2c {{ border-color: color-mix(in srgb, var(--i2c) 45%, var(--line)); color: var(--i2c); }}
.badge.pinmux {{ border-color: color-mix(in srgb, var(--pinmux) 45%, var(--line)); color: var(--pinmux); }}
.badge.power {{ border-color: color-mix(in srgb, var(--power) 45%, var(--line)); color: var(--power); }}
.badge.peripheral {{ border-color: color-mix(in srgb, var(--peripheral) 45%, var(--line)); color: var(--peripheral); }}
.badge.sw {{ color: var(--sw); cursor: default; }}
.chain {{ margin-top: 8px; padding: 8px; border-left: 3px solid #456e83; background: #f7faf8; line-height: 1.45; }}
.chain strong {{ display: block; margin-bottom: 5px; color: #22303a; }}
.chain span {{ display: inline-block; margin: 2px 0; }}
.chain em {{ display: inline-block; padding: 0 6px; color: var(--muted); font-style: normal; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
th, td {{ padding: 7px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ text-align: left; background: #eef2ee; color: #33424e; }}
td:nth-child(1) {{ width: 54px; color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
td:nth-child(2) {{ width: 34%; }}
.right {{ border-left: 1px solid var(--line); background: #ecefeb; position: sticky; top: 80px; height: calc(100vh - 80px); display: flex; flex-direction: column; }}
.viewer-head {{ padding: 10px 14px; background: #fff; border-bottom: 1px solid var(--line); }}
.viewer-head strong {{ display: block; font-size: 13px; }}
.viewer-head span {{ display: block; color: var(--muted); font-size: 12px; line-height: 1.35; margin-top: 3px; }}
.viewer-links {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }}
.viewer-links a {{ color: #245e86; font-size: 12px; text-decoration: none; }}
.crop-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; padding: 10px; max-height: 36vh; overflow: auto; background: #fff; border-bottom: 1px solid var(--line); }}
.crop-card {{ border: 1px solid var(--line); border-radius: 6px; padding: 6px; background: #fff; text-align: left; cursor: pointer; }}
.crop-card img {{ width: 100%; height: 86px; object-fit: cover; border: 1px solid var(--line); display: block; background: #fff; }}
.crop-card strong {{ display: block; margin-top: 5px; font-size: 12px; }}
.crop-card span {{ display: block; color: var(--muted); font-size: 11px; line-height: 1.25; }}
.page-view {{ flex: 1; overflow: auto; padding: 14px; }}
.page-view img {{ width: 1500px; max-width: none; background: #fff; box-shadow: 0 2px 18px rgba(30,38,45,.16); }}
.hidden {{ display: none; }}
@media (max-width: 1050px) {{
  main {{ grid-template-columns: 1fr; }}
  .right {{ position: static; height: 70vh; border-left: 0; border-top: 1px solid var(--line); }}
  summary {{ grid-template-columns: 80px 1fr; }}
  .source {{ grid-column: 2; }}
}}
</style>
</head>
<body>
<header>
  <h1>FRDM-IMX93 DTS Block Evidence Browser</h1>
  <div class="meta">
    <span>來源 DTS: orig/linux_kernel/imx93-11x11-frdm.dts</span>
    <span>證據範圍: FRDM-IMX93-DESIGNFILES/PDF only</span>
    <span>{len(blocks)} blocks</span>
    <span>depth: {", ".join(f"{k}={v}" for k, v in sorted(by_depth.items()))}</span>
    <span>舊的 index/Markdown matrix 可能包含非 FRDM PDF，本頁已排除那些來源</span>
  </div>
</header>
<main>
  <div class="left">
    <div class="toolbar">
      <input id="search" type="search" placeholder="搜尋 block、DTS 內容、evidence ID、PDF term">
      <select id="kind">
        <option value="">全部類型</option>
        <option value="power">Power / regulator</option>
        <option value="i2c">I2C device</option>
        <option value="pinmux">Pinmux / signal</option>
        <option value="peripheral">Peripheral</option>
        <option value="sw">SW / SoC only</option>
      </select>
    </div>
    <div id="blocks">
      {''.join(block_html)}
    </div>
  </div>
  <aside class="right">
    <div class="viewer-head">
      <strong id="viewerTitle">選擇一個 evidence 或 block</strong>
      <span id="viewerText">點選左側 evidence badge 後，這裡會顯示對應 PDF、頁碼、term、說明與標記圖。</span>
      <div class="viewer-links" id="viewerLinks"></div>
    </div>
    <div class="crop-list" id="cropList"></div>
    <div class="page-view"><img id="pageImage" alt="annotated schematic page" src="annotated_FRDM_p22.png"></div>
  </aside>
</main>
<script>
const EVIDENCE = {render_evidence_data(evidence)};
const search = document.getElementById('search');
const kind = document.getElementById('kind');
const blocks = Array.from(document.querySelectorAll('.block'));
const viewerTitle = document.getElementById('viewerTitle');
const viewerText = document.getElementById('viewerText');
const viewerLinks = document.getElementById('viewerLinks');
const cropList = document.getElementById('cropList');
const pageImage = document.getElementById('pageImage');

function selectEvidence(ids) {{
  const clean = ids.filter(id => EVIDENCE[id]);
  cropList.innerHTML = '';
  viewerLinks.innerHTML = '';
  if (!clean.length) {{
    viewerTitle.textContent = 'SW / SoC 設定';
    viewerText.textContent = '這些行沒有直接對應到 schematic 的元件或訊號，通常是 Linux/SoC binding、memory、graph endpoint 或 driver 設定。';
    return;
  }}
  const first = EVIDENCE[clean[0]];
  viewerTitle.textContent = `${{first.id}} · ${{first.term}} · ${{first.pdf}} p.${{first.page}}`;
  viewerText.textContent = `${{first.summary}} DTS: ${{first.dts}}`;
  if (first.pdfPath) {{
    const a = document.createElement('a');
    a.href = '../../' + first.pdfPath;
    a.textContent = '開啟原始 PDF';
    viewerLinks.appendChild(a);
  }}
  const pdf = document.createElement('a');
  pdf.href = 'imx93_frdm_dts_pdf_evidence_annotated.pdf';
  pdf.textContent = '開啟標記 PDF';
  viewerLinks.appendChild(pdf);
  pageImage.src = first.pageImage;
  for (const id of clean) {{
    const item = EVIDENCE[id];
    const card = document.createElement('button');
    card.className = 'crop-card';
    card.innerHTML = `<img src="${{item.crop}}" alt="${{id}} crop"><strong>${{id}} · ${{item.term}}</strong><span>${{item.pdf}} p.${{item.page}} · ${{item.kind}}</span>`;
    card.addEventListener('click', () => selectEvidence([id]));
    cropList.appendChild(card);
  }}
}}

document.addEventListener('click', (event) => {{
  const badge = event.target.closest('.badge[data-eid]');
  if (badge) {{
    event.preventDefault();
    selectEvidence([badge.dataset.eid]);
    return;
  }}
  const summary = event.target.closest('summary');
  if (summary) {{
    const block = summary.closest('.block');
    const ids = (block.dataset.evidence || '').split(',').filter(Boolean);
    selectEvidence(ids);
  }}
}});

function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  const selected = kind.value;
  for (const block of blocks) {{
    const textMatch = !q || block.textContent.toLowerCase().includes(q);
    const kindMatch = !selected || block.classList.contains(selected);
    block.classList.toggle('hidden', !(textMatch && kindMatch));
  }}
}}
search.addEventListener('input', applyFilters);
kind.addEventListener('change', applyFilters);
selectEvidence(['E01']);
</script>
</body>
</html>
"""
    HTML.write_text(html_doc)


if __name__ == "__main__":
    render()
