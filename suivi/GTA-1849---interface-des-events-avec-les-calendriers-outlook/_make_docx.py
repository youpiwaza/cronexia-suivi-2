import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

src = Path(__file__).with_name("final-report.md")
dst = Path(__file__).with_name("final-report.docx")
lines = src.read_text(encoding="utf-8").splitlines()

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def runs_from_text(text):
    parts = []
    buf = ""
    code = False
    for char in text:
        if char == "`":
            if buf:
                parts.append((buf, code))
                buf = ""
            code = not code
            continue
        buf += char
    if buf:
        parts.append((buf, code))
    xml = ""
    for value, is_code in parts:
        rpr = (
            '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr>'
            if is_code
            else ""
        )
        xml += f'<w:r>{rpr}<w:t xml:space="preserve">{escape(value)}</w:t></w:r>'
    return xml


def paragraph(text, style=None, bullet=False):
    ppr = ""
    if style:
        ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
    elif bullet:
        ppr = '<w:pPr><w:ind w:left="420" w:hanging="280"/></w:pPr>'
        text = "• " + text
    return f"<w:p>{ppr}{runs_from_text(text)}</w:p>"


body = []
para = []


def flush_para():
    if para:
        body.append(paragraph(" ".join(para)))
        para.clear()


for raw in lines:
    line = raw.rstrip()
    if line.strip() == "---":
        flush_para()
        continue
    if not line.strip():
        flush_para()
        continue
    if line.startswith("### "):
        flush_para()
        body.append(paragraph(line[4:].strip(), "Heading3"))
        continue
    if line.startswith("## "):
        flush_para()
        title = line[3:].strip()
        if title.startswith("Partie 2"):
            body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        body.append(paragraph(title, "Heading2"))
        continue
    if line.startswith("# "):
        flush_para()
        body.append(paragraph(line[2:].strip(), "Heading1"))
        continue
    if line.startswith("- "):
        flush_para()
        body.append(paragraph(line[2:].strip(), bullet=True))
        continue
    para.append(line.strip())

flush_para()

document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}">
  <w:body>
    {"".join(body)}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
'''

content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
"""

rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""

styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:sz w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:uiPriority w:val="9"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="360" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1F4E79"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:uiPriority w:val="9"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="320" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="2E75B6"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:uiPriority w:val="9"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="2E75B6"/></w:rPr>
  </w:style>
</w:styles>
"""

with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    archive.writestr("[Content_Types].xml", content_types)
    archive.writestr("_rels/.rels", rels)
    archive.writestr("word/_rels/document.xml.rels", doc_rels)
    archive.writestr("word/styles.xml", styles)
    archive.writestr("word/document.xml", document.encode("utf-8"))
