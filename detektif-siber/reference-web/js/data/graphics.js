// Gambar SVG yang dibuat lewat kode.

// Latar dinding meja kerja
const WALL =
  '<svg class="wall" viewBox="0 0 1000 690" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="wl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#171a3a"/><stop offset="1" stop-color="#2b3068"/></linearGradient><linearGradient id="nt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0d2e"/><stop offset="1" stop-color="#4553c9"/></linearGradient><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd95a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd95a" stop-opacity="0"/></linearGradient></defs><rect width="1000" height="690" fill="url(#wl)"/>' +
  '<rect x="560" y="46" width="390" height="340" fill="url(#nt)" stroke="#0d0f24" stroke-width="8"/><circle cx="860" cy="118" r="30" fill="#f3efe6"/><path d="M560 386V270h40v-34h30v54h30v-96h40v74h30v-44h40v64h30v-116h40v96h30v-34h40v142z" fill="#10122b"/>' +
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    .map(
      (i) =>
        '<rect x="560" y="' +
        (54 + i * 33) +
        '" width="390" height="11" fill="#0d0f24" opacity=".6"/>'
    )
    .join("") +
  '<polygon points="560,46 950,46 1000,330 480,330" fill="#fff" opacity=".05"/><rect x="100" y="86" width="340" height="216" fill="#c8955a" stroke="#5a3f3a" stroke-width="9"/>' +
  '<polyline points="170,140 290,200 380,130 210,250" fill="none" stroke="#d9483a" stroke-width="3"/><g stroke="#0d0f24" stroke-width="2"><rect x="140" y="112" width="60" height="50" fill="#fff6dd" transform="rotate(-6 170 137)"/><rect x="260" y="170" width="64" height="52" fill="#fff" transform="rotate(5 290 196)"/><rect x="350" y="106" width="56" height="48" fill="#ffd95a" transform="rotate(8 378 130)"/><rect x="182" y="226" width="62" height="50" fill="#a9b3ff" transform="rotate(-4 213 251)"/></g><circle cx="170" cy="140" r="5" fill="#d9483a"/><circle cx="290" cy="200" r="5" fill="#d9483a"/><circle cx="380" cy="130" r="5" fill="#d9483a"/>' +
  '<rect y="520" width="1000" height="170" fill="#3b2a2f"/><rect y="520" width="1000" height="10" fill="#5a3f3a"/><polygon points="262,392 312,404 440,560 190,560" fill="url(#lg)"/><ellipse cx="170" cy="522" rx="44" ry="9" fill="#10122b"/><path d="M170 516L214 404L276 352" stroke="#2d3270" stroke-width="10" fill="none" stroke-linecap="round"/><polygon points="248,336 322,366 296,410 222,380" fill="#ffd95a" stroke="#0d0f24" stroke-width="3"/>' +
  '<g stroke="#0d0f24" stroke-width="3"><rect x="470" y="478" width="130" height="62" fill="#ff7a6b" transform="rotate(-3 535 509)"/><rect x="490" y="462" width="130" height="62" fill="#38bdf8" transform="rotate(2 555 493)"/><rect x="480" y="446" width="130" height="62" fill="#a9b3ff" transform="rotate(-1 545 477)"/><rect x="700" y="486" width="44" height="46" rx="6" fill="#fff6dd"/><rect x="662" y="578" width="120" height="80" fill="#fff" transform="rotate(-8 722 618)"/></g><path d="M744 498h14v22h-14" stroke="#fff6dd" stroke-width="6" fill="none"/><g fill="none" stroke="#1b1e42" stroke-width="2" transform="rotate(-8 722 618)"><ellipse cx="722" cy="618" rx="8" ry="11"/><ellipse cx="722" cy="618" rx="16" ry="21"/><ellipse cx="722" cy="618" rx="24" ry="31"/></g><circle cx="860" cy="590" r="30" fill="#8f9bff" fill-opacity=".35" stroke="#f3efe6" stroke-width="7"/><path d="M882 612L920 652" stroke="#f3efe6" stroke-width="10" stroke-linecap="round"/></svg>';

// Badan karakter (a berisi ciri: g = kacamata, c = topi, b = tas)
const BODY = (c, a) =>
  (a.includes("b")
    ? '<rect x="6" y="0" width="9" height="21" rx="3" fill="#1b6fd8" stroke="#0d0f24" stroke-width="1.5"/>'
    : "") +
  '<rect class="l1" x="-8" y="22" width="6" height="9" rx="2" fill="#2d3270"/><rect class="l2" x="2" y="22" width="6" height="9" rx="2" fill="#2d3270"/><rect x="-9" y="-2" width="18" height="27" rx="8" fill="' +
  c +
  '" stroke="#0d0f24" stroke-width="1.5"/><circle cy="-12" r="9" fill="#f6d9c0" stroke="#0d0f24" stroke-width="1.5"/><path d="M-9 -13a9 9 0 0 1 18 0z" fill="#2d3270"/>' +
  (a.includes("c")
    ? '<path d="M-10 -16Q0 -28 10 -16Z" fill="#fff" stroke="#0d0f24" stroke-width="1.5"/><rect x="-3" y="-17" width="15" height="3" fill="#fff" stroke="#0d0f24" stroke-width="1.2"/>'
    : "") +
  (a.includes("g")
    ? '<rect x="-8" y="-14" width="7" height="5" rx="2" fill="#0d0f24"/><rect x="1" y="-14" width="7" height="5" rx="2" fill="#0d0f24"/>'
    : "");

// Kartu satu karakter lengkap dengan namanya
const AV = (c, a, n) =>
  '<span style="display:inline-block;text-align:center;margin:4px 8px"><svg viewBox="-20 -32 40 76" width="56" height="106">' +
  BODY(c, a) +
  '</svg><br><u data-v="' +
  n +
  '">' +
  n +
  "</u></span>";

// Deretan kartu karakter untuk halaman foto
const GAL = (l) => l.map((a) => AV(a[1], a[2], a[0])).join("");

// Gambar komputer di layar CCTV
const PC = (x, l, on) =>
  '<rect x="' +
  (x - 26) +
  '" y="118" width="52" height="36" rx="4" fill="' +
  (on ? "#1f5f9e" : "#0f1129") +
  '" stroke="#0d0f24" stroke-width="2"/><rect x="' +
  (x - 36) +
  '" y="160" width="72" height="10" fill="#7b5e4b"/><text x="' +
  x +
  '" y="112" text-anchor="middle" font-size="10" fill="#5b5f8f">' +
  l +
  "</text>";
