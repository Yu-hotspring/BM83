# BM83 プロジェクトの3Dモデル

PCB内の参照はすべて `${KIPRJMOD}/3dmodels/…step`。このフォルダをプロジェクトと一緒に移動すれば参照を維持できます。対象は今回指定された13部品です。

|部品|モデル|根拠・注意|
|---|---|---|
|RV301–303、RV401|RV_2C_RK09712200HA.step|回路図にメーカー型番なし。手元のSamacSys製ALPS RK09712200HAモデルを使用。6端子の2.5 mmピッチ、9.5 mm幅の本体が一致するため推定で採用。シャフト先端はフットプリント原点から25 mm（シルクの20 mmより5 mm長い）。実装予定品の軸長は要照合。|
|U202|Microchip_BM83.step|回路図のMicrochip BM83に対応する手元のBM83SM1-00ABモデル。基板接触面をZ=0へ調整。|
|J101|USB_C_HRO_TYPE-C-31-M-12.step|フットプリント型番と一致するai03公開モデル。シェル取付脚を基準に位置・向きを調整。|
|R110|CEMENT_RESISTOR_5W.step|回路図は51 Ω、独自5Wフットプリントで型番なし。22×10×9 mm本体、28 mm端子ピッチの汎用モデルを新規作成。高さは公称値で、実部品の確定寸法ではない。|
|K101|G2R-1-E-DC24.step|回路図の値G2R-1-E 24Vに対応する手元のSamacSysモデル。ユーザー確認済み。G2RL用に設定されていた参照を交換。|
|J104|Keystone_3557-2_simplified.step|3557-2のメーカー図面をもとに作成。19.8×6.8×7.4 mm、脚長2.8 mm。端子配置は既存フットプリント13.47×3.4 mmに合わせた。接点ばね・樹脂細部は簡略化。ヒューズ本体は含まない。|
|PS101、PS102|M78AR-0.5.step|MINMAXのM78AR-0.5シリーズ公式STEP。05と033は同一ケース。上下反転・端子列位置を調整。|
|J102、J105|JST_B2P-VH.step|PCB-3D公開のB2P-VH(LF)(SN)モデル。3.96 mmピッチ、メーカー図面の外形と照合し位置・向きを調整。|

## 入手先と原本

- MINMAX公式製品ページ: https://www.minmaxpower.com/en/product/M78AR-0.5
- MINMAX公式STEP ZIP: https://www.minmaxpower.com/storage/media/Product-MINMAX/M78AR-0.5/M78AR-0_5_3D_Mechanical.zip
- USB-C STEP: https://github.com/ai03-2725/Type-C.pretty/blob/master/HRO%20%20TYPE-C-31-M-12.step
- JST STEP: https://www.pcb-3d.com/wordpress/models/jst_b2p-vhlfsn_hdr_th_3-96mm_pitch_v/
- JSTメーカー図面: https://www.jst-mfg.com/product/pdf/eng/eVH.pdf
- Keystoneメーカー製品ページ: https://www.keyelco.com/product.cfm/product_id/296
- Keystoneメーカー図面: https://www.keyelco.com/product-pdf.cfm?p=296
- 図面取得元（Keystoneカタログp.41の写し）: https://www.micro-semiconductor.com/datasheet/97-3557.pdf
- セメント抵抗の公称ケース寸法参考: https://www.yeso.com.tw/en/products.php?cid=11
- RK097、G2R、BM83の原本: ユーザーの既存 `Desktop/Robocon/LL` に保存されていたSamacSysモデル。再取得不要で利用。

`sources/` に取得原本と寸法資料を保存。外部モデルの権利は各提供元に帰属します。配置調整したモデルを含め、第三者モデルを独自のライセンスで再許諾するものではありません。

## 再生成

CadQuery 2.6以降の環境で `python 3dmodels/build_models.py` を実行すると、正規化した8種類のSTEPを再生成できます。単位はmm、PCB上面をZ=0、上方向を+Zとし、モデルYはKiCadフットプリントYと逆向きです。PCB側のオフセット・回転はすべて0、倍率は1です。

## 回路図の不整合（今回は変更しない）

K101は値欄がオムロンG2R-1-E 24Vですが、Manufacturer_Name/Manufacturer_Part_Number/Datasheet/Heightなどの補助属性がDURAKOOL DG85Bのままです。ユーザーの指定によりG2Rの3Dモデルを使用しています。部品調達に補助属性を使う際は別途修正が必要です。

RVとR110は実装品のメーカー型番が回路図にないため、筐体の厳密な干渉検討には現物寸法の確認が必要です。
