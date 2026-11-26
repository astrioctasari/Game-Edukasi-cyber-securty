// Jendela Browser: pencarian dan halaman web palsu untuk tiap kasus.

// Kata kunci pencarian saat ini
let Q = "";

// Tampilkan halaman h dengan alamat u
function bw(h, u) {
  $("#bp").innerHTML = h;
  $("#bu").textContent = u;
}

// Halaman awal Browser
function bhome() {
  bw(
    "<h3>🔎 CariAja</h3><p>Cari petunjuk di internet. Coba kata kunci seperti nama, domain, atau topik kasus.</p>",
    "cariaja.id"
  );
}

// Cari halaman dari kata kunci
function bsearch(q) {
  const ws = q
    .toLowerCase()
    .split(/\s+/)
    .filter((x) => x.length > 2);
  const r = LV[cur].web
    .map((p) => [
      p,
      ws.filter((w) => (p[0] + " " + p[1] + " " + p[2]).toLowerCase().includes(w)).length,
    ])
    .filter((x) => x[1])
    .sort((a, b) => b[1] - a[1]);
  bw(
    r.length
      ? "<p>" +
          r.length +
          ' hasil untuk "' +
          esc(q) +
          '"</p>' +
          r
            .map(
              (x) =>
                '<p><a href="#" data-go="' +
                x[0][0] +
                '"><b>' +
                x[0][1] +
                "</b></a><br><small>" +
                x[0][0] +
                "</small></p>"
            )
            .join("")
      : '<p>Tidak ada hasil untuk "' + esc(q) + '". Coba kata kunci lain.</p>',
    "cariaja.id/cari?q=" + encodeURIComponent(q)
  );
}

// Pasang aksi Browser: cari, buka halaman, dan pilih bukti
function wireWeb() {
  const w = $("#w-web");
  bhome();
  const go = () => {
    Q = $("#bq").value.trim();
    if (Q) bsearch(Q);
  };
  $("#bs").onclick = go;
  $("#bq").onkeydown = (e) => {
    if (e.key == "Enter") go();
  };
  $("#bh").onclick = bhome;
  w.addEventListener("click", (e) => {
    const a = e.target.closest("[data-go]");
    if (a) {
      e.preventDefault();
      const g = a.dataset.go;
      if (g == "@") return Q ? bsearch(Q) : bhome();
      const p = LV[cur].web.find((x) => x[0] == g);
      if (p) bw(banner(p) + p[3] + '<p><a href="#" data-go="@">← Kembali ke hasil</a></p>', p[0]);
      return;
    }
    const u = e.target.closest("[data-v]");
    if (u) setPin(u.dataset.v, "Browser");
  });
}
