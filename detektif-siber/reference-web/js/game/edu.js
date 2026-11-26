// Jendela Buku Panduan.

// Isi jendela Buku Panduan: daftar bab dan area baca
const bookHTML = (ks) =>
  '<div class="book"><div class="pgb" id="rd"><small class="chp">BUKU PANDUAN</small><h3>Pilih bab di sisi kanan</h3><p class="mut">Tiap bab yang dibaca memberi +10 EXP.</p></div><div class="tabs">' +
  ks
    .map(
      (k, i) =>
        '<button class="ed" data-k="' +
        k +
        '" style="--c:' +
        COL[i % 5] +
        '" aria-label="Bab ' +
        (i + 1) +
        '">' +
        (i + 1) +
        "</button>"
    )
    .join("") +
  "</div></div>";

// Pasang klik pada bab (+10 XP saat pertama dibaca)
function wireEdu() {
  $("#w-edu").addEventListener("click", (e) => {
    const b = e.target.closest(".ed");
    if (!b) return;
    const k = b.dataset.k,
      v = ED[k];
    const bs = [...document.querySelectorAll("#w-edu .ed")],
      em = v[0].split(" ")[0];
    $("#rd").innerHTML =
      '<small class="chp">BAB ' +
      (bs.indexOf(b) + 1) +
      "</small><h3>" +
      v[0].slice(em.length + 1) +
      "</h3><p>" +
      v[1] +
      '</p><div class="cmc"><i>' +
      em +
      "</i><em>" +
      v[2] +
      "</em></div>";
    bs.forEach((x) => x.classList.toggle("on", x === b));
    if (!read[k]) {
      read[k] = 1;
      xp += 10;
      save();
      $("#xp").textContent = xp;
      $("#rk").textContent = rank();
    }
  });
}
