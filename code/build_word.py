"""Build a Word convenience copy with the PDF's citation and cross-reference numbers."""
import pathlib
import re
import subprocess
import tempfile
from docx import Document
from docx.shared import Pt

root=pathlib.Path(__file__).resolve().parents[1]
paper=root/"manuscript";tex=(paper/"CQA07_v2.tex").read_text()
aux=(paper/"CQA07_v2.aux").read_text()
citations=dict(re.findall(r"\\bibcite\{([^}]+)\}\{([^}]+)\}",aux))
labels=dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]+)\}",aux))
assert len(citations)==13
def cite(match):
    optional=match.group(1);keys=match.group(2).split(",")
    nums=", ".join(citations[k.strip()] for k in keys)
    return "["+nums+("; "+optional if optional else "")+"]"
tex=re.sub(r"\\cite(?:\[([^\]]+)\])?\{([^}]+)\}",cite,tex)
names={"thm":"Theorem","lem":"Lemma","cor":"Corollary","rem":"Remark","tab":"Table",
       "fig":"Figure","sec":"Section","app":"Appendix","def":"Definition"}
def cross(match):
    key=match.group(1)
    return names.get(key.split(":")[0],"Section")+" "+labels[key]
tex=re.sub(r"\\Cref\{([^}]+)\}",cross,tex)
tex=re.sub(r"\\eqref\{([^}]+)\}",lambda m:"("+labels[m.group(1)]+")",tex)
tex=re.sub(r"\\ref\{([^}]+)\}",lambda m:labels[m.group(1)],tex)
def theorem_heading(match):
    kind,caption,label=match.groups()
    suffix=(" ("+caption+")") if caption else ""
    return "\\paragraph{"+kind.title()+" "+labels[label]+suffix+".}"
tex=re.sub(r"\\begin\{(theorem|lemma|definition|corollary|remark)\}(?:\[([^\]]+)\])?\s*\\label\{([^}]+)\}",
           theorem_heading,tex)
tex=re.sub(r"\\end\{(?:theorem|lemma|definition|corollary|remark)\}","",tex)
tex=tex.replace(r"\input{computed_values.tex}",(paper/"computed_values.tex").read_text())
tex=tex.replace(r"\begin{thebibliography}{99}",r"\section*{References}"+"\n"+r"\begin{enumerate}")
tex=re.sub(r"\\bibitem\{[^}]+\}",r"\\item",tex)
tex=tex.replace(r"\end{thebibliography}",r"\end{enumerate}")
# Pandoc cannot embed a PDF in Word; use the matching regenerated PNG.
tex=tex.replace("fig1_frontier.pdf","fig1_frontier.png").replace("fig2_covering.pdf","fig2_covering.png")
with tempfile.TemporaryDirectory(prefix="cqa07-word-") as d:
    source=pathlib.Path(d)/"word_source.tex";source.write_text(tex)
    result=subprocess.run(["pandoc",str(source),"--from=latex","--to=docx",
                           "--resource-path="+str(paper)+":"+str(paper/"figures"),
                           "-o",str(paper/"CQA07_v2.docx")],capture_output=True,text=True)
    (root/"logs/word_build.log").write_text(result.stdout+result.stderr)
    result.check_returncode()
doc=Document(paper/"CQA07_v2.docx")
doc.styles["Normal"].font.size=Pt(12)
doc.save(paper/"CQA07_v2.docx")
text="\n".join(p.text for p in doc.paragraphs)
assert "XXXXXXXX" not in text and "[JOURNAL]" not in text
assert "[1]" in text and "References" in text
print("Word copy generated with numeric citations and resolved references")
