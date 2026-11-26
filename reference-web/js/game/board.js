// Papan Bukti.

// Gambar Papan Bukti: langkah yang sudah selesai dan kartu pelaku
function board() {
  const pb = $("#pb");
  if (!pb) return;
  const n = TK.length,
    P = [
      [40, 22],
      [245, 22],
      [450, 22],
      [40, 128],
      [245, 128],
      [450, 128],
    ],
    C = LV[cur].cul,
    fin = ti >= n;
  let h = '<rect width="600" height="340" fill="#c8955a"/>';
  for (let i = 0; i < 70; i++)
    h +=
      '<circle cx="' +
      ((i * 97) % 600) +
      '" cy="' +
      ((i * 53) % 340) +
      '" r="1.6" fill="#a87440"/>';
  h += '<rect x="3" y="3" width="594" height="334" fill="none" stroke="#5a3f3a" stroke-width="6"/>';
  for (let i = 0; i < Math.min(ti, n) - 1; i++)
    h +=
      '<line x1="' +
      (P[i][0] + 55) +
      '" y1="' +
      (P[i][1] + 8) +
      '" x2="' +
      (P[i + 1][0] + 55) +
      '" y2="' +
      (P[i + 1][1] + 8) +
      '" stroke="#d9483a" stroke-width="2.5"/>';
  if (fin)
    h +=
      '<line x1="' +
      (P[n - 1][0] + 55) +
      '" y1="' +
      (P[n - 1][1] + 8) +
      '" x2="300" y2="240" stroke="#d9483a" stroke-width="2.5"/>';
  for (let i = 0; i < n; i++) {
    const x = P[i][0],
      y = P[i][1],
      ok = i < ti,
      v = ok ? String(got[i]) : "";
    h +=
      '<g transform="rotate(' +
      ((i % 3) - 1) * 2.5 +
      " " +
      (x + 55) +
      " " +
      (y + 42) +
      ')"><rect x="' +
      x +
      '" y="' +
      y +
      '" width="110" height="84" fill="' +
      (ok ? "#fff6dd" : "#d9d3c4") +
      '" stroke="#0d0f24" stroke-width="2"/>' +
      (ok
        ? '<text x="' +
          (x + 55) +
          '" y="' +
          (y + 34) +
          '" text-anchor="middle" font-size="10" font-weight="800" fill="#3d4bb8">' +
          (i + 1) +
          ". " +
          TK[i][0].toUpperCase() +
          '</text><text x="' +
          (x + 55) +
          '" y="' +
          (y + 58) +
          '" text-anchor="middle" font-size="13" font-weight="700" fill="#1b1e42">' +
          esc(v.length > 14 ? v.slice(0, 13) + "…" : v) +
          "</text>"
        : '<text x="' +
          (x + 55) +
          '" y="' +
          (y + 56) +
          '" text-anchor="middle" font-size="34" font-weight="800" fill="#a39c8a">?</text>') +
      '<circle cx="' +
      (x + 55) +
      '" cy="' +
      (y + 8) +
      '" r="5" fill="#d9483a"/></g>';
  }
  h +=
    '<rect x="230" y="232" width="140" height="102" fill="' +
    (fin ? "#fff6dd" : "#d9d3c4") +
    '" stroke="#0d0f24" stroke-width="2"/><circle cx="300" cy="240" r="5" fill="#d9483a"/>' +
    (fin
      ? '<text x="300" y="256" text-anchor="middle" font-size="11" font-weight="800" fill="#d9483a">' +
        C[0] +
        '</text><g transform="translate(300,288) scale(1.25)">' +
        BODY(C[2], C[3]) +
        '</g><text x="300" y="329" text-anchor="middle" font-size="12" font-weight="800" fill="#1b1e42">' +
        C[1] +
        "</text>"
      : '<text x="300" y="296" text-anchor="middle" font-size="40" font-weight="800" fill="#a39c8a">?</text><text x="300" y="322" text-anchor="middle" font-size="10" fill="#5b5f8f">Belum terungkap</text>');
  pb.innerHTML = h;
}
