"""Publica as simulações no DivulgaCandContas com navegação de volta ao Museu.

As fontes em prototipo/ já trazem o CPF mascarado e sem dados pessoais sem fonte."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [("memoria-da-campanha", "memoria-da-campanha.html", "Memória da Campanha"),
         ("conteudo-digital-oficial", "conteudo-digital-oficial.html", "Conteúdo Digital Oficial")]
DISCLAIMER_END = "Não é um sistema oficial do TSE.</div>"
for name, out, label in PAGES:
    src = (ROOT / f"prototipo/{name}.dc.html").read_text()
    links = "".join(
        f'<a href="{o}" style="color:#FBF5EE;text-decoration:none;padding:2px 0;border-bottom:2px solid {"#F2A65A" if o == out else "transparent"};font-weight:{600 if o == out else 400}">{l}</a>'
        for _, o, l in PAGES)
    nav = ('\n<nav style="background:#4A1320;color:#FBF5EE;font-size:13px;line-height:1.4;padding:9px 16px;display:flex;gap:6px 18px;flex-wrap:wrap;align-items:center;justify-content:center">'
           '<a href="index.html" style="color:#FBF5EE;font-weight:600;text-decoration:none">← Museu Eleitoral</a>'
           '<span style="color:#E6CFC0">Simulação da proposta dentro do DivulgaCandContas:</span>' + links + '</nav>')
    assert src.count(DISCLAIMER_END) == 1, name
    src = src.replace(DISCLAIMER_END, DISCLAIMER_END + nav)
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / out).write_text(src)
    print("ok", out)
