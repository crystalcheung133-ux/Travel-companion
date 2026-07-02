import json, re, os, textwrap
from bs4 import BeautifulSoup
root='/mnt/data/v24work'
places=json.load(open('/mnt/data/places.json'))
# Updated addresses/hours from user Store Audit + live/review enrichment. Hours can still change by Oct.
updates={
'fusion': dict(address='Fusion Original Saigon Centre, 65 Lê Lợi, Bến Nghé, District 1, Ho Chi Minh City', hours='24 Hours', desc='Fusion Original Saigon Centre 係今次旅程嘅城市據點：第一郡核心、樓下直通 Saigon Centre / Takashimaya，四個人每日出入、寄放戰利品、返酒店補妝都非常方便。兩房兩衛令行程唔需要因為梳洗同收拾而互相等待，呢點對短途女生旅行特別重要。', signature=['2 Bedroom Suite：四人共享客廳，私隱同方便度平衡得好','直通 Takashimaya，雨天、酷熱或夜晚返酒店都安心','Maison Marou、超市、餐廳都在同一棟／附近，適合臨時補給'], worth=['Hotel 係 base，不代表每日都由酒店出發；網站路線會以當時上一站作交通提示。','最適合用作「回巢點」：午后小休、放低戰利品、晚餐前換裝。']),
'bakes': dict(address='16 Thảo Điền, An Khánh, Hồ Chí Minh 700000, Vietnam', hours='07:30–22:00', desc='Bakes Thảo Điền 係草田區很順路的法式甜點 stop。相比普通 cafe，Bakes 嘅重點係精緻甜點同 croissant 類 pastry，適合 Day 3 逛完 Thảo Điền 小店後，用一小時坐低補糖、吹冷氣、整理戰利品。', signature=['多款法式甜點與千層 croissant','冷氣座位，適合午后避暑','同 The Dreamers Bakery 很近，可二選一'], worth=['唔需要當成正式下午茶，4 人點 2–3 件 share 最剛好。','若當日太飽，可以外帶 pastry 留返酒店。']),
'cafe-apartments': dict(address='The Cafe Apartments, 42 Nguyễn Huệ, District 1, Ho Chi Minh City', hours='各店不同；大多約 09:00–22:00', desc='The Cafe Apartments 係阮惠步行街最有代表性的老公寓改造景點。白天入內是迷宮式小店與 cafe，夜晚外牆一格格招牌亮起，反而成為最經典的西貢夜景背景。今次 Day 1 將 Spa 同夜景安排在同一棟樓，動線很聰明：下午上樓放鬆，晚上食完飯回來影霓虹燈。', signature=['夜晚外牆最上鏡','每層都有不同 cafe、選物店、香氛小店','電梯可能收小額費用，亦可逐層行樓梯探索'], worth=['建議先搭到高層，再慢慢向下行，體力消耗較少。','不建議一入門就坐第一間；先逛一圈再決定。']),
'cong': dict(address='Cộng Cà Phê Tân Định, Hai Bà Trưng, District 3, Ho Chi Minh City', hours='約 07:00–23:00；出發前再確認', desc='Cộng Cà Phê Tân Định 最大賣點唔係咖啡本身，而係位置：粉紅教堂正對面／附近，適合打完卡後上樓坐低，用椰子咖啡或冰沙咖啡換一個俯瞰教堂角度。復古軍綠風裝潢亦好有越南味。', signature=['椰子咖啡／椰子冰沙咖啡','粉紅教堂視角','復古越南風格'], worth=['如果只想影教堂，停留 20–30 分鐘已足夠。','座位景觀視乎當日樓層與窗邊位置。']),
'marou': dict(address='Tòa nhà Saigon Centre, 65 Lê Lợi, Sài Gòn, Hồ Chí Minh 700000, Vietnam', hours='09:30–21:30', desc='Maison Marou 是越南精品朱古力品牌，今次最方便的分店就在 Saigon Centre / Fusion 附近。它適合兩種用途：一是旅行中段回酒店後飲杯熱朱古力，二是最後買手信。比起普通 souvenir，Marou 朱古力包裝靚、有越南產地特色，而且容易帶回澳洲。', signature=['熱朱古力、朱古力撻、bonbon','越南產地朱古力手信','包裝靚，送禮安全牌'], worth=['如果怕行李熱溶，最後一日或晚間買最好。','店內甜品偏濃郁，4 人 share 會比每人一份舒服。']),
'running-bean': dict(address='115 Hồ Tùng Mậu, Sài Gòn, Hồ Chí Minh 70000, Vietnam', hours='07:30–22:00', desc='The Running Bean 係一間比較現代、明亮、旅客友善的 Saigon cafe。今次放在 Day 4 早上，角色唔係 brunch，而係入 War Museum 前的 caffeine stop：坐低 30–45 分鐘，飲杯蛋咖啡或椰子咖啡，再開始比較沉重的人文行程。', signature=['越式蛋咖啡','椰子咖啡／冰沙咖啡','明亮現代空間'], worth=['早餐尖峰時段可能較多人，建議短坐即可。','Day 4 之後會有 Pizza 4P，不需要在這裡食太飽。']),
'bep-me-in': dict(address='136/9 Lê Thánh Tôn, Bến Thành, Hồ Chí Minh, Vietnam', hours='10:30–22:30', desc='Bếp Mẹ Ỉn 是 Michelin Bib Gourmand 越式家常菜，藏在市中心小巷內，氣氛比街邊小店舒服，但菜式仍然保留越南家庭菜與街頭味道。放在最後一日午餐很適合：不用太 formal，但又可以把 bánh xèo、椰子炒飯、越式小食一次過收尾。', signature=['Bánh Xèo 黃金煎餅','椰子炒飯','越式拼盤與家常菜'], worth=['入口在巷內，第一次去要跟 Google Maps 慢慢找。','多人 share 最好食，4 人比 2 人更適合。']),
'com-tam-moc': dict(address='85 Lý Tự Trọng, Bến Thành, Hồ Chí Minh, Vietnam', hours='09:00–21:30', desc='Cơm Tấm Mộc 是碎米飯的舒服版：保留炭烤豬排香氣，但環境比街邊小店乾淨、有冷氣。Day 2 早上放在 Cooking Class 前，重點是試一口地道早餐，而不是食到太飽。', signature=['炭烤豬排碎米飯','魚露、蛋、酸菜配搭','冷氣環境比街邊舒服'], worth=['4 人點 2–3 份 share 已足夠，因為 10:00 還有 cooking class。','如果早上不餓，可以改成外帶咖啡。']),
'little-bear': dict(address='36 Nguyễn Bá Huân, An Khánh, Hồ Chí Minh 700000, Vietnam', hours='18:00–22:00；Monday closed', desc='Little Bear 是 Thảo Điền 近年非常受注目的小型 wine bar / modern Vietnamese bistro。餐廳空間不大，但氣氛輕鬆，料理不是傳統大碟越菜，而是以分享盤、細緻調味和年輕主廚風格去呈現越南味道。Day 3 逛完草田區再去，地理同氣氛都最順。', signature=['Michelin Selected / Young Chef 話題','小型空間，counter/table seating 氣氛親近','越南味道 + bistro 手法，適合 share plates'], worth=['星期一休息，必須訂位。','份量偏精緻，建議不要期待傳統大份量越菜。','不飲酒也可以去，重點是食物和氣氛。']),
'lune': dict(address='17/14 Lê Thánh Tôn, Sài Gòn, Hồ Chí Minh 70000, Vietnam', hours='Dinner service 17:00–22:30；Sunday closed', desc='LÚNE Restaurant & Bar 是現代法式／fusion fine dining 路線，位置在 Lê Thánh Tôn 小巷內，氣氛比傳統酒店 fine dining 更有城市感。它適合 Day 2 晚上：白天已經 cooking class + shopping + spa，夜晚需要一餐有儀式感但不會太沉重的 dinner。', signature=['Michelin Selected 話題餐廳','法式技巧結合越南／亞洲食材','Bar + restaurant 氣氛，適合四人換裝後晚餐'], worth=['建議提前 2–4 週預約，週日休息要留意。','Smart casual 已足夠，不需要太正式。','如果行街時間 delay，要預留回酒店換裝與 Grab 時間。']),
'omakase-tiger': dict(address='85/9 Phạm Viết Chánh, Thạnh Mỹ Tây, Hồ Chí Minh 700000, Vietnam', hours='Tue–Sun 17:30 / 20:00；Monday closed', desc='Omakase Tiger 最大賣點是「西貢景觀 + 8 座板前 + 價格相對友善」的組合。它不是傳統東京嚴肅壽司店，而是更有 Saigon rooftop 氣氛的 modern omakase。Day 1 選 17:30 場剛好遇上日落，食完再回阮惠步行街影 The Cafe Apartments 夜景，時間線很漂亮。', signature=['8-seat countertop，座位極少','17:30 日落場最有記憶點','約 10–14 道 omakase，價格比澳港日同類體驗低'], worth=['最新 IG 曾出現 temporarily closed 訊息，出發前必須再確認營業狀態。','建議用官方／TableCheck 或 Facebook Messenger 確認訂位。']),
'pho-sol': dict(address='Phở SOL Bến Thành, District 1, Ho Chi Minh City', hours='出發前再確認', desc='Phở SOL 是抵達後第一餐的好選擇：位置近第一郡，石鍋河粉上枱有儀式感，熱湯、牛肉、油條很適合剛落機後慢慢進入越南節奏。它比街邊河粉更乾淨舒服，適合四位媽媽第一餐先穩陣開局。', signature=['石鍋河粉','牛骨湯與牛肉配料','油條 quẩy 沾湯'], worth=['4 人可以點不同款式 share，不一定每人一碗。','第一日下機後不要排太多，食完留體力去景點和 spa。']),
'pho-vietnam': dict(address='14 Phạm Hồng Thái, Bến Thành, Hồ Chí Minh, Vietnam', hours='06:00–03:00', desc='Phở Việt Nam Bến Thành 是 Michelin Selected 河粉店，以 phở thố đá 石鍋河粉聞名。湯、牛肉和配料分開上，熱石鍋令湯從第一口到最後仍然滾熱。放在最後一日早餐，有一種「用一碗越南河粉收尾」的完整感。', signature=['Michelin Selected','Phở thố đá 石鍋河粉','湯保持高溫，牛肉即場燙熟'], worth=['熱門時段可能要等位，但流轉快。','湯很熱，慢慢食比較安全。']),
'pizza4ps': dict(address="Pizza 4P's Võ Văn Tần, Ho Chi Minh City", hours='出發前再確認', desc='Pizza 4P’s 是越南最成功的日式 pizza 品牌，重點是自家製芝士、窯烤 pizza 和穩定服務。Day 4 午餐安排它很合理：連續幾日越南菜後轉一餐西式 comfort food，而且 Võ Văn Tần 分店動線接 War Museum / District 3 很順。', signature=['House-made cheese','Burrata / 4-cheese pizza','Pasta 與 sharing dishes'], worth=['建議預約，尤其週末或 lunch peak。','不需要點太多，下午還有 11 Garmentory / spa / dinner。']),
'quan-thuy': dict(address='Quán Thuý 94, 94 Đinh Tiên Hoàng, District 1, Ho Chi Minh City', hours='出發前再確認；早餐/午餐較合適', desc='Quán Thuý 94 是蟹肉粉絲老店風格，適合 Day 3 早上先食一餐地道小店，再步行去粉紅教堂。它不是精緻 cafe，而是用蟹肉、粉絲、炸蟹春捲帶出很 Saigon 的早餐／早午餐感。', signature=['Miến cua 蟹肉粉絲','炸蟹肉春捲','Tân Định / Pink Church 動線順路'], worth=['環境偏地道，接受度要有心理準備。','建議早去，太晚可能部分款式售完。']),
'quince': dict(address='37bis Ký Con, Bến Thành, Hồ Chí Minh, Vietnam', hours='17:30–22:30', desc='Quince Saigon 是最後一晚很適合的 farewell dinner。它以 wood-fired cooking、charcoal grill 和開放式廚房聞名，菜式有火烤香氣但不會太難懂。氣氛成熟、燈光暗、服務穩定，適合四人旅行最後一晚坐低慢慢回味。', signature=['Wood-fired / charcoal-grilled dishes','Open kitchen / counter seats','成熟但不拘謹的 farewell dinner 氣氛'], worth=['如果想看廚房動作，可嘗試要求 counter seats。','燈光偏暗，影相未必最清楚，但氣氛很好。']),
'libe': dict(address='LIBÉ Nguyễn Trãi, 52 Nguyễn Trãi, Bến Thành, Hồ Chí Minh, Vietnam', hours='09:30–21:30', desc='LIBÉ 是越南最易入手的本地女裝品牌之一，風格偏 casual chic，像「日常但有一點設計感」的衣櫃單品。放在 Day 2 shopping 起點很合理，因為 Nguyễn Trãi 一帶同類品牌集中，試完 LIBÉ 就可以順住路線慢慢掃。', signature=['Casual chic 女裝','上班、旅行、日常都易穿','多層店面，款式更新快'], worth=['記得上不同樓層，唔好只睇地下。','尺寸可能偏亞洲版型，最好試身。']),
'dauple': dict(address="Dauple by Ka's, 70 Phạm Hồng Thái, Bến Thành, Hồ Chí Minh, Vietnam", hours='09:30–21:30', desc='Dauple by Ka’s 偏成熟、優雅、度假感，適合想買一兩件「比普通 fast fashion 更有質感」的媽媽。亞麻、真絲、柔和色調和寬鬆剪裁會比街頭品牌更耐看。', signature=['亞麻／真絲質感','成熟優雅剪裁','適合旅行 resort / dinner look'], worth=['價位通常比普通本地品牌高少少，但勝在質感。','如果只想買年輕街頭款，可留時間給 The New Playground。']),
'nosbyn': dict(address='Nosbyn, 9 Phan Chu Trinh, Bến Thành, Ho Chi Minh City', hours='10:00–21:00', desc='NOSBYN 是越南本地較成熟的極簡女裝品牌，重點不是花巧，而是布料、剪裁和耐穿度。它適合買襯衫、連身裙、外套等 timeless 單品，風格像 COS 的簡潔版，但線條更女性化。', signature=['Minimal / timeless 女裝','布料質感與剪裁較穩','Office、旅行、日常都可重複穿'], worth=['顏色偏 neutral，啱鍾意低調質感的人。','熱門尺碼可能不齊，看到喜歡要即試。']),
'new-playground': dict(address='26 Lý Tự Trọng, Sài Gòn, Hồ Chí Minh 700000, Vietnam', hours='10:00–21:00', desc='The New Playground 是多品牌集合地，像地下版的本地設計師小商場。它很適合「時間有限但想一次看多幾個越南品牌」的情況，streetwear、配飾、年輕女裝都有。', signature=['多個越南本地品牌集中','冷氣環境，適合下午避暑','Streetwear 到 accessories 都有'], worth=['店多但不是每間都精緻，當作快速掃街最有效率。','如果時間 delay，可以只逛這裡，不逐間 boutique 追。']),
'saigon-concept': dict(address='14 Trần Ngọc Diện, P. Phú Thuận, An Khánh, Hồ Chí Minh 700000, Vietnam', hours='09:00–18:00', desc='Saigon Concept 是 Thảo Điền 很適合慢逛的 lifestyle compound：紅磚庭園、棉麻服飾、家居選物與小型品牌集中在同一區。Day 3 到草田區後先放慢節奏，由這裡開始很舒服。', signature=['庭園式複合空間','DESIGNED BY SISI / lifestyle 選物','適合拍照與慢逛'], worth=['下午早段去比較好，部分小店可能較早關。','重點是氛圍，不一定每間都要買。']),
'ohquao': dict(address='19 Đường Số 38, P. Thảo Điền, Quận 2, TP. Hồ Chí Minh', hours='10:00–20:00', desc='OHQUAO 是比較有藝術感的 Thảo Điền 小店，適合找明信片、香氛、手工小物和不太 mass-market 的 souvenir。比起商場手信，這裡更像旅行中途發現的小寶物。', signature=['在地藝術家小物','明信片、香氛、家居手信','適合買輕便 souvenir'], worth=['不要預期大型店鋪，這類小店重點是慢慢看。','適合安排在 Mộc Hương Spa 前後順路逛。']),
'garmentory': dict(address='11 Garmentory, Trần Quang Diệu, District 3, Ho Chi Minh City', hours='出發前再確認', desc='11 Garmentory 是 Day 4 District 3 逛街線的重點，風格偏本地設計、質感小眾，不是大量連鎖品牌。配合 Trần Quang Diệu 一帶的 cafe / boutique 氣氛，適合慢慢試衫、感受西貢比較安靜的時髦街區。', signature=['本地設計師選物','女裝／生活風格小店感','District 3 氣氛比 D1 更 local'], worth=['小店營業時間可能變動，出發前再查 IG。','如果當日博物館或午餐 delay，可以保留 11 Garmentory 作主站，其他小店自由取捨。']),
'push-push': dict(address='20 Nguyễn Văn Nguyễn, Tân Định, Hồ Chí Minh 700000, Vietnam', hours='09:30–21:30', desc='Push Push Official 走比較年輕、streetwear、褲款和休閒風格，適合想幫高瘦男生或喜歡寬鬆街頭感的人找褲。今次放在粉紅教堂附近作 optional stop，如果當日時間或店舖狀態不穩，可以直接 skip。', signature=['Streetwear / casual pants','年輕感、寬鬆剪裁','粉紅教堂附近可順路'], worth=['這類品牌 IG 資訊可能比 Google 準，出發前查 IG 最穩。','不是每位媽媽都會啱，可作分組自由逛。']),
'nha-suga': dict(address='Spa Nhà Suga Premium, The Cafe Apartments, 42 Nguyễn Huệ, District 1, Ho Chi Minh City', hours='出發前再確認', desc='Spa Nhà Suga Premium 的賣點是 head spa / scalp care，而不是傳統全身按摩。安排在 Day 1 下午很聰明：剛落機、頭皮和肩頸繃緊，做完再吹好頭髮，晚上去 Omakase Tiger 會精神很多。', signature=['Korean-style head spa / scalp care','肩頸放鬆','位於 The Cafe Apartments，同日夜景動線順'], worth=['評論提過可能 overbook，出發前務必 WhatsApp 確認。','做完頭髮要確認有足夠時間吹乾再去晚餐。']),
'moc-kim': dict(address='Mộc Kim Spa, 12L Nguyễn Thị Minh Khai, Sài Gòn, Hồ Chí Minh, Vietnam', hours='08:30–21:00', desc='Mộc Kim Spa 適合 Day 2 shopping 後做足底＋草本洗頭。它比一般按摩店多一點儀式感，適合逛完 Nguyễn Trãi / Vincom 後放低戰利品、休息雙腳，再回酒店換裝去 LÚNE。', signature=['越式草本洗頭','足底穴位按摩','可作 shopping 後回復站'], worth=['最好預約 2 小時 package，才不會太趕。','如果買了很多東西，先問是否可暫存戰利品。']),
'moc-huong': dict(address='61 Xuân Thủy, Thủ Đức, Hồ Chí Minh 700000, Vietnam', hours='09:00–22:00', desc='Mộc Hương Wellness Thảo Điền 走高級 villa spa 路線，環境比普通按摩店更度假。Day 3 逛草田區後在這裡做熱石／精油按摩，再去 Little Bear，整日節奏會很一致：慢、綠意、輕奢。', signature=['Villa-style spa setting','熱石／精油按摩','Thảo Điền 動線極順'], worth=['比市區普通 spa 價位高，但環境感更好。','做完按摩去 Little Bear 只需短 Grab，唔需要返 D1 再出來。']),
'temple-leaf': dict(address='74/1 Hai Ba Trung St., Ben Nghe Ward, District 1', hours='10:00–23:30', desc='Temple Leaf Spa Land 是行完 Day 4 人文 + shopping 後的腳底救援站。它的位置在市中心，適合不想再拉遠車程、只想實用地按腳、放鬆肩頸的人。', signature=['足底按摩','熱石／身體按摩','市中心位置方便'], worth=['重點是實用和位置，不是最奢華 spa。','晚飯前做 60–90 分鐘最剛好。']),
'ha-spa': dict(address='334 Nguyễn Trọng Tuyển, Tân Sơn Hòa, Hồ Chí Minh 700000, Vietnam', hours='08:30–22:00', desc='Hạ Spa 是最後一日飛機前的 airport-side spa。最大優勢是距離新山一機場近、可寄存行李，適合在搭夜機前洗頭、按摩、整理狀態，不用一身汗上機。', signature=['近機場','行李寄存','洗頭 + 全身放鬆 package'], worth=['最後一日時間要保守，不要排太晚。','預約時確認行李寄存、吹髮、叫車到機場時間。']),
'post-office': dict(address='Saigon Central Post Office, 2 Công xã Paris, Bến Nghé, District 1, Ho Chi Minh City', hours='Mon–Fri 07:00–17:00；Sat 07:00–18:00；Sun 08:00–18:00', desc='西貢中央郵政局是最容易安排、最有法式殖民建築感的經典景點。金黃色拱頂、古老地圖、木製電話亭都很上鏡，而且仍然是運作中的郵局。Day 1 放在抵達後不會太累，因為它和紅教堂、書街三點幾乎連在一起。', signature=['金黃色拱頂大廳','法式殖民建築','可買明信片／郵票'], worth=['免費入場，停留 20–30 分鐘已夠。','人多時先拍建築細節，不一定要等無人全景。']),
'notre-dame': dict(address='Notre-Dame Cathedral Basilica of Saigon, Công xã Paris, Bến Nghé, District 1, Ho Chi Minh City', hours='外觀打卡；內部開放情況出發前確認', desc='西貢聖母聖殿主教座堂是中央郵政局對面的紅磚地標。近年常有修復工程，重點應放在外觀打卡與和郵政局／書街形成一個短小經典路線，不建議專程安排太長時間。', signature=['紅磚外觀','郵政局對面','經典 D1 地標合照'], worth=['內部是否開放常受工程／宗教活動影響，當作外觀景點最穩。','中午光線硬，早上或傍晚拍照較舒服。']),
'book-street': dict(address='Nguyễn Văn Bình Book Street, Bến Nghé, District 1, Ho Chi Minh City', hours='Mon–Fri 08:00–21:00；Sat–Sun 08:00–21:30', desc='Nguyễn Văn Bình Book Street 夾在郵政局與紅教堂旁邊，是短短一條步行文化街。書店、咖啡、文創攤位集中，適合在 Day 1 三大景點中作一個較輕鬆的過渡位。', signature=['步行書街','書店、文創、咖啡小攤','與郵政局／紅教堂相連'], worth=['不是大型景點，停留 20–40 分鐘即可。','若太熱，可以只穿過拍照，不必硬逛每間店。']),
'pink-church': dict(address='Tan Dinh Church, 289 Hai Bà Trưng, Ward 8, District 3, Ho Chi Minh City', hours='外觀打卡；內部開放情況出發前確認', desc='新定教堂／粉紅教堂是 Saigon 最容易出片的地標之一。粉紅色外牆本身已經很有記憶點，配對面 Cộng Cà Phê 的樓上視角，可以一次拍到近景和俯瞰全景。', signature=['粉紅外牆','對面 cafe 視角','Tân Định 街區順路早餐'], worth=['內部開放不穩，當作外觀打卡最實際。','早上光線和人流通常較友善。']),
'war-museum': dict(address='War Remnants Museum, 28 Võ Văn Tần, District 3, Ho Chi Minh City', hours='07:30–17:30', desc='戰爭遺跡博物館是今次最沉重但最值得保留的人文景點。展覽以照片、文字和戰爭後果為主，內容不輕鬆，但能讓整個旅程不只是吃喝購物，也真正理解這座城市的歷史厚度。', signature=['越戰相關照片與史料','館內有冷氣，適合上午安排','與 District 3 / Pizza 4P’s 動線順'], worth=['建議預留 90–120 分鐘，比「打卡景點」需要更多情緒空間。','看完可安排 Pizza 4P’s 或 cafe 作心理緩衝。']),
'fine-arts': dict(address='Ho Chi Minh City Museum of Fine Arts, 97A Phó Đức Chính, District 1, Ho Chi Minh City', hours='08:00–17:00', desc='胡志明市美術館是一座黃色法式大宅，比起展品本身，建築、樓梯、彩色玻璃、舊式地磚和復古感更容易令人留下印象。Day 5 上午安排它很適合：節奏慢、拍照靚、又不會太消耗體力。', signature=['黃色法式建築','彩色玻璃、樓梯、復古地磚','適合王家衛感照片'], worth=['館內部分位置沒有強冷氣，早上去較舒服。','建議停留 60–90 分鐘。']),
'cooking': dict(address='Saigon Cooking Class, 74 Hai Bà Trưng, Bến Nghé, District 1, Ho Chi Minh City', hours='10:00–13:00（固定課程）', desc='Saigon Cooking Class 是 Day 2 的主活動：不是單純食 lunch，而是透過市場／食材／實作去理解越南菜。對四位媽媽來說，這種共同完成一餐的 activity 比普通景點更容易成為旅行記憶。', signature=['3 小時越菜體驗','親手做菜，即場享用作午餐','適合四人共同參與'], worth=['課程時間固定，Day 2 早上不要排太緊。','早餐要輕食，留肚食自己煮的午餐。'])
}
for k,u in updates.items():
    if k in places:
        places[k].update(u)
        # Add new structured editorial fields
        places[k]['highlights']=u.get('signature', places[k].get('signature', []))
        places[k]['tips']=u.get('worth', places[k].get('worth', []))
# ensure addresses already from audit for a few
# Replace JS PLACES
src=open(os.path.join(root,'script.js')).read()
new_obj=json.dumps(places,ensure_ascii=False,separators=(',',':'))
src=re.sub(r'const PLACES=\{[\s\S]*?\};\nconst CATEGORIES=', 'const PLACES='+new_obj+';\nconst CATEGORIES=', src)
# Replace modal content labels Signature/Worth Knowing -> Highlights/Good to Know and show paragraph
src=src.replace('<h3>Signature</h3><ul>${sig}</ul>','<h3>Highlights</h3><ul>${sig}</ul>')
src=src.replace('<h3>Worth Knowing</h3><ul>${worth}</ul>','<h3>Good to Know</h3><ul>${worth}</ul>')
open(os.path.join(root,'script.js'),'w').write(src)

def make_sections(key,g):
    desc=g.get('desc','')
    sig=g.get('signature',[])
    worth=g.get('worth',[])
    html=f'''<section class="prose-block guide-overview"><h2>Overview</h2><p>{desc}</p></section>'''
    if sig:
        html += '<section class="prose-block"><h2>Highlights</h2><ul>' + ''.join(f'<li>{x}</li>' for x in sig) + '</ul></section>'
    if worth:
        html += '<section class="prose-block"><h2>Good to Know</h2><ul>' + ''.join(f'<li>{x}</li>' for x in worth) + '</ul></section>'
    return html
for key,g in places.items():
    path=os.path.join(root, key+'.html')
    if not os.path.exists(path):
        continue
    soup=BeautifulSoup(open(path).read(),'html.parser')
    # update quick info values
    q=soup.select_one('section.quick-info-card')
    if q:
        values=q.select('.quick-info-value')
        vals=[g.get('address',''),g.get('hours',''),g.get('price',''),g.get('transport','Grab / walk depending on current route')]
        for v,txt in zip(values, vals): v.string=txt
        a=q.select_one('a.map-button')
        if a: a['href']=g.get('maps','#')
    # replace prose blocks immediately after quick info until before other content (we can replace all old prose blocks after main except page hero / quick info)
    main=soup.select_one('main.content-page')
    if main:
        # remove existing prose-block sections
        for sec in list(main.select('section.prose-block')):
            sec.decompose()
        frag=BeautifulSoup(make_sections(key,g),'html.parser')
        # append after quick info
        q=soup.select_one('section.quick-info-card')
        if q:
            for sec in reversed(list(frag.contents)):
                q.insert_after(sec)
    open(path,'w').write(str(soup))
# Add CSS polish for detailed guides and compact days
css=open(os.path.join(root,'styles.css')).read()
add='''\n/* v2.4 content structure: detailed Guide, compact Days */\n.guide-overview p{font-size:1.02rem;line-height:1.78;}\n.prose-block h2{margin-bottom:10px;}\n.prose-block ul{line-height:1.75;}\n.journey-note,.next-hop{display:flex;gap:10px;align-items:flex-start;background:#fff7eb;border:1px solid rgba(166,119,76,.22);border-radius:18px;padding:10px 12px;margin:10px 0;color:#5b4636;font-weight:700;}\n.day-lite-note{font-size:.92rem;color:#7a6a5d;margin-top:4px;}\n@media(max-width:600px){.guide-overview p{font-size:.98rem;line-height:1.65}.prose-block{padding:18px!important}.timeline-card p,.day-card p{font-size:.94rem;line-height:1.45}}\n'''
if 'v2.4 content structure' not in css: css += add
open(os.path.join(root,'styles.css'),'w').write(css)
# Days: add a short helper line after headings about details in guide; don't destroy master content yet.
for fname in ['day1.html','day2.html','day3.html','day4.html','day5.html']:
    path=os.path.join(root,fname)
    txt=open(path).read()
    if 'day-lite-note' not in txt:
        txt=txt.replace('<main class="content-page">','<main class="content-page"><div class="day-lite-note">Days 頁以即場導航為主；詳細背景、必點同注意事項已移到 Guide。</div>',1)
    open(path,'w').write(txt)
# Release notes
notes='''# Saigon Companion v2.4 — Content Structure Clean-up\n\n## Main direction\n- Guide pages are now the detailed reading layer: Overview, Highlights, Good to Know.\n- Days pages stay as the fast travel layer: time, next stop, maps, and short notes.\n- Address fields follow the updated Store Audit provided by Crystal.\n- Attraction opening hours updated where reliable, with “check before visit” kept for churches / variable openings.\n\n## Guide editorial updates\n- Added richer guide descriptions using master itinerary context plus live review / official-source style information.\n- Added practical “Good to Know” notes: booking, best use in route, portion expectations, whether it is mostly photo / food / shopping value.\n- Removed unnecessary “Why We Picked This”. The selection is already Crystal’s curation.\n\n## QA notes\n- Omakase Tiger has a live-status caution because one current Instagram result indicates temporary closure; reconfirm before booking.\n- Boutique and spa hours should be checked again closer to October.\n- Churches remain treated as exterior-photo stops unless internal opening is confirmed.\n'''
open(os.path.join(root,'RELEASE_NOTES_v2.4.md'),'w').write(notes)
# Save enriched audit JSON for future
open(os.path.join(root,'GUIDE_CONTENT_AUDIT_v2.4.json'),'w').write(json.dumps(places,ensure_ascii=False,indent=2))
