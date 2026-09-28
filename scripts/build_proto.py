"""Gera o protótipo com dados reais.

Entrada: prototipo/museu-eleitoral.dc.html + coleta/dados/gerados/real.json
Saída:   dist/index.html
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "prototipo/museu-eleitoral.dc.html").read_text()
real = json.loads((ROOT / "coleta/dados/gerados/real.json").read_text())


def sub(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, f"esperava {count}x, achei {n}x: {old[:80]!r}"
    src = src.replace(old, new)


def sub_between(start, end, new):
    """Troca tudo entre start (inclusive) e end (exclusive)."""
    global src
    i = src.index(start)
    j = src.index(end, i)
    src = src[:i] + new + src[j:]


# ---------------------------------------------------------------- template: início
sub('<span style="font-size:13px;color:#7A6A63;margin-right:4px">Temas:</span>',
    '<span style="font-size:13px;color:#7A6A63;margin-right:4px">Tipos:</span>')

# ---------------------------------------------------------------- template: candidato
sub('<span>Candidatos</span><span>/</span><span>Pernambuco</span><span>/</span><span style="color:#2B1A17">Jones Manoel</span>\n  </div>',
    '<span>Candidatos</span><span>/</span><span>{{ cand.ufName }}</span><span>/</span><span style="color:#2B1A17">{{ cand.short }}</span>\n  </div>\n'
    '  <div style="max-width:1200px;margin:0 auto;padding:14px 24px 0;display:flex;gap:8px;flex-wrap:wrap;align-items:center">\n'
    '    <span style="font-size:12px;color:#5E4E47;margin-right:4px">Acervo real, coletado em {{ collectedAt }}:</span>\n'
    '    <sc-for list="{{ candTabs }}" as="ct" hint-placeholder-count="2">\n'
    '      <button onClick="{{ ct.go }}" style="border:1px solid {{ ct.bd }};background:{{ ct.bg }};color:{{ ct.fg }};border-radius:20px;padding:6px 14px;font:inherit;font-size:13px;font-weight:600;cursor:pointer">{{ ct.label }}</button>\n'
    '    </sc-for>\n'
    '  </div>')
sub('<img src="https://en.wikipedia.org/wiki/Special:FilePath/Jones_Manoel.jpg" alt="Foto de Jones Manoel"',
    '<img src="{{ cand.photo }}" alt="Foto de {{ cand.short }}"')
sub('<a href="https://en.wikipedia.org/wiki/File:Jones_Manoel.jpg" target="_blank"',
    '<a href="{{ cand.photoPage }}" target="_blank"')
sub('font-weight:600">Deputado Federal - Pernambuco/PE</div>', 'font-weight:600">{{ cand.cargo }}</div>')
sub('flex-wrap:wrap">JONES MANOEL <span style="font-size:.62em;color:#7A1F33;font-weight:400">5050</span></h1>',
    'flex-wrap:wrap">{{ cand.name }} <span style="font-size:.62em;color:#7A1F33;font-weight:400">{{ cand.num }}</span></h1>')
sub('<div style="font-size:15px;color:#2B1A17">Partido Socialismo E Liberdade - PSOL · Federação PSOL REDE (50-PSOL/18-REDE)</div>',
    '<div style="font-size:15px;color:#2B1A17">{{ cand.party }}</div>')
sub('Situação: <strong>Deferido</strong>', 'Situação: <strong>{{ cand.situacao }}</strong>')
sub('Acervo do Museu · última coleta 24/09/2026, 14:00', 'Acervo do Museu · última coleta {{ collectedAt }}')
sub('<span style="font-size:13px;font-weight:600;color:#2B1A17;width:48px">Tema</span>',
    '<span style="font-size:13px;font-weight:600;color:#2B1A17;width:48px">Tipo</span>')
sub('margin:0">Promessas por tema</h3>', 'margin:0">Contribuições por tipo</h3>')
sub('Nenhuma promessa corresponde aos filtros selecionados.', 'Nenhum trecho classificado corresponde aos filtros selecionados.')
sub("Contratante: CNPJ 00.000.000/0001-00 (ilustrativo) · legitimado ✓ · exibe 'Propaganda Eleitoral' ✓", '{{ it.adText }}')
sub('<div style="margin-top:22px"><button style="border:1px solid #7A1F33;background:transparent;color:#7A1F33;border-radius:4px;padding:8px 18px;font:inherit;font-size:14px;font-weight:500;cursor:pointer" style-hover="background:#F1E3D3">Carregar mais</button></div>',
    '<div style="margin-top:22px;font-size:13px;color:#5E4E47;line-height:1.5">{{ collectNote }}</div>')
sub('Mandato 2027–2031 · simulação com dados ilustrativos',
    'Mandato 2027–2031 · compromissos reais identificados na campanha; as organizações parceiras só avaliam depois da posse')
sub('Fonte: TSE · atualizado em 18/09/2026</span>', '{{ cand.tseNote }}</span>')
sub('<a href="#" style="margin-top:14px;font-size:13px;font-weight:600">Ver no DivulgaCandContas ↗</a>',
    '<a href="{{ cand.divulga }}" target="_blank" rel="noopener" style="margin-top:14px;font-size:13px;font-weight:600">Ver no DivulgaCandContas ↗</a>\n'
    '        <div style="font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#7A6A63;padding:22px 0 6px">Canais declarados ao TSE</div>\n'
    '        <sc-for list="{{ channels }}" as="ch" hint-placeholder-count="5">\n'
    '          <div style="display:flex;gap:10px;align-items:flex-start;padding:7px 0;border-bottom:1px solid #F1E3D3;font-size:13px">\n'
    '            <span style="flex:none;width:9px;height:9px;border-radius:50%;margin-top:5px;background:{{ ch.dot }};border:1.5px solid {{ ch.ring }}"></span>\n'
    '            <span style="display:flex;flex-direction:column;gap:1px;min-width:0"><a href="{{ ch.url }}" target="_blank" rel="noopener" style="font-weight:600;word-break:break-all">{{ ch.label }}</a><span style="font-size:12px;color:#5E4E47">{{ ch.status }}</span></span>\n'
    '          </div>\n'
    '        </sc-for>')

sub('<div style="max-width:1200px;margin:0 auto;padding:32px 24px 72px;display:flex;gap:32px;flex-wrap:wrap-reverse;align-items:flex-start">',
    '<div style="max-width:1200px;margin:0 auto;padding:32px 24px 72px;display:flex;gap:32px;flex-wrap:wrap-reverse;align-items:flex-end">')

# ---------------------------------------------------------------- template: modal
MODAL = '''<!-- ============ 3. MODAL ============ -->
<sc-if value="{{ hasModal }}" hint-placeholder-val="{{ false }}">
  <div onClick="{{ closeModal }}" style="position:fixed;inset:0;z-index:50;background:rgba(43,26,23,.6);display:flex;align-items:flex-start;justify-content:center;padding:36px 12px;overflow-y:auto">
    <div onClick="{{ stop }}" style="background:#FBF5EE;border-radius:4px;box-shadow:0 16px 48px rgba(43,26,23,.3);width:100%;max-width:980px">
      <div style="padding:20px 24px;border-bottom:1px solid #E2CFBA;display:flex;align-items:flex-start;gap:16px">
        <div style="flex:1;min-width:0">
          <div style="font-size:12px;letter-spacing:1.2px;text-transform:uppercase;color:#7A1F33;font-weight:600">{{ m.modalTitle }}</div>
          <div style="font-family:'Source Serif 4',Georgia,serif;font-size:22px;font-weight:600;color:#4A1320;margin-top:4px;font-style:{{ m.fstyle }};text-wrap:pretty">{{ m.title }}</div>
          <div style="font-size:13px;color:#5E4E47;margin-top:8px;display:flex;align-items:center;gap:8px;flex-wrap:wrap">
            <span style="display:flex;align-items:center;gap:6px;background:#F1E3D3;border-radius:20px;padding:3px 11px 3px 8px;color:#2B1A17;font-weight:600"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#7A1F33" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="{{ m.icon }}"></path></svg>{{ m.origin }}</span>
            <span>{{ m.handle }}</span><span>{{ m.when }}</span>
          </div>
        </div>
        <button onClick="{{ closeModal }}" style="background:none;border:0;color:#4A1320;font-size:26px;line-height:1;cursor:pointer">×</button>
      </div>
      <div style="padding:22px 24px;display:flex;flex-direction:column;gap:20px">
        <sc-if value="{{ m.showFacade }}" hint-placeholder-val="{{ false }}">
          <button onClick="{{ playEmbed }}" title="Assistir ao vídeo" style="display:block;width:100%;aspect-ratio:16/9;border:0;padding:0;cursor:pointer;background:{{ m.posterBg }};position:relative">
            <span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:76px;height:76px;border-radius:50%;background:rgba(74,19,32,.92);display:flex;align-items:center;justify-content:center"><svg width="30" height="30" viewBox="0 0 24 24" fill="#FBF5EE"><path d="M8 5l12 7-12 7z"></path></svg></span>
            <span style="position:absolute;left:12px;bottom:12px;font-size:12px;color:#FBF5EE;background:rgba(0,0,0,.65);padding:4px 9px">Clique para carregar o player do YouTube</span>
          </button>
        </sc-if>
        <sc-if value="{{ m.showEmbed }}" hint-placeholder-val="{{ false }}">
          <div style="aspect-ratio:16/9;background:#2B1A17">
            <iframe src="{{ m.embed }}" title="Vídeo original" referrerpolicy="strict-origin-when-cross-origin" style="width:100%;height:100%;border:0;display:block" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe>
          </div>
        </sc-if>
        <div style="display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start">
          <sc-if value="{{ m.hasThumb }}" hint-placeholder-val="{{ false }}">
            <img src="{{ m.thumb }}" alt="Mídia do post" style="flex:none;width:180px;max-width:100%;border:1px solid #E2CFBA;background:#F1E3D3" />
          </sc-if>
          <div style="flex:1 1 320px;min-width:0;display:flex;flex-direction:column;gap:10px">
            <div style="font-size:15px;line-height:1.55;color:#2B1A17;white-space:pre-wrap;max-height:280px;overflow-y:auto;background:#fff;border:1px solid #E2CFBA;padding:12px 14px">{{ m.full }}</div>
            <sc-if value="{{ m.hasUrl }}" hint-placeholder-val="{{ true }}">
              <a href="{{ m.url }}" target="_blank" rel="noopener" style="align-self:flex-start;font-size:13px;font-weight:600">Abrir no original ↗</a>
              <div style="font-size:12px;color:#5E4E47;font-family:'IBM Plex Mono',monospace;word-break:break-all">{{ m.url }}</div>
            </sc-if>
          </div>
        </div>

        <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:stretch">
          <div style="flex:3 1 380px;min-width:0;background:#fff;border:1px solid #7A1F33">
            <div style="padding:12px 16px;border-bottom:1px solid #E2CFBA;display:flex;align-items:center;gap:8px">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7A1F33" stroke-width="1.8"><path d="M12 3l7 3v5c0 4.5-3 8.5-7 10-4-1.5-7-5.5-7-10V6l7-3z"></path></svg>
              <span style="font-size:15px;font-weight:600;color:#4A1320">Registro</span>
            </div>
            <div style="padding:16px;display:flex;flex-direction:column;gap:16px;font-size:14px">
              <div>
                <div style="font-weight:600;margin-bottom:6px">CID</div>
                <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
                  <code style="flex:1 1 260px;min-width:0;background:#FBF5EE;border:1px solid #E2CFBA;padding:8px 10px;font-family:'IBM Plex Mono',monospace;font-size:12px;word-break:break-all;color:#2B1A17">{{ m.cid }}</code>
                  <button onClick="{{ copyCid }}" style="height:34px;padding:0 14px;border:1px solid #7A1F33;background:#fff;color:#7A1F33;border-radius:4px;font:inherit;font-size:13px;font-weight:500;cursor:pointer" style-hover="background:#F1E3D3">{{ copyLabel }}</button>
                </div>
                <div style="font-size:12px;color:#5E4E47;margin-top:8px;line-height:1.5">CID v1 (sha2-256) do registro coletado. Se alguém mudar uma vírgula, o CID muda. A publicação no IPFS e no Fediverso entra no MVP.</div>
              </div>
              <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px">
                <div><div style="font-weight:600;margin-bottom:4px">Coleta</div><div style="line-height:1.5">{{ m.collected }}</div></div>
                <div><div style="font-weight:600;margin-bottom:4px">Canal</div><div style="line-height:1.5">{{ m.channelNote }}</div></div>
              </div>
              <div>
                <div style="font-weight:600;margin-bottom:4px">Histórico de versões</div>
                <sc-for list="{{ m.versions }}" as="v" hint-placeholder-count="1">
                  <div style="display:flex;gap:10px;align-items:center;padding:3px 0"><span style="width:8px;height:8px;border-radius:50%;background:#D9622B"></span><strong>{{ v.label }}</strong><span style="color:#5E4E47">{{ v.when }}</span></div>
                </sc-for>
              </div>
            </div>
          </div>
          <div style="flex:2 1 260px;min-width:0;border:1px dashed #B9A493;background:#F1E3D3">
            <div style="padding:12px 16px;border-bottom:1px dashed #B9A493">
              <div style="font-size:15px;font-weight:600;color:#2B1A17">Indexação</div>
              <div style="font-size:12px;color:#5E4E47">gerada por IA</div>
            </div>
            <div style="padding:16px;display:flex;flex-direction:column;gap:10px;font-size:14px;color:#2B1A17">
              <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center"><span style="font-weight:600">Tipo:</span><sc-for list="{{ m.cats }}" as="c" hint-placeholder-count="1"><span style="background:#FBF5EE;border-radius:20px;padding:2px 10px;font-size:13px">{{ c }}</span></sc-for></div>
              <div><span style="font-weight:600">Trecho:</span> {{ m.mark }}</div>
              <div><span style="font-weight:600">Revisão:</span> {{ m.review }}</div>
              <div style="font-size:12px;color:#5E4E47;border-top:1px solid #E2CFBA;padding-top:10px;line-height:1.5">A indexação organiza o acervo para busca. Pode conter imprecisões e não altera o registro.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</sc-if>

'''
sub_between('<!-- ============ 3. MODAL ============ -->', '<div style="position:fixed;left:50%;bottom:16px;', MODAL)

# ---------------------------------------------------------------- script: dados
DATA = "const REAL = " + json.dumps(real, ensure_ascii=False).replace("</", "<\\/") + ";\n"
DATA += r"""IC.yt = 'M3 7a3 3 0 013-3h12a3 3 0 013 3v10a3 3 0 01-3 3H6a3 3 0 01-3-3zM10 9l5 3-5 3z';
const NETS = { instagram: { label: 'Instagram', icon: IC.ig, stat: 'posts no Instagram' }, x: { label: 'X', icon: IC.x, stat: 'posts no X' }, youtube: { label: 'YouTube', icon: IC.yt, stat: 'vídeos no YouTube' } };
const TYPES = ['Propostas', 'Compromissos', 'Críticas', 'Propostas de fiscalização'];
BADGE['Repostagem'] = ['#B9A493', 'transparent', '#5E4E47', 'dashed'];
BADGE['Propaganda eleitoral identificada'] = ['#C9A3AC', '#F6E8EA', '#7A1F33', 'solid'];
const ALLI = {}, ALLC = {};
Object.entries(REAL.cands).forEach(([k, c]) => { c.items.forEach(x => { ALLI[x.id] = { ...x, cand: k }; }); c.contribs.forEach(x => { ALLC[x.id] = x; }); });
const FIRST_VIDEO_CONTRIB = Object.values(ALLC).find(c => ALLI[c.item].net === 'youtube') || Object.values(ALLC)[0];
"""
sub("const LSTART = [0, 8, 16, 24, 33, 42, 52, 61, 70, 80];", DATA + "const LSTART = [0, 8, 16, 24, 33, 42, 52, 61, 70, 80];")

sub("state = { page: 'home', tab: 'acervo', media: 'Todas', theme: null,",
    "state = { page: 'home', cand: 'jones', tab: 'acervo', media: 'Todas', theme: null,")
sub("'3': { ...c, modal: { tl: 't6', promise: 'p1' } }",
    "'3': { ...c, cand: ALLI[FIRST_VIDEO_CONTRIB.item].cand, modal: { tl: FIRST_VIDEO_CONTRIB.item, promise: FIRST_VIDEO_CONTRIB.id } }")

LOGIC = r"""    const C = REAL.cands[s.cand];
    const byId = {}; C.items.forEach(x => { byId[x.id] = x; });
    const netOk = x => s.media === 'Todas' || NETS[x.net].label === s.media;
    const cf = C.contribs.filter(c => netOk(byId[c.item]) && (!s.theme || c.type === s.theme));
    const groups = TYPES.map(ty => ({ theme: ty, list: cf.filter(c => c.type === ty) })).filter(g => g.list.length).map(g => ({
      theme: g.theme, count: g.list.length + (g.list.length === 1 ? ' trecho' : ' trechos'),
      items: g.list.map(c => { const x = byId[c.item]; return { text: '“' + c.quote + '”', icon: NETS[x.net].icon,
        source: NETS[x.net].label + ' · ' + x.acct + ' · ' + x.date, plan: 'IA · sem revisão humana', planBd: '#B9A493', planBg: 'transparent', planFg: '#5E4E47',
        open: () => this.openItem(x.id, c.id) }; })
    }));
    const tf = C.items.filter(x => netOk(x) && (!s.theme || x.types.includes(s.theme)));
    const RI = { views: 'M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12zM12 9a3 3 0 100 6 3 3 0 000-6z', likes: 'M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z', comments: 'M4 5h16v11H9l-5 4z', reposts: 'M4 12v7h16v-7M12 3v12M8 7l4-4 4 4' };
    const RL = { views: 'visualizações', likes: 'curtidas', comments: 'comentários', reposts: 'repostagens' };
    const clip = (t, n) => t.length > n ? t.slice(0, n - 1).trimEnd() + '…' : t;
    const items = tf.map(x => ({ ...x, icon: NETS[x.net].icon, origin: NETS[x.net].label + ' · ' + x.acct,
      text: x.text ? clip(x.text, 360) : '(post sem legenda)', fstyle: x.text ? 'normal' : 'italic',
      hasReach: x.metrics.length > 0, reach: x.metrics.map(([k, n]) => ({ n, icon: RI[k], label: RL[k] })), chipBg: '#FBF5EE',
      thumbBg: x.thumb ? 'center / cover no-repeat url("' + x.thumb + '"), #2B1A17' : 'repeating-linear-gradient(135deg,#F1E3D3 0 8px,#EADACA 8px 16px)',
      thumbFg: x.thumb ? 'transparent' : '#5E4E47',
      badges: x.badges.map(l => ({ label: l, bd: BADGE[l][0], bg: BADGE[l][1], fg: BADGE[l][2], bs: BADGE[l][3] })),
      boosted: x.ad,
      open: e => { e && e.preventDefault(); this.openItem(x.id, null); } }));

    let m = null, L = [];
    if (s.modal) {
      const legacy = TL.find(t => t.id === s.modal.tl);
      if (legacy) {
        m = { modalTitle: 'Registro ilustrativo', title: legacy.text, fstyle: 'normal', full: legacy.text + '\n\n[Item ilustrativo, usado só na demonstração de verificação.]',
          origin: legacy.origin, icon: legacy.icon, handle: '', when: legacy.date + ', ' + legacy.time, hasPlayer: false, embed: '', hasThumb: false, thumb: '',
          hasUrl: false, url: '', cid: 'ilustrativo', collected: 'ilustrativo', channelNote: 'ilustrativo', versions: [{ label: 'Publicado', when: legacy.date + ', ' + legacy.time }],
          cats: ['ilustrativo'], mark: 'ilustrativo', review: 'ilustrativo' };
      } else {
        const x = ALLI[s.modal.tl], c = s.modal.promise ? ALLC[s.modal.promise] : null;
        const when = x.date + (x.time ? ', ' + x.time : '');
        m = { modalTitle: c ? 'Trecho no original · ' + c.type : 'Registro do item',
          title: c ? '“' + c.quote + '”' : clip(x.title || x.text || '(post sem legenda)', 160), fstyle: c ? 'italic' : 'normal',
          full: (x.text || '(post sem legenda)') + (x.transcript.length ? '\n\nTranscrição automática do YouTube (pode conter erros):\n' + x.transcript.map(([t, l]) => String(Math.floor(t / 60)).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0') + '  ' + l).join('\n') : ''), origin: NETS[x.net].label, icon: NETS[x.net].icon, handle: x.acct + ' ·', when,
          hasPlayer: !!x.embed, showFacade: !!x.embed && !s.embedOn, showEmbed: !!x.embed && !!s.embedOn, embed: x.embed ? x.embed + '?autoplay=1' : '',
          posterBg: x.thumb ? 'center / cover no-repeat url("' + x.thumb.replace('hqdefault', 'maxresdefault') + '"), center / cover no-repeat url("' + x.thumb + '"), #2B1A17' : '#2B1A17', hasThumb: !!x.thumb && !x.embed, thumb: x.thumb || '', hasUrl: true, url: x.url,
          cid: x.cid, collected: REAL.collectedAt + ' · opencli ' + REAL.tool, channelNote: 'Canal declarado ao TSE ✓',
          versions: [{ label: 'Publicado', when }],
          cats: x.types.length ? x.types : ['nenhum tipo identificado'],
          mark: c ? c.quote : (x.types.length ? 'veja os trechos em “Contribuições por tipo”' : 'item integral · nenhum trecho classificado'),
          review: 'pendente · classificação automática, sem revisão humana' };
      }
      this._m = m;
    }
    const ai = this.activeIdx();
    const status = { 'Em andamento': ['#F2A65A', '#D9622B'], 'Cumprido': ['#7A1F33', '#7A1F33'], 'Não cumprido': ['transparent', '#7A6A63'], 'Sem avaliação': ['#E2CFBA', '#B9A493'] };
    const commitments = C.contribs.filter(c => c.type === 'Compromissos').map(c => { const x = byId[c.item];
      return { theme: 'Compromisso', text: '“' + c.quote + '”', icon: NETS[x.net].icon, source: NETS[x.net].label + ' · ' + x.acct + ' · ' + x.date,
        status: 'Sem avaliação', dot: status['Sem avaliação'][0], ring: status['Sem avaliação'][1],
        evaluator: 'Nenhuma organização parceira avaliou este compromisso. A avaliação começa depois da posse, em 2027.',
        open: e => { e.preventDefault(); this.openItem(x.id, c.id); } }; });
    const cnt = n => C.items.filter(x => x.net === n).length;
    const stats = [
      ...Object.keys(NETS).filter(n => cnt(n)).map(n => [cnt(n), NETS[n].stat, NETS[n].icon]),
      [C.contribs.length, 'trechos classificados pela IA'],
      ...TYPES.map(t => [C.contribs.filter(c => c.type === t).length, t.toLowerCase()]),
      [C.items.filter(x => x.ad).length, 'com identificação de propaganda eleitoral'],
      [C.items.filter(x => x.rt).length, 'repostagens']
    ].map(([n, label, icon]) => ({ n, label, icon: icon || null, hasParts: false, parts: [] }));
    const nets = Object.keys(NETS).filter(n => cnt(n)).map(n => NETS[n].label);
"""
sub_between("    const mediaOk = x => s.media === 'Todas' || x.media === s.media;", "    const chip = (on) =>", LOGIC)

sub("openItem(tl, promise) { clearInterval(this.timer); this.setState({ modal: { tl, promise }, t: 42, playing: false, copied: false }); }",
    "openItem(tl, promise) { clearInterval(this.timer); this.setState({ modal: { tl, promise }, t: 42, playing: false, copied: false, embedOn: false }); }")

# ---------------------------------------------------------------- script: valores devolvidos ao template
def sub_line(key_regex, new):
    global src
    pat = re.compile(r"^      " + key_regex + r".*$", re.M)
    assert len(pat.findall(src)) == 1, key_regex
    src = pat.sub(lambda _: new, src)

sub_line(r"homeChips: THEMES\.map", "      homeChips: TYPES.map(l => ({ label: l, ...chip(false), go: () => this.nav('cand', { theme: l, tab: 'acervo' }) })),")
sub_line(r"stats: \[\[41,", "      stats,")
sub_line(r"mediaOpts: \['Todas', 'Redes'", "      mediaOpts: ['Todas', ...nets].map(l => { const on = s.media === l; return { label: l, bg: on ? '#7A1F33' : 'transparent', fg: on ? '#fff' : '#7A1F33', bd: on ? '#7A1F33' : '#D8C4AE', go: () => this.setState({ media: l }) }; }),")
sub_line(r"themeChips: THEMES\.map", "      themeChips: TYPES.filter(t => C.contribs.some(c => c.type === t)).map(l => { const on = s.theme === l; return { label: l, ...chip(on), go: () => this.setState({ theme: on ? null : l }) }; }),")
sub_line(r"groups, noPromises", "      groups, noPromises: !groups.length, promiseCount: 'Mostrando ' + cf.length + ' de ' + C.contribs.length + ' trechos',")
sub_line(r"items, timelineCount", "      items, timelineCount: 'Mostrando ' + tf.length + ' de ' + C.items.length + ' itens',")
sub_line(r"tseFields: \[\['Nome completo'", "      tseFields: C.tse.map(([label, value]) => ({ label, value })),")
sub_line(r"statusSummary: \[\['Em andamento', 9\]", "      statusSummary: [['Em andamento', 0], ['Cumprido', 0], ['Não cumprido', 0], ['Sem avaliação', commitments.length]].map(([label, n]) => ({ label, n, dot: status[label][0], ring: status[label][1] })),")
sub_line(r"hasModal: !!m, m: m \|\|",
         "      hasModal: !!m, m: m || { versions: [], cats: [] },\n"
         "      cand: C, collectedAt: REAL.collectedAt, collectNote: C.collectNote, playEmbed: () => this.setState({ embedOn: true }),\n"
         "      candTabs: Object.entries(REAL.cands).map(([k, c]) => { const on = s.cand === k; return { label: c.short + ' · ' + c.uf, bg: on ? '#4A1320' : 'transparent', fg: on ? '#FBF5EE' : '#4A1320', bd: on ? '#4A1320' : '#D8C4AE', go: () => this.setState({ cand: k, media: 'Todas', theme: null, modal: null }) }; }),\n"
         "      channels: C.channels.map(ch => ({ ...ch, dot: ch.ok ? '#7A1F33' : 'transparent', ring: ch.ok ? '#7A1F33' : '#B9A493' })),")

# ---------------------------------------------------------------- navegação para as simulações no TSE
# menu: sem "Acervo" e "Promessas" (levavam à mesma página de "Candidatos")
sub("const navMap = { 'Acervo': 'cand', 'Candidatos': 'cand', 'Promessas': 'cand',", "const navMap = { 'Candidatos': 'cand',")
sub('Ver no DivulgaCandContas ↗</a>\n',
    'Ver no DivulgaCandContas ↗</a>\n'
    '        <a href="memoria-da-campanha.html" style="margin-top:10px;font-size:13px;font-weight:600">Veja como isso ficaria no DivulgaCandContas →</a>\n')

(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "dist/index.html").write_text(src)
print("ok:", len(src), "bytes")
