// Jendela Terminal: menyusun perintah SQL dari bubble.

// Susunan perintah, bubble yang tersedia, dan jumlah hasil
let QT = [],
  TRAYF = [],
  TRAY = [],
  tcnt = 0;

// Warna bubble menurut jenisnya
const KC = { kw: "#6cc4ff", tbl: "#3dc6ff", col: "#a9b3ff", op: "#ff7a6b", val: "#ffd95a" };

// Terjemahan istilah SQL ke bahasa sehari-hari
const TRN = {
  SELECT: "Tampilkan",
  "*": "semua kolom",
  "COUNT(*)": "jumlah baris",
  FROM: "dari tabel",
  WHERE: "yang",
  AND: "dan",
  "=": "sama dengan",
  "<>": "bukan",
  LIKE: "mirip pola",
  ">": "lebih dari",
  "<": "kurang dari",
  "ORDER BY": "urutkan menurut",
  DESC: "dari terbesar",
  ",": "dan",
};

// Ubah bubble menjadi teks
const tv2 = (t) => (t.k == "val" ? (typeof t.v == "number" ? String(t.v) : "'" + t.v + "'") : t.v);

// Jalankan perintah dan hasilkan baris data
function runQ(tk) {
  let i = 0;
  const pk = () => tk[i],
    nx = () => tk[i++],
    e = (m) => {
      throw Error(m);
    };
  if (!tk.length || tk[0].v != "SELECT") e("Perintah harus diawali bubble SELECT.");
  i = 1;
  let cols = [],
    cnt = false;
  if (pk() && pk().v == "COUNT(*)") {
    cnt = true;
    i++;
  } else if (pk() && pk().v == "*") {
    cols = "*";
    i++;
  } else {
    while (pk() && pk().k == "col") {
      cols.push(nx().v);
      if (pk() && pk().v == ",") i++;
      else break;
    }
    if (!cols.length) e("Setelah SELECT pilih *, COUNT(*), atau nama kolom.");
  }
  if (!pk() || pk().v != "FROM") e("Tambahkan bubble FROM, lalu nama tabel.");
  i++;
  const t = nx();
  if (!t || t.k != "tbl") e("Setelah FROM pilih nama tabel.");
  const R = DB[t.v],
    ks = Object.keys(R[0]);
  if (cols != "*")
    cols.forEach((c) => {
      if (!ks.includes(c)) e('Kolom "' + c + '" tidak ada di tabel ' + t.v + ".");
    });
  const cd = [];
  if (pk() && pk().v == "WHERE") {
    i++;
    for (;;) {
      const c = nx(),
        o = nx(),
        v = nx();
      if (!c || c.k != "col") e("Setelah WHERE pilih nama kolom.");
      if (!ks.includes(c.v)) e('Kolom "' + c.v + '" tidak ada di tabel ' + t.v + ".");
      if (!o || o.k != "op") e("Setelah kolom pilih operator (=, <>, LIKE ...).");
      if (!v || v.k != "val") e("Setelah operator pilih sebuah nilai.");
      cd.push([c.v, o.v, v.v]);
      if (pk() && pk().v == "AND") {
        i++;
        continue;
      }
      break;
    }
  }
  let ob = null,
    ds = false;
  if (pk() && pk().v == "ORDER BY") {
    i++;
    const c = nx();
    if (!c || c.k != "col" || !ks.includes(c.v)) e("Setelah ORDER BY pilih kolom dari tabel ini.");
    ob = c.v;
    if (pk() && pk().v == "DESC") {
      ds = true;
      i++;
    }
  }
  if (i < tk.length) e("Ada bubble berlebih: " + tv2(tk[i]));
  let r = R.filter((x) =>
    cd.every(([c, o, v]) => {
      const a = x[c],
        A = String(a).toLowerCase(),
        B = String(v).toLowerCase(),
        n = !isNaN(a) && !isNaN(v);
      return o == "="
        ? A == B
        : o == "<>"
          ? A != B
          : o == "LIKE"
            ? new RegExp(
                "^" + B.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/%/g, ".*") + "$"
              ).test(A)
            : o == ">"
              ? n
                ? +a > +v
                : A > B
              : n
                ? +a < +v
                : A < B;
    })
  );
  if (ob) r = [...r].sort((a, b) => (a[ob] > b[ob] ? 1 : -1) * (ds ? -1 : 1));
  return cnt
    ? [["COUNT(*)"], [{ "COUNT(*)": r.length }], true]
    : [cols == "*" ? ks : cols, r, false];
}

// Siapkan bubble yang tersedia di level ini
function trayBuild() {
  const i = cur,
    B = ["SELECT", "*", "FROM", "WHERE"],
    O = ["="];
  if (i >= 3) {
    B.push("AND");
    O.push("<>", "LIKE");
  }
  if (i >= 5) {
    B.push("COUNT(*)", "ORDER BY", "DESC", ",");
    O.push(">", "<");
  }
  const cols = [...new Set(Object.values(DB).flatMap((r) => Object.keys(r[0])))];
  let n = 0;
  const tkn = (k, a) => a.map((v) => ({ k, v, i: n++ }));
  TRAY = [
    ["Perintah", tkn("kw", B)],
    ["Tabel", tkn("tbl", Object.keys(DB))],
    ["Kolom", tkn("col", cols)],
    ["Operator", tkn("op", O)],
    ["Nilai", tkn("val", LV[cur].vals || [])],
  ];
  TRAYF = TRAY.flatMap((g) => g[1]);
}

// Gambar ulang baris perintah
function qdraw() {
  $("#ql").innerHTML =
    QT.map(
      (t, i) =>
        '<b class="qb" data-x="' +
        i +
        '" style="background:' +
        KC[t.k] +
        '" title="Klik untuk menghapus">' +
        esc(tv2(t)) +
        "</b>"
    ).join("") || '<i style="color:#a9acd0">(kosong)</i>';
  $("#qt").textContent = QT.length
    ? QT.map((t) => (t.k == "val" ? tv2(t) : TRN[t.v] || t.v)).join(" ")
    : "Susun bubble di bawah menjadi sebuah perintah.";
}

// Perintah yang diharapkan di langkah ini (dibaca dari petunjuk)
function expQ() {
  if (ti >= TK.length) return null;
  const t = TK[ti];
  for (const s of [t[3], t[1]]) {
    const m = s.indexOf("SELECT");
    if (m < 0) continue;
    let r = s.slice(m),
      o = [];
    for (;;) {
      r = r.replace(/^\s+/, "");
      const c = TRAYF.filter((x) => r.startsWith(tv2(x))).sort(
        (a, b) => tv2(b).length - tv2(a).length
      )[0];
      if (!c) break;
      o.push(c);
      r = r.slice(tv2(c).length);
    }
    if (o.length > 3) return o;
  }
  return null;
}

// Cek susunan perintah dan beri tahu bubble mana yang kurang tepat
function qchk() {
  const E = expQ();
  if (!E) return "";
  const a = QT.map(tv2),
    b = E.map(tv2);
  let i = 0;
  while (i < a.length && i < b.length && a[i] == b[i]) i++;
  if (i == b.length && a.length == b.length)
    return '<div class="msg good">✅ Susunan sudah benar.</div>';
  if (i == a.length)
    return '<div class="msg hint">🧭 Benar sejauh ini. Berikutnya: <b>' + esc(b[i]) + "</b></div>";
  if (i == b.length)
    return '<div class="msg bad">🧭 Bubble <b>' + esc(a[i]) + "</b> berlebih.</div>";
  return (
    '<div class="msg bad">🧭 Bubble ke-' +
    (i + 1) +
    " kurang tepat. Coba: <b>" +
    esc(b[i]) +
    "</b></div>"
  );
}

// Tombol Jalankan
function qrun() {
  const o = $("#qr");
  try {
    const [c, r, cn] = runQ(QT);
    qruns++;
    save();
    tcnt = r.length;
    o.innerHTML =
      '<div class="res"><table><tr>' +
      c.map((k) => "<th>" + esc(k) + "</th>").join("") +
      "</tr>" +
      r
        .map(
          (x) =>
            "<tr>" +
            c.map((k) => '<td data-v="' + esc(x[k]) + '">' + esc(x[k]) + "</td>").join("") +
            "</tr>"
        )
        .join("") +
      "</table></div>" +
      (r.length || cn ? "" : '<div class="errd">🚨 Tidak ada data yang cocok.</div>') +
      '<div class="row"><span>' +
      (cn ? "Klik angka hasilnya untuk dijadikan bukti." : r.length + " baris") +
      "</span>" +
      (cn ? "" : '<button class="btn" id="tpc">📌 Pakai jumlah ini</button>') +
      "</div>" +
      qchk();
  } catch (er) {
    o.innerHTML = '<div class="errd">🚨 ' + esc(er.message) + "</div>" + qchk();
  }
}

// Pasang aksi Terminal
function wireTerm() {
  const w = $("#w-term");
  QT = [];
  trayBuild();
  $("#tr").innerHTML = TRAY.map(
    (g) =>
      '<div class="tg2"><small>' +
      g[0] +
      "</small>" +
      g[1]
        .map(
          (t) =>
            '<button class="bb" data-i="' +
            t.i +
            '" style="background:' +
            KC[t.k] +
            '">' +
            esc(tv2(t)) +
            "</button>"
        )
        .join("") +
      "</div>"
  ).join("");
  w.addEventListener("click", (e) => {
    const b = e.target.closest(".bb");
    if (b) {
      QT.push(TRAYF[+b.dataset.i]);
      qdraw();
      return;
    }
    const q = e.target.closest(".qb");
    if (q) {
      QT.splice(+q.dataset.x, 1);
      qdraw();
      return;
    }
    const id = e.target.id;
    if (id == "qun") {
      QT.pop();
      qdraw();
    } else if (id == "qcl") {
      QT = [];
      qdraw();
      $("#qr").innerHTML = "";
    } else if (id == "qrun") qrun();
    else if (id == "tpc") setPin(String(tcnt), "jumlah baris");
    else if (e.target.tagName == "TD") setPin(e.target.dataset.v, "Terminal");
  });
  qdraw();
}

// Kerangka perintah: SELECT ... FROM ... WHERE ...
const SK = [
  ["SELECT", "kw"],
  ["*", "kw"],
  ["FROM", "kw"],
  ["tabel", "tbl"],
  ["WHERE", "kw"],
  ["kolom", "col"],
  ["operator", "op"],
  ["nilai", "val"],
]
  .map(
    (x) => '<span class="qb" style="background:' + KC[x[1]] + ';cursor:default">' + x[0] + "</span>"
  )
  .join("");

// Isi jendela Terminal
const TERMHTML =
  '<div class="term"><div class="pr">detektif@db:~$ <span class="ql" id="ql"></span></div><div class="trn" id="qt"></div><div class="trn">Klik bubble berurutan, lalu ▶ Jalankan. ' +
  SK +
  '</div><div id="tr"></div><div class="row"><button class="btn" id="qrun">▶ Jalankan</button><button class="btn g" id="qun">⌫ Hapus</button><button class="btn g" id="qcl">✕ Bersihkan</button></div><div id="qr"></div></div>';
