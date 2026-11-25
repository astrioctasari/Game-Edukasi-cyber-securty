// Jendela CCTV dan Foto TKP (hanya ada di level tertentu).

// Gambar satu sosok di layar
const chr = (c, n, a) =>
  '<g class="ch hs" data-n="' +
  n +
  '"><ellipse cy="27" rx="13" ry="4" fill="#0005"/>' +
  BODY(c, a) +
  '<text y="46" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" stroke="#0d0f24" stroke-width="3" paint-order="stroke">' +
  n +
  "</text></g>";

// ID animasi CCTV yang sedang berjalan
let raf = 0;

// Pasang Foto TKP (gambar diam)
function wireScene() {
  cancelAnimationFrame(raf);
  const S = LV[cur].sc,
    sv = $("#sv");
  sv.innerHTML =
    S.bg +
    S.ch
      .map(
        (c) =>
          '<g transform="translate(' +
          c[2][0] +
          "," +
          c[2][1] +
          ') scale(1.35)">' +
          chr(c[1], c[0], c[3] || "") +
          "</g>"
      )
      .join("") +
    S.bub
      .map((b) => {
        const c = S.ch.find((x) => x[0] == b[0]),
          w = b[1].length * 6.3 + 14;
        return (
          '<g transform="translate(' +
          (c[2][0] - w / 2) +
          "," +
          (c[2][1] - 70) +
          ')"><rect rx="6" height="18" width="' +
          w +
          '" fill="#fff" stroke="#0d0f24" stroke-width="2"/><text y="13" x="7" font-size="11" font-weight="700" fill="#1b1e42">' +
          b[1] +
          "</text></g>"
        );
      })
      .join("");
  $("#sl").textContent = S.cap;
  sv.onclick = (e) => {
    const g = e.target.closest(".ch");
    if (g) setPin(g.dataset.n, "Foto TKP");
  };
}

// Pasang pemutar CCTV: garis waktu, tombol putar, dan klik sosok
function wireCctv() {
  const S = LV[cur].cc,
    B = LV[cur].sc.bg.replace("TKP ·", "CCTV ·"),
    sv = $("#cv");
  cancelAnimationFrame(raf);
  let t = 0,
    play = false,
    last = 0;
  const [h, m, s0] = S.t0.split(":").map(Number),
    base = h * 3600 + m * 60 + s0,
    bw2 = (b) => b[3].length * 6.3 + 14;
  sv.innerHTML =
    B +
    S.ch.map((c) => chr(c[1], c[0], c[3] || "")).join("") +
    S.bub
      .map(
        (b, i) =>
          '<g id="cb' +
          i +
          '" style="display:none"><rect rx="6" height="18" width="' +
          bw2(b) +
          '" fill="#fff" stroke="#0d0f24" stroke-width="2"/><text y="13" x="7" font-size="11" font-weight="700" fill="#1b1e42">' +
          b[3] +
          "</text></g>"
      )
      .join("") +
    '<text id="ck" x="14" y="332" font-size="13" font-weight="800" font-family="monospace" fill="#d9483a"></text>';
  const pos = (k) => {
    for (let i = 0; i < k.length - 1; i++) {
      const a = k[i],
        b = k[i + 1];
      if (t >= a[0] && t <= b[0]) {
        const f = (t - a[0]) / (b[0] - a[0]);
        return [a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f, a[1] != b[1] || a[2] != b[2]];
      }
    }
    const l = k[k.length - 1];
    return [l[1], l[2], false];
  };
  const draw = () => {
    sv.querySelectorAll(".ch").forEach((g) => {
      const c = S.ch.find((x) => x[0] == g.dataset.n),
        p = pos(c[2]),
        w = p[2] ? Math.sin(t * 14) * 3 : 0;
      g.setAttribute(
        "transform",
        "translate(" +
          p[0] +
          "," +
          (p[1] + (p[2] ? Math.abs(Math.sin(t * 14)) * -2 : Math.sin(t * 5) * 0.8)) +
          ") scale(1.35)"
      );
      g.querySelector(".l1").setAttribute("transform", "translate(0," + w + ")");
      g.querySelector(".l2").setAttribute("transform", "translate(0," + -w + ")");
    });
    S.bub.forEach((b, i) => {
      const g = $("#cb" + i),
        p = pos(S.ch.find((x) => x[0] == b[2])[2]);
      g.style.display = t >= b[0] && t <= b[1] ? "" : "none";
      g.setAttribute("transform", "translate(" + (p[0] - bw2(b) / 2) + "," + (p[1] - 70) + ")");
    });
    const q = Math.floor(base + t),
      f = (n) => String(n).padStart(2, "0");
    $("#ck").textContent =
      "● REC " + f(Math.floor(q / 3600)) + ":" + f(Math.floor((q % 3600) / 60)) + ":" + f(q % 60);
    $("#cs").value = t;
    $("#cl").textContent = S.ev
      .filter((e) => e[0] <= t)
      .map((e) => "• " + e[1])
      .join("\n");
  };
  const loop = (n) => {
    if (play) {
      t = Math.min(S.dur, t + (n - last) / 1000);
      if (t >= S.dur) {
        play = false;
        $("#cp").textContent = "▶ Putar";
      }
    }
    last = n;
    draw();
    raf = requestAnimationFrame(loop);
  };
  raf = requestAnimationFrame(loop);
  $("#cp").onclick = () => {
    if (t >= S.dur) t = 0;
    play = !play;
    last = performance.now();
    $("#cp").textContent = play ? "⏸ Jeda" : "▶ Putar";
  };
  $("#cr").onclick = () => {
    t = 0;
    play = false;
    $("#cp").textContent = "▶ Putar";
  };
  $("#cs").oninput = (e) => {
    t = +e.target.value;
    play = false;
    $("#cp").textContent = "▶ Putar";
  };
  sv.onclick = (e) => {
    const g = e.target.closest(".ch");
    if (g) setPin(g.dataset.n, "CCTV");
  };
}
