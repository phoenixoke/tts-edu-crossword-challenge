import random, json, sys
sys.path.insert(0, '/home/claude/work')
from bank import PACKS

MAXW, MAXH = 15, 13

def can_place(grid, w, r, c, d):
    dr, dc = (0, 1) if d == 'A' else (1, 0)
    L = len(w)
    # cell before / after must be empty
    pr, pc = r - dr, c - dc
    if (pr, pc) in grid: return -1
    er, ec = r + dr * L, c + dc * L
    if (er, ec) in grid: return -1
    inter = 0
    for i, ch in enumerate(w):
        rr, cc = r + dr * i, c + dc * i
        if (rr, cc) in grid:
            g, dirs = grid[(rr, cc)]
            if g != ch or d in dirs: return -1
            inter += 1
        else:
            # perpendicular neighbours must be empty
            n1 = (rr + dc, cc + dr); n2 = (rr - dc, cc - dr)
            if n1 in grid or n2 in grid: return -1
    return inter

def bbox(grid):
    rs = [k[0] for k in grid]; cs = [k[1] for k in grid]
    return min(rs), max(rs), min(cs), max(cs)

def place(grid, w, r, c, d):
    dr, dc = (0, 1) if d == 'A' else (1, 0)
    for i, ch in enumerate(w):
        k = (r + dr * i, c + dc * i)
        if k in grid: grid[k][1].add(d)
        else: grid[k] = [ch, {d}]

def attempt(words, rng):
    order = words[:]
    rng.shuffle(order)
    order.sort(key=lambda x: -len(x[0]) + rng.random() * 3)
    grid = {}; placed = []
    first = order[0]
    d0 = rng.choice('AD')
    place(grid, first[0], 0, 0, d0); placed.append((first, 0, 0, d0))
    rest = order[1:]
    progress = True
    while rest and progress:
        progress = False
        for item in list(rest):
            w = item[0]
            cands = []
            for (pr, pc), (ch, dirs) in list(grid.items()):
                for i, wc in enumerate(w):
                    if wc != ch: continue
                    for d in 'AD':
                        if d in dirs: continue
                        r, c = (pr, pc - i) if d == 'A' else (pr - i, pc)
                        k = can_place(grid, w, r, c, d)
                        if k < 1: continue
                        # bbox check
                        g2 = dict(grid)
                        dr, dc = (0, 1) if d == 'A' else (1, 0)
                        rs = [x[0] for x in grid] + [r, r + dr * (len(w) - 1)]
                        cs = [x[1] for x in grid] + [c, c + dc * (len(w) - 1)]
                        H = max(rs) - min(rs) + 1; W = max(cs) - min(cs) + 1
                        if W > MAXW or H > MAXH: continue
                        score = k * 10 - (W * H) / 8 - abs(W - H * 1.2) + rng.random() * 4
                        cands.append((score, r, c, d))
            if cands:
                cands.sort(reverse=True)
                _, r, c, d = cands[0]
                place(grid, w, r, c, d); placed.append((item, r, c, d))
                rest.remove(item); progress = True
    return grid, placed, rest

def validate(grid, placed):
    # every maximal run >=2 must equal exactly one placed word
    words = {(r, c, d): it[0] for it, r, c, d in placed}
    r0, r1, c0, c1 = bbox(grid)
    runs = set()
    for d in 'AD':
        lines = range(r0, r1 + 1) if d == 'A' else range(c0, c1 + 1)
        for ln in lines:
            span = range(c0, c1 + 2) if d == 'A' else range(r0, r1 + 2)
            cur = []
            for p in span:
                k = (ln, p) if d == 'A' else (p, ln)
                if k in grid: cur.append(k)
                else:
                    if len(cur) >= 2:
                        s = cur[0]; txt = ''.join(grid[x][0] for x in cur)
                        runs.add((s[0], s[1], d, txt))
                    cur = []
    expect = {(r, c, d, w) for (r, c, d), w in words.items()}
    if runs != expect: return False
    # connectivity
    start = next(iter(grid)); seen = {start}; st = [start]
    while st:
        a, b = st.pop()
        for n in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
            if n in grid and n not in seen: seen.add(n); st.append(n)
    return len(seen) == len(grid)

def build(pack, seed=1):
    rng = random.Random(seed * 7919 + pack['id'])
    main = [(w, c) for w, c in pack['words'] if not w.startswith('*')]
    spare = [(w[1:], c) for w, c in pack['words'] if w.startswith('*')]
    best = None
    for pool in (main, main + spare):
        for t in range(4000):
            grid, placed, rest = attempt(pool, rng)
            if rest: continue
            if not validate(grid, placed): continue
            r0, r1, c0, c1 = bbox(grid)
            W, H = c1 - c0 + 1, r1 - r0 + 1
            inter = sum(1 for v in grid.values() if len(v[1]) == 2)
            density = len(grid) / (W * H)
            score = inter * 3 + density * 40 - abs(W - H) * 0.5
            if best is None or score > best[0]:
                best = (score, grid, placed)
        if best: break
    assert best, f"Paket {pack['id']} gagal"
    _, grid, placed = best
    r0, r1, c0, c1 = bbox(grid)
    W, H = c1 - c0 + 1, r1 - r0 + 1
    # normalise
    pl = [(it, r - r0, c - c0, d) for it, r, c, d in placed]
    starts = {}
    for it, r, c, d in pl: starts.setdefault((r, c), []).append((it, d))
    num = 0; entries = []
    for (r, c) in sorted(starts):
        num += 1
        for it, d in sorted(starts[(r, c)], key=lambda x: x[1]):
            entries.append(dict(n=num, dir=d, row=r, col=c, answer=it[0], clue=it[1], len=len(it[0])))
    return dict(id=pack['id'], name=pack['name'], level=pack['level'], w=W, h=H, words=entries)

if __name__ == '__main__':
    out = []
    for p in PACKS:
        b = build(p)
        out.append(b)
        print(p['id'], p['name'], f"{b['w']}x{b['h']}", len(b['words']), 'kata', [w['answer'] for w in b['words']])
    json.dump(out, open('/home/claude/work/packs.json', 'w'), ensure_ascii=False)
