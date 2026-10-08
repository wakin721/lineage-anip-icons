# 小黑盒图像生成重绘

使用内置 image_gen，非 CLI。最终 PNG 为 `heybox-redrawn-v1.png`，1254 × 1254 RGBA；原始 alpha 保留。第一轮白色稿出现噪点，被弃用。第二轮为最终深紫色稿。

## 第一轮提示词

Use case: precise-object-edit. Asset type: high-resolution Android adaptive app icon foreground for 小黑盒 (Heybox). Input image 1 is the exact logo reference: a low-resolution 50 by 50 pixel transparent monochrome notification glyph. Reconstruct and redraw this SAME glyph at high definition, with precise clean geometric edges, preserving the recognizable two interlocking angular ribbon-like halves, their topology, proportions, placement, and transparent gaps. Do not invent a different brand mark. Enlarge the source logically by reconstructing smooth edges rather than enlarging source pixels. Output a single centered solid WHITE monochrome logo on a truly TRANSPARENT canvas, without any background color, circle, frame, text, shadow, glow, blur, texture, gradients or 3D. Use clean straight line segments and small smooth corner joins where the reference indicates them. Keep the silhouette approximately 44 percent of the square canvas width and 56 percent of the square canvas height, centered, with generous uniform clear space suitable for an adaptive icon foreground; this padding is deliberate to prevent an oversized desktop symbol. Keep all negative spaces truly transparent. Produce the highest practical resolution, crisp antialiased edge only, flat logo asset.

## 第二轮提示词（最终）

Repair this logo asset. Image 1 is a failed reconstruction; image 2 is the exact small original Heybox logo reference. Keep the basic centered interlocking angular logo silhouette from image 1, but correct its gaps to match image 2. Replace all visible white regions with a perfectly uniform solid dark plum #703650. Remove every speckle, distressed region, hairline, outline, sketch mark and noisy edge. The only visible pixels must form TWO clean smooth flat angular ribbon shapes. All canvas outside those two shapes and all gaps between them must have clean transparent alpha, no mottling. Use an exact flat vector-like app icon style, with straight diagonal and vertical boundaries and very subtle corner rounding. Preserve image 2 logo identity and its open center gap; don't add motifs, lettering or decorative elements. Keep the logo centered occupying about 44% canvas width and 56% canvas height to avoid oversize after Android adaptive-icon masking. Single square transparent PNG, crisp high-definition silhouette, uniform dark plum fill, no white pixels, no gradient, no 3D, no shadows, no glow, no background, no circle. This is a technical clean icon asset, not an illustration.

## 模块接入

`tools/import_heybox_imagegen.py` 读取最终 PNG 的 alpha，转成两个闭合轮廓，过滤小噪点，归一化到原 50 × 50 视口。PNG 本身不改写。模块只使用派生矢量轮廓，颜色继续由 Android 主题决定；生成稿的颜色和透明度不作为模块填充。原 ANIP PNG 与通知四层透明度保留。此轮仅替换小黑盒桌面图形，其他 695 个图形维持 0.1.9。
