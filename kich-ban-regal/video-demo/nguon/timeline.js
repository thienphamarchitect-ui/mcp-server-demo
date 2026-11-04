// Mọi mốc tính bằng giây trên timeline tổng. Nguồn: phân tích silencedetect của voice.
window.TL = {
  fps: 30, total: 55.6, drop: 29.13,
  vo: [ // [file, start, srcFrom, srcTo]
    ['f1.wav', 0.25, 0, null], ['f2.wav', 4.58, 0, null], ['f3.wav', 10.77, 0, null],
    ['f4.wav', 15.80, 0, null], ['f5.wav', 20.41, 0, null], ['f6.wav', 26.16, 0, 2.2],
    ['f6.wav', 28.96, 2.2, null], ['f7.wav', 33.39, 0, null], ['f8.wav', 41.84, 0, null],
    ['f9.wav', 48.16, 0, null]
  ],
  bgs: [ // ảnh nền: [src, in, out, kenburns dir]
    ['assets/tt_ifc_img1.png', 0, 4.6, 1], ['DARK', 4.4, 10.9, 0],
    ['MAP', 10.6, 13.0, 0], ['assets/vnf_img0.png', 12.8, 16.0, -1],
    ['MAP', 15.8, 17.1, 0], ['assets/tt_ifc_img0.png', 16.9, 20.6, 1],
    ['MAP', 20.4, 22.0, 0], ['assets/cafeland_img0.png', 21.8, 26.3, -1],
    ['MAP', 26.1, 33.6, 0], ['assets/tt_regal_img0.png', 33.3, 42.0, 1],
    ['assets/tcct_img0.png', 41.8, 45.2, -1], ['assets/tcct_img2.png', 45.0, 48.4, 1],
    ['assets/tt_bg_img0.png', 48.1, 55.6, -1]
  ],
};
