// Jendela Tabel: menyaring data kasus.

// Daftar operator saringan dan labelnya
const OPS = [
  ["=", "sama dengan"],
  ["c", "mengandung"],
  [">", "lebih dari / sesudah"],
  ["<", "kurang dari / sebelum"],
  ["!", "bukan"],
];

// Gambar kontrol saringan
function ui() {
  const ks = Object.keys(DB[tb][0]);
  $("#rl").innerHTML = rules
    .map(
      (r, i) =>
        '<div class="row" data-i="' +
        i +
        '"><select data-f="c">' +
        ks
          .map(
            (k, j) =>
              '<option value="' + j + '"' + (j == r.c ? " selected" : "") + ">" + k + "</option>"
          )
          .join("") +
        '</select><select data-f="o">' +
        OPS.map(
          (o) =>
            '<option value="' +
            o[0] +
            '"' +
            (o[0] == r.o ? " selected" : "") +
            ">" +
            o[1] +
            "</option>"
        ).join("") +
        '</select><input type="text" data-f="v" list="dl' +
        i +
        '" value="' +
        esc(r.v) +
        '" placeholder="pilih / isi nilai"><datalist id="dl' +
        i +
        '">' +
        [...new Set(DB[tb].map((x) => x[ks[r.c]]))]
          .map((v) => '<option value="' + esc(v) + '">')
          .join("") +
        "</datalist></div>"
    )
    .join("");
  view();
}

// Tampilkan hasil tabel sesuai saringan
function view() {
  const R = DB[tb],
    ks = Object.keys(R[0]);
  let o = R.filter((x) =>
    rules.every((r) => {
      if (r.v === "") return true;
      const a = x[ks[r.c]],
        b = r.v,
        A = String(a).toLowerCase(),
        B = b.toLowerCase(),
        n = !isNaN(a) && !isNaN(b);
      return r.o == "="
        ? A == B
        : r.o == "!"
          ? A != B
          : r.o == "c"
            ? A.includes(B)
            : r.o == ">"
              ? n
                ? +a > +b
                : A > B
              : n
                ? +a < +b
                : A < B;
    })
  );
  if (sk != null) o = [...o].sort((p, q) => (p[sk] > q[sk] ? 1 : -1) * sd);
  cnt = o.length;
  $("#cn").textContent = cnt + " dari " + R.length;
  $("#tv").innerHTML =
    '<div class="res"><table><tr>' +
    ks.map((k) => '<th data-k="' + k + '">' + k + " ↕</th>").join("") +
    "</tr>" +
    o
      .map(
        (x) =>
          "<tr>" +
          ks.map((k) => '<td data-v="' + esc(x[k]) + '">' + esc(x[k]) + "</td>").join("") +
          "</tr>"
      )
      .join("") +
    "</table></div>" +
    (o.length
      ? ""
      : '<div class="errd">🚨 Tidak ada data yang cocok. Coba ubah atau kurangi syaratnya.</div>');
}
