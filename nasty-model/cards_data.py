# All important cards 2015-2026 (chase cards, SIR, ALT, IR, Gold, Full Art, etc.)

USD_CAD = 1.364
def u(v): return round(v * USD_CAD, 2)

ALL_CARDS = [
    # ═══════════════════════════════════════════
    # XY BASE (2014-2015)
    # ═══════════════════════════════════════════
    {"id":"XY-140","name":"Xerneas (Full Art)","set":"XY","rarity":"FA","tier":"B","price":u(8),"p1":u(7.9),"p7":u(7.5),"p30":u(6.5),"sat":0.10,"arb":0.20,"vel":0.20,"whale":0.15,"cross":0.40,"soc":0.25,"rep":0.50,"stab":0.55},
    {"id":"XY-141","name":"Yveltal (Full Art)","set":"XY","rarity":"FA","tier":"B","price":u(10),"p1":u(9.8),"p7":u(9.2),"p30":u(8.0),"sat":0.09,"arb":0.22,"vel":0.22,"whale":0.18,"cross":0.42,"soc":0.28,"rep":0.48,"stab":0.55},
    {"id":"XY-142","name":"Sylveon (Full Art)","set":"XY","rarity":"FA","tier":"A","price":u(18),"p1":u(17.5),"p7":u(16.0),"p30":u(13.0),"sat":0.08,"arb":0.30,"vel":0.30,"whale":0.28,"cross":0.55,"soc":0.40,"rep":0.45,"stab":0.60},

    # ═══════════════════════════════════════════
    # FLASHFIRE (2014)
    # ═══════════════════════════════════════════
    {"id":"FLF-107","name":"Charizard EX (Full Art)","set":"FLF","rarity":"FA","tier":"S","price":u(45),"p1":u(44),"p7":u(40),"p30":u(32),"sat":0.07,"arb":0.45,"vel":0.45,"whale":0.50,"cross":0.80,"soc":0.60,"rep":0.35,"stab":0.65},
    {"id":"FLF-100","name":"Charizard EX","set":"FLF","rarity":"EX","tier":"S","price":u(28),"p1":u(27.5),"p7":u(25),"p30":u(20),"sat":0.08,"arb":0.38,"vel":0.40,"whale":0.42,"cross":0.78,"soc":0.55,"rep":0.38,"stab":0.62},

    # ═══════════════════════════════════════════
    # ROARING SKIES (2015)
    # ═══════════════════════════════════════════
    {"id":"ROS-096","name":"Rayquaza EX (Full Art)","set":"ROS","rarity":"FA","tier":"S","price":u(35),"p1":u(34),"p7":u(31),"p30":u(24),"sat":0.07,"arb":0.42,"vel":0.42,"whale":0.45,"cross":0.75,"soc":0.55,"rep":0.38,"stab":0.62},
    {"id":"ROS-104","name":"Mega Rayquaza EX (Full Art)","set":"ROS","rarity":"FA","tier":"S","price":u(55),"p1":u(54),"p7":u(49),"p30":u(38),"sat":0.06,"arb":0.50,"vel":0.48,"whale":0.55,"cross":0.80,"soc":0.62,"rep":0.32,"stab":0.65},
    {"id":"ROS-061","name":"Mega Rayquaza EX (Colorless)","set":"ROS","rarity":"EX","tier":"S","price":u(40),"p1":u(39),"p7":u(36),"p30":u(28),"sat":0.07,"arb":0.44,"vel":0.44,"whale":0.48,"cross":0.78,"soc":0.58,"rep":0.35,"stab":0.63},

    # ═══════════════════════════════════════════
    # ANCIENT ORIGINS (2015)
    # ═══════════════════════════════════════════
    {"id":"AOR-093","name":"Lugia EX (Full Art)","set":"AOR","rarity":"FA","tier":"S","price":u(42),"p1":u(41),"p7":u(37),"p30":u(29),"sat":0.07,"arb":0.44,"vel":0.44,"whale":0.48,"cross":0.75,"soc":0.55,"rep":0.38,"stab":0.63},
    {"id":"AOR-083","name":"Gyarados EX (Full Art)","set":"AOR","rarity":"FA","tier":"A","price":u(22),"p1":u(21.5),"p7":u(19),"p30":u(15),"sat":0.08,"arb":0.32,"vel":0.32,"whale":0.30,"cross":0.55,"soc":0.40,"rep":0.42,"stab":0.58},

    # ═══════════════════════════════════════════
    # BREAKTHROUGH (2015)
    # ═══════════════════════════════════════════
    {"id":"BKT-123","name":"Mewtwo EX (Full Art)","set":"BKT","rarity":"FA","tier":"S","price":u(38),"p1":u(37),"p7":u(34),"p30":u(26),"sat":0.07,"arb":0.44,"vel":0.44,"whale":0.48,"cross":0.80,"soc":0.60,"rep":0.38,"stab":0.63},
    {"id":"BKT-130","name":"Mega Mewtwo Y EX (Full Art)","set":"BKT","rarity":"FA","tier":"S","price":u(48),"p1":u(47),"p7":u(43),"p30":u(33),"sat":0.06,"arb":0.48,"vel":0.48,"whale":0.52,"cross":0.82,"soc":0.62,"rep":0.35,"stab":0.65},
    {"id":"BKT-129","name":"Mega Mewtwo X EX (Full Art)","set":"BKT","rarity":"FA","tier":"S","price":u(42),"p1":u(41),"p7":u(37),"p30":u(29),"sat":0.07,"arb":0.45,"vel":0.45,"whale":0.50,"cross":0.80,"soc":0.60,"rep":0.36,"stab":0.63},

    # ═══════════════════════════════════════════
    # BREAKPOINT (2016)
    # ═══════════════════════════════════════════
    {"id":"BKP-122","name":"Gyarados EX (Full Art)","set":"BKP","rarity":"FA","tier":"A","price":u(20),"p1":u(19.5),"p7":u(18),"p30":u(14),"sat":0.08,"arb":0.30,"vel":0.30,"whale":0.28,"cross":0.52,"soc":0.38,"rep":0.42,"stab":0.58},

    # ═══════════════════════════════════════════
    # FATES COLLIDE (2016)
    # ═══════════════════════════════════════════
    {"id":"FCO-124","name":"Zygarde EX (Full Art)","set":"FCO","rarity":"FA","tier":"B","price":u(15),"p1":u(14.5),"p7":u(13),"p30":u(10),"sat":0.09,"arb":0.25,"vel":0.28,"whale":0.22,"cross":0.48,"soc":0.35,"rep":0.45,"stab":0.55},
    {"id":"FCO-122","name":"Mew EX (Full Art)","set":"FCO","rarity":"FA","tier":"A","price":u(30),"p1":u(29.5),"p7":u(27),"p30":u(21),"sat":0.07,"arb":0.38,"vel":0.38,"whale":0.35,"cross":0.65,"soc":0.48,"rep":0.40,"stab":0.60},

    # ═══════════════════════════════════════════
    # STEAM SIEGE (2016)
    # ═══════════════════════════════════════════
    {"id":"STS-114","name":"Volcanion EX (Full Art)","set":"STS","rarity":"FA","tier":"B","price":u(18),"p1":u(17.5),"p7":u(16),"p30":u(12),"sat":0.09,"arb":0.28,"vel":0.28,"whale":0.24,"cross":0.50,"soc":0.36,"rep":0.44,"stab":0.56},
    {"id":"STS-115","name":"Gardevoir EX (Full Art)","set":"STS","rarity":"FA","tier":"A","price":u(32),"p1":u(31),"p7":u(28),"p30":u(22),"sat":0.07,"arb":0.40,"vel":0.40,"whale":0.38,"cross":0.65,"soc":0.50,"rep":0.40,"stab":0.60},

    # ═══════════════════════════════════════════
    # EVOLUTIONS (2016)
    # ═══════════════════════════════════════════
    {"id":"EVO-098","name":"Charizard EX (Full Art)","set":"EVO","rarity":"FA","tier":"S","price":u(85),"p1":u(84),"p7":u(76),"p30":u(58),"sat":0.06,"arb":0.55,"vel":0.55,"whale":0.60,"cross":0.85,"soc":0.68,"rep":0.30,"stab":0.68},
    {"id":"EVO-020","name":"Charizard (Holo Rare)","set":"EVO","rarity":"HOLO","tier":"S","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.55,"cross":0.85,"soc":0.65,"rep":0.30,"stab":0.65},
    {"id":"EVO-108","name":"Mega Charizard X EX (Full Art)","set":"EVO","rarity":"FA","tier":"S","price":u(70),"p1":u(69),"p7":u(62),"p30":u(48),"sat":0.06,"arb":0.52,"vel":0.52,"whale":0.58,"cross":0.85,"soc":0.66,"rep":0.30,"stab":0.66},
    {"id":"EVO-107","name":"Mega Charizard Y EX (Full Art)","set":"EVO","rarity":"FA","tier":"S","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.56,"cross":0.84,"soc":0.65,"rep":0.30,"stab":0.65},
    {"id":"EVO-104","name":"Pikachu (Full Art)","set":"EVO","rarity":"FA","tier":"S","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.07,"arb":0.45,"vel":0.48,"whale":0.50,"cross":0.88,"soc":0.70,"rep":0.32,"stab":0.63},

    # ═══════════════════════════════════════════
    # SUN & MOON BASE (2017)
    # ═══════════════════════════════════════════
    {"id":"SUM-150","name":"Solgaleo GX (Full Art)","set":"SUM","rarity":"FA","tier":"B","price":u(18),"p1":u(17.5),"p7":u(16),"p30":u(12),"sat":0.09,"arb":0.27,"vel":0.28,"whale":0.22,"cross":0.50,"soc":0.36,"rep":0.44,"stab":0.56},
    {"id":"SUM-149","name":"Lunala GX (Full Art)","set":"SUM","rarity":"FA","tier":"B","price":u(16),"p1":u(15.5),"p7":u(14),"p30":u(11),"sat":0.09,"arb":0.25,"vel":0.26,"whale":0.20,"cross":0.48,"soc":0.34,"rep":0.45,"stab":0.54},

    # ═══════════════════════════════════════════
    # GUARDIANS RISING (2017)
    # ═══════════════════════════════════════════
    {"id":"GRI-149","name":"Tapu Lele GX (Full Art)","set":"GRI","rarity":"FA","tier":"A","price":u(28),"p1":u(27.5),"p7":u(25),"p30":u(19),"sat":0.08,"arb":0.35,"vel":0.35,"whale":0.32,"cross":0.55,"soc":0.42,"rep":0.42,"stab":0.58},
    {"id":"GRI-155","name":"Tapu Lele GX (Rainbow)","set":"GRI","rarity":"RR","tier":"A","price":u(35),"p1":u(34),"p7":u(31),"p30":u(24),"sat":0.07,"arb":0.40,"vel":0.40,"whale":0.38,"cross":0.58,"soc":0.45,"rep":0.40,"stab":0.60},

    # ═══════════════════════════════════════════
    # BURNING SHADOWS (2017)
    # ═══════════════════════════════════════════
    {"id":"BUS-149","name":"Charizard GX (Full Art)","set":"BUS","rarity":"FA","tier":"S","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.52,"vel":0.52,"whale":0.58,"cross":0.85,"soc":0.65,"rep":0.30,"stab":0.65},
    {"id":"BUS-150","name":"Charizard GX (Rainbow)","set":"BUS","rarity":"RR","tier":"S","price":u(85),"p1":u(84),"p7":u(76),"p30":u(58),"sat":0.05,"arb":0.56,"vel":0.55,"whale":0.62,"cross":0.87,"soc":0.68,"rep":0.28,"stab":0.67},
    {"id":"BUS-147","name":"Ho-Oh GX (Full Art)","set":"BUS","rarity":"FA","tier":"A","price":u(30),"p1":u(29.5),"p7":u(27),"p30":u(20),"sat":0.08,"arb":0.37,"vel":0.37,"whale":0.34,"cross":0.62,"soc":0.45,"rep":0.40,"stab":0.58},
    {"id":"BUS-148","name":"Darkrai GX (Full Art)","set":"BUS","rarity":"FA","tier":"A","price":u(22),"p1":u(21.5),"p7":u(19.5),"p30":u(15),"sat":0.08,"arb":0.30,"vel":0.30,"whale":0.28,"cross":0.55,"soc":0.38,"rep":0.43,"stab":0.56},
    {"id":"BUS-152","name":"Necrozma GX (Rainbow)","set":"BUS","rarity":"RR","tier":"B","price":u(18),"p1":u(17.5),"p7":u(16),"p30":u(12),"sat":0.09,"arb":0.27,"vel":0.27,"whale":0.22,"cross":0.48,"soc":0.34,"rep":0.45,"stab":0.54},

    # ═══════════════════════════════════════════
    # SHINING LEGENDS (2017)
    # ═══════════════════════════════════════════
    {"id":"SHL-027","name":"Shining Charizard","set":"SHL","rarity":"SHINING","tier":"S","price":u(180),"p1":u(178),"p7":u(160),"p30":u(125),"sat":0.05,"arb":0.65,"vel":0.60,"whale":0.70,"cross":0.88,"soc":0.70,"rep":0.20,"stab":0.75},
    {"id":"SHL-022","name":"Shining Mew","set":"SHL","rarity":"SHINING","tier":"S","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.06,"arb":0.55,"vel":0.52,"whale":0.58,"cross":0.78,"soc":0.60,"rep":0.25,"stab":0.70},
    {"id":"SHL-060","name":"Ho-Oh GX (Full Art)","set":"SHL","rarity":"FA","tier":"A","price":u(28),"p1":u(27.5),"p7":u(25),"p30":u(19),"sat":0.08,"arb":0.35,"vel":0.35,"whale":0.32,"cross":0.60,"soc":0.44,"rep":0.40,"stab":0.58},
    {"id":"SHL-073","name":"Mewtwo GX (Rainbow)","set":"SHL","rarity":"RR","tier":"S","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.07,"arb":0.47,"vel":0.47,"whale":0.52,"cross":0.80,"soc":0.62,"rep":0.33,"stab":0.63},

    # ═══════════════════════════════════════════
    # CRIMSON INVASION (2017)
    # ═══════════════════════════════════════════
    {"id":"CRI-099","name":"Necrozma GX (Full Art)","set":"CRI","rarity":"FA","tier":"B","price":u(14),"p1":u(13.5),"p7":u(12),"p30":u(9),"sat":0.09,"arb":0.24,"vel":0.24,"whale":0.20,"cross":0.46,"soc":0.32,"rep":0.46,"stab":0.54},

    # ═══════════════════════════════════════════
    # ULTRA PRISM (2018)
    # ═══════════════════════════════════════════
    {"id":"UPR-142","name":"Dialga GX (Full Art)","set":"UPR","rarity":"FA","tier":"A","price":u(22),"p1":u(21.5),"p7":u(19.5),"p30":u(15),"sat":0.08,"arb":0.30,"vel":0.30,"whale":0.28,"cross":0.55,"soc":0.38,"rep":0.43,"stab":0.56},
    {"id":"UPR-143","name":"Palkia GX (Full Art)","set":"UPR","rarity":"FA","tier":"A","price":u(20),"p1":u(19.5),"p7":u(17.5),"p30":u(13),"sat":0.08,"arb":0.28,"vel":0.28,"whale":0.25,"cross":0.53,"soc":0.36,"rep":0.44,"stab":0.55},
    {"id":"UPR-166","name":"Lusamine (Full Art)","set":"UPR","rarity":"FA","tier":"A","price":u(35),"p1":u(34),"p7":u(31),"p30":u(24),"sat":0.07,"arb":0.40,"vel":0.40,"whale":0.38,"cross":0.58,"soc":0.50,"rep":0.40,"stab":0.60},

    # ═══════════════════════════════════════════
    # FORBIDDEN LIGHT (2018)
    # ═══════════════════════════════════════════
    {"id":"FLI-131","name":"Ultra Necrozma GX (Full Art)","set":"FLI","rarity":"FA","tier":"B","price":u(16),"p1":u(15.5),"p7":u(14),"p30":u(11),"sat":0.09,"arb":0.25,"vel":0.25,"whale":0.21,"cross":0.48,"soc":0.34,"rep":0.45,"stab":0.54},
    {"id":"FLI-140","name":"Zygarde GX (Full Art)","set":"FLI","rarity":"FA","tier":"B","price":u(14),"p1":u(13.5),"p7":u(12),"p30":u(9),"sat":0.09,"arb":0.23,"vel":0.23,"whale":0.19,"cross":0.46,"soc":0.32,"rep":0.46,"stab":0.53},

    # ═══════════════════════════════════════════
    # CELESTIAL STORM (2018)
    # ═══════════════════════════════════════════
    {"id":"CES-168","name":"Rayquaza GX (Full Art)","set":"CES","rarity":"FA","tier":"S","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.06,"arb":0.47,"vel":0.47,"whale":0.52,"cross":0.80,"soc":0.60,"rep":0.33,"stab":0.63},
    {"id":"CES-177","name":"Rayquaza GX (Rainbow)","set":"CES","rarity":"RR","tier":"S","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.06,"arb":0.52,"vel":0.52,"whale":0.58,"cross":0.82,"soc":0.63,"rep":0.30,"stab":0.65},

    # ═══════════════════════════════════════════
    # LOST THUNDER (2018)
    # ═══════════════════════════════════════════
    {"id":"LOT-203","name":"Lugia GX (Full Art)","set":"LOT","rarity":"FA","tier":"S","price":u(48),"p1":u(47),"p7":u(43),"p30":u(33),"sat":0.07,"arb":0.46,"vel":0.46,"whale":0.50,"cross":0.75,"soc":0.58,"rep":0.35,"stab":0.62},
    {"id":"LOT-214","name":"Tyranitar GX (Full Art)","set":"LOT","rarity":"FA","tier":"B","price":u(16),"p1":u(15.5),"p7":u(14),"p30":u(11),"sat":0.09,"arb":0.25,"vel":0.25,"whale":0.21,"cross":0.48,"soc":0.34,"rep":0.45,"stab":0.54},
    {"id":"LOT-223","name":"Zeraora GX (Rainbow)","set":"LOT","rarity":"RR","tier":"B","price":u(20),"p1":u(19.5),"p7":u(17.5),"p30":u(13),"sat":0.08,"arb":0.28,"vel":0.28,"whale":0.25,"cross":0.50,"soc":0.36,"rep":0.43,"stab":0.55},

    # ═══════════════════════════════════════════
    # TEAM UP (2019)
    # ═══════════════════════════════════════════
    {"id":"TEU-182","name":"Red & Blue (Full Art)","set":"TEU","rarity":"FA","tier":"S","price":u(120),"p1":u(118),"p7":u(106),"p30":u(82),"sat":0.05,"arb":0.60,"vel":0.58,"whale":0.65,"cross":0.80,"soc":0.68,"rep":0.22,"stab":0.70},
    {"id":"TEU-183","name":"Pikachu & Zekrom GX (Full Art)","set":"TEU","rarity":"FA","tier":"S","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.06,"arb":0.52,"vel":0.52,"whale":0.58,"cross":0.82,"soc":0.65,"rep":0.28,"stab":0.65},
    {"id":"TEU-184","name":"Eevee & Snorlax GX (Full Art)","set":"TEU","rarity":"FA","tier":"A","price":u(35),"p1":u(34),"p7":u(31),"p30":u(24),"sat":0.07,"arb":0.40,"vel":0.40,"whale":0.38,"cross":0.65,"soc":0.50,"rep":0.38,"stab":0.60},
    {"id":"TEU-196","name":"Red & Blue (Rainbow)","set":"TEU","rarity":"RR","tier":"S","price":u(150),"p1":u(148),"p7":u(134),"p30":u(103),"sat":0.04,"arb":0.65,"vel":0.62,"whale":0.70,"cross":0.82,"soc":0.70,"rep":0.20,"stab":0.72},

    # ═══════════════════════════════════════════
    # UNBROKEN BONDS (2019)
    # ═══════════════════════════════════════════
    {"id":"UNB-215","name":"Reshiram & Charizard GX (Full Art)","set":"UNB","rarity":"FA","tier":"S","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.56,"vel":0.55,"whale":0.62,"cross":0.88,"soc":0.68,"rep":0.25,"stab":0.68},
    {"id":"UNB-217","name":"Reshiram & Charizard GX (Rainbow)","set":"UNB","rarity":"RR","tier":"S","price":u(130),"p1":u(128),"p7":u(115),"p30":u(89),"sat":0.05,"arb":0.62,"vel":0.60,"whale":0.68,"cross":0.90,"soc":0.70,"rep":0.22,"stab":0.70},
    {"id":"UNB-214","name":"Garchomp & Giratina GX (Full Art)","set":"UNB","rarity":"FA","tier":"A","price":u(40),"p1":u(39),"p7":u(35),"p30":u(27),"sat":0.07,"arb":0.43,"vel":0.43,"whale":0.42,"cross":0.62,"soc":0.48,"rep":0.38,"stab":0.60},

    # ═══════════════════════════════════════════
    # UNIFIED MINDS (2019)
    # ═══════════════════════════════════════════
    {"id":"UNM-215","name":"Mewtwo & Mew GX (Full Art)","set":"UNM","rarity":"FA","tier":"S","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.56,"vel":0.55,"whale":0.62,"cross":0.85,"soc":0.65,"rep":0.25,"stab":0.68},
    {"id":"UNM-222","name":"Mewtwo & Mew GX (Rainbow)","set":"UNM","rarity":"RR","tier":"S","price":u(130),"p1":u(128),"p7":u(115),"p30":u(89),"sat":0.04,"arb":0.62,"vel":0.60,"whale":0.68,"cross":0.87,"soc":0.68,"rep":0.22,"stab":0.70},
    {"id":"UNM-216","name":"Umbreon & Darkrai GX (Full Art)","set":"UNM","rarity":"FA","tier":"S","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.55,"cross":0.78,"soc":0.60,"rep":0.28,"stab":0.65},

    # ═══════════════════════════════════════════
    # HIDDEN FATES (2019)
    # ═══════════════════════════════════════════
    {"id":"HIF-SV049","name":"Charizard GX (Shiny)","set":"HIF","rarity":"SHV","tier":"S","price":u(280),"p1":u(276),"p7":u(248),"p30":u(192),"sat":0.04,"arb":0.72,"vel":0.68,"whale":0.78,"cross":0.90,"soc":0.75,"rep":0.18,"stab":0.75},
    {"id":"HIF-SV068","name":"Gyarados GX (Shiny)","set":"HIF","rarity":"SHV","tier":"A","price":u(60),"p1":u(59),"p7":u(53),"p30":u(41),"sat":0.06,"arb":0.48,"vel":0.47,"whale":0.52,"cross":0.65,"soc":0.50,"rep":0.30,"stab":0.63},
    {"id":"HIF-SV094","name":"Mewtwo GX (Shiny)","set":"HIF","rarity":"SHV","tier":"S","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.55,"vel":0.53,"whale":0.58,"cross":0.82,"soc":0.62,"rep":0.22,"stab":0.68},
    {"id":"HIF-SV070","name":"Umbreon GX (Shiny)","set":"HIF","rarity":"SHV","tier":"S","price":u(110),"p1":u(108),"p7":u(97),"p30":u(75),"sat":0.05,"arb":0.58,"vel":0.56,"whale":0.62,"cross":0.80,"soc":0.65,"rep":0.20,"stab":0.70},
    {"id":"HIF-SV079","name":"Eevee GX (Shiny)","set":"HIF","rarity":"SHV","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.06,"arb":0.44,"vel":0.43,"whale":0.45,"cross":0.70,"soc":0.52,"rep":0.32,"stab":0.62},
    {"id":"HIF-SV059","name":"Pikachu GX (Shiny)","set":"HIF","rarity":"SHV","tier":"S","price":u(80),"p1":u(79),"p7":u(71),"p30":u(55),"sat":0.05,"arb":0.52,"vel":0.50,"whale":0.56,"cross":0.88,"soc":0.68,"rep":0.23,"stab":0.67},

    # ═══════════════════════════════════════════
    # COSMIC ECLIPSE (2019)
    # ═══════════════════════════════════════════
    {"id":"CEC-233","name":"Charizard & Braixen GX (Full Art)","set":"CEC","rarity":"FA","tier":"S","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.06,"arb":0.52,"vel":0.52,"whale":0.58,"cross":0.82,"soc":0.62,"rep":0.28,"stab":0.65},
    {"id":"CEC-236","name":"Venusaur & Snivy GX (Full Art)","set":"CEC","rarity":"FA","tier":"A","price":u(30),"p1":u(29.5),"p7":u(27),"p30":u(20),"sat":0.07,"arb":0.37,"vel":0.37,"whale":0.34,"cross":0.60,"soc":0.44,"rep":0.40,"stab":0.58},
    {"id":"CEC-230","name":"Arceus & Dialga & Palkia GX (Full Art)","set":"CEC","rarity":"FA","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.06,"arb":0.44,"vel":0.44,"whale":0.48,"cross":0.65,"soc":0.50,"rep":0.35,"stab":0.62},
    {"id":"CEC-253","name":"Arceus & Dialga & Palkia GX (Rainbow)","set":"CEC","rarity":"RR","tier":"A","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.55,"cross":0.68,"soc":0.52,"rep":0.32,"stab":0.63},

    # ═══════════════════════════════════════════
    # REBEL CLASH (2020)
    # ═══════════════════════════════════════════
    {"id":"RCL-195","name":"Zacian V (Full Art)","set":"RCL","rarity":"FA","tier":"A","price":u(25),"p1":u(24.5),"p7":u(22),"p30":u(17),"sat":0.08,"arb":0.32,"vel":0.32,"whale":0.30,"cross":0.55,"soc":0.40,"rep":0.42,"stab":0.57},
    {"id":"RCL-196","name":"Zamazenta V (Full Art)","set":"RCL","rarity":"FA","tier":"A","price":u(22),"p1":u(21.5),"p7":u(19.5),"p30":u(15),"sat":0.08,"arb":0.30,"vel":0.30,"whale":0.27,"cross":0.53,"soc":0.38,"rep":0.43,"stab":0.56},

    # ═══════════════════════════════════════════
    # DARKNESS ABLAZE (2020)
    # ═══════════════════════════════════════════
    {"id":"DAA-189","name":"Charizard VMAX (Full Art)","set":"DAA","rarity":"FA","tier":"S","price":u(110),"p1":u(108),"p7":u(97),"p30":u(75),"sat":0.05,"arb":0.58,"vel":0.56,"whale":0.62,"cross":0.88,"soc":0.68,"rep":0.24,"stab":0.68},
    {"id":"DAA-190","name":"Charizard VMAX (Rainbow)","set":"DAA","rarity":"RR","tier":"S","price":u(150),"p1":u(148),"p7":u(134),"p30":u(103),"sat":0.05,"arb":0.64,"vel":0.62,"whale":0.68,"cross":0.90,"soc":0.70,"rep":0.22,"stab":0.70},
    {"id":"DAA-188","name":"Charizard V (Full Art)","set":"DAA","rarity":"FA","tier":"S","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.55,"cross":0.86,"soc":0.65,"rep":0.26,"stab":0.65},

    # ═══════════════════════════════════════════
    # VIVID VOLTAGE (2020)
    # ═══════════════════════════════════════════
    {"id":"VIV-185","name":"Pikachu VMAX (Rainbow)","set":"VIV","rarity":"RR","tier":"S","price":u(120),"p1":u(118),"p7":u(106),"p30":u(82),"sat":0.05,"arb":0.60,"vel":0.58,"whale":0.65,"cross":0.90,"soc":0.72,"rep":0.23,"stab":0.68},
    {"id":"VIV-170","name":"Pikachu VMAX (Full Art)","set":"VIV","rarity":"FA","tier":"S","price":u(85),"p1":u(84),"p7":u(76),"p30":u(58),"sat":0.06,"arb":0.55,"vel":0.53,"whale":0.60,"cross":0.90,"soc":0.70,"rep":0.25,"stab":0.67},

    # ═══════════════════════════════════════════
    # SHINING FATES (2021)
    # ═══════════════════════════════════════════
    {"id":"SHF-SV107","name":"Charizard VMAX (Shiny)","set":"SHF","rarity":"SHV","tier":"S","price":u(220),"p1":u(218),"p7":u(196),"p30":u(151),"sat":0.04,"arb":0.70,"vel":0.68,"whale":0.75,"cross":0.90,"soc":0.75,"rep":0.20,"stab":0.75},
    {"id":"SHF-SV122","name":"Eevee VMAX (Shiny)","set":"SHF","rarity":"SHV","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.06,"arb":0.47,"vel":0.46,"whale":0.50,"cross":0.72,"soc":0.55,"rep":0.28,"stab":0.63},
    {"id":"SHF-SV084","name":"Pikachu VMAX (Shiny)","set":"SHF","rarity":"SHV","tier":"S","price":u(130),"p1":u(128),"p7":u(116),"p30":u(89),"sat":0.05,"arb":0.62,"vel":0.60,"whale":0.67,"cross":0.92,"soc":0.75,"rep":0.22,"stab":0.70},
    {"id":"SHF-SV036","name":"Umbreon VMAX (Shiny)","set":"SHF","rarity":"SHV","tier":"S","price":u(150),"p1":u(148),"p7":u(134),"p30":u(103),"sat":0.04,"arb":0.65,"vel":0.62,"whale":0.70,"cross":0.80,"soc":0.68,"rep":0.20,"stab":0.72},

    # ═══════════════════════════════════════════
    # BATTLE STYLES (2021)
    # ═══════════════════════════════════════════
    {"id":"BST-163","name":"Urshifu VMAX (Alt Art)","set":"BST","rarity":"ALT","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.06,"arb":0.44,"vel":0.43,"whale":0.45,"cross":0.58,"soc":0.45,"rep":0.35,"stab":0.60},
    {"id":"BST-165","name":"Empoleon V (Alt Art)","set":"BST","rarity":"ALT","tier":"A","price":u(40),"p1":u(39),"p7":u(35),"p30":u(27),"sat":0.07,"arb":0.42,"vel":0.42,"whale":0.42,"cross":0.60,"soc":0.46,"rep":0.36,"stab":0.60},

    # ═══════════════════════════════════════════
    # CHILLING REIGN (2021)
    # ═══════════════════════════════════════════
    {"id":"CRE-198","name":"Ice Rider Calyrex VMAX (Alt Art)","set":"CRE","rarity":"ALT","tier":"A","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.55,"cross":0.62,"soc":0.50,"rep":0.30,"stab":0.63},
    {"id":"CRE-199","name":"Shadow Rider Calyrex VMAX (Alt Art)","set":"CRE","rarity":"ALT","tier":"A","price":u(70),"p1":u(69),"p7":u(62),"p30":u(48),"sat":0.06,"arb":0.51,"vel":0.51,"whale":0.56,"cross":0.63,"soc":0.51,"rep":0.30,"stab":0.63},
    {"id":"CRE-197","name":"Blaziken VMAX (Alt Art)","set":"CRE","rarity":"ALT","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.06,"arb":0.47,"vel":0.47,"whale":0.50,"cross":0.62,"soc":0.48,"rep":0.32,"stab":0.62},

    # ═══════════════════════════════════════════
    # EVOLVING SKIES (2021)
    # ═══════════════════════════════════════════
    {"id":"EVS-215","name":"Umbreon VMAX (Alt Art)","set":"EVS","rarity":"ALT","tier":"S","price":u(310),"p1":u(308),"p7":u(285),"p30":u(218),"sat":0.02,"arb":0.90,"vel":0.60,"whale":0.90,"cross":0.55,"soc":0.80,"rep":0.05,"stab":0.90},
    {"id":"EVS-217","name":"Rayquaza VMAX (Alt Art)","set":"EVS","rarity":"ALT","tier":"S","price":u(282),"p1":u(280),"p7":u(255),"p30":u(198),"sat":0.03,"arb":0.80,"vel":0.55,"whale":0.85,"cross":0.70,"soc":0.72,"rep":0.05,"stab":0.85},
    {"id":"EVS-074","name":"Espeon VMAX (Alt Art)","set":"EVS","rarity":"ALT","tier":"A","price":u(120),"p1":u(118),"p7":u(108),"p30":u(83),"sat":0.04,"arb":0.65,"vel":0.52,"whale":0.68,"cross":0.55,"soc":0.65,"rep":0.10,"stab":0.78},
    {"id":"EVS-075","name":"Glaceon VMAX (Alt Art)","set":"EVS","rarity":"ALT","tier":"A","price":u(95),"p1":u(93),"p7":u(85),"p30":u(65),"sat":0.04,"arb":0.60,"vel":0.48,"whale":0.60,"cross":0.52,"soc":0.60,"rep":0.12,"stab":0.76},
    {"id":"EVS-225","name":"Rayquaza V (Alt Art)","set":"EVS","rarity":"ALT","tier":"S","price":u(85),"p1":u(84),"p7":u(76),"p30":u(58),"sat":0.05,"arb":0.55,"vel":0.50,"whale":0.60,"cross":0.70,"soc":0.62,"rep":0.08,"stab":0.72},
    {"id":"EVS-214","name":"Umbreon V (Alt Art)","set":"EVS","rarity":"ALT","tier":"S","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.05,"arb":0.52,"vel":0.48,"whale":0.58,"cross":0.55,"soc":0.60,"rep":0.08,"stab":0.70},

    # ═══════════════════════════════════════════
    # FUSION STRIKE (2021)
    # ═══════════════════════════════════════════
    {"id":"FST-267","name":"Mew VMAX (Alt Art)","set":"FST","rarity":"ALT","tier":"A","price":u(85),"p1":u(84),"p7":u(76),"p30":u(58),"sat":0.05,"arb":0.55,"vel":0.50,"whale":0.58,"cross":0.72,"soc":0.58,"rep":0.18,"stab":0.68},
    {"id":"FST-268","name":"Mew VMAX (SIR)","set":"FST","rarity":"SIR","tier":"A","price":u(130),"p1":u(128),"p7":u(117),"p30":u(90),"sat":0.04,"arb":0.62,"vel":0.52,"whale":0.65,"cross":0.72,"soc":0.60,"rep":0.15,"stab":0.72},
    {"id":"FST-264","name":"Gengar VMAX (Alt Art)","set":"FST","rarity":"ALT","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.06,"arb":0.47,"vel":0.45,"whale":0.50,"cross":0.65,"soc":0.52,"rep":0.22,"stab":0.63},

    # ═══════════════════════════════════════════
    # CELEBRATIONS (2021)
    # ═══════════════════════════════════════════
    {"id":"CEL-016","name":"Charizard (Classic Collection)","set":"CEL","rarity":"CLASSIC","tier":"S","price":u(180),"p1":u(178),"p7":u(160),"p30":u(123),"sat":0.04,"arb":0.65,"vel":0.62,"whale":0.70,"cross":0.90,"soc":0.72,"rep":0.18,"stab":0.73},
    {"id":"CEL-025","name":"Pikachu (Classic Collection)","set":"CEL","rarity":"CLASSIC","tier":"S","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.56,"vel":0.54,"whale":0.60,"cross":0.92,"soc":0.72,"rep":0.20,"stab":0.70},

    # ═══════════════════════════════════════════
    # BRILLIANT STARS (2022)
    # ═══════════════════════════════════════════
    {"id":"BRS-174","name":"Charizard V (Alt Art)","set":"BRS","rarity":"ALT","tier":"S","price":u(120),"p1":u(118),"p7":u(107),"p30":u(82),"sat":0.04,"arb":0.60,"vel":0.58,"whale":0.65,"cross":0.88,"soc":0.70,"rep":0.20,"stab":0.70},
    {"id":"BRS-178","name":"Arceus VSTAR (Rainbow)","set":"BRS","rarity":"RR","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.06,"arb":0.44,"vel":0.44,"whale":0.46,"cross":0.62,"soc":0.48,"rep":0.35,"stab":0.60},
    {"id":"BRS-176","name":"Arceus VSTAR (Gold)","set":"BRS","rarity":"GOLD","tier":"A","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.52,"cross":0.65,"soc":0.52,"rep":0.32,"stab":0.63},

    # ═══════════════════════════════════════════
    # ASTRAL RADIANCE (2022)
    # ═══════════════════════════════════════════
    {"id":"ASR-208","name":"Hisuian Decidueye VSTAR (Alt Art)","set":"ASR","rarity":"ALT","tier":"B","price":u(30),"p1":u(29.5),"p7":u(27),"p30":u(20),"sat":0.08,"arb":0.37,"vel":0.36,"whale":0.33,"cross":0.55,"soc":0.42,"rep":0.40,"stab":0.57},
    {"id":"ASR-207","name":"Palkia VSTAR (Alt Art)","set":"ASR","rarity":"ALT","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.06,"arb":0.47,"vel":0.46,"whale":0.50,"cross":0.62,"soc":0.48,"rep":0.30,"stab":0.62},

    # ═══════════════════════════════════════════
    # POKEMON GO (2022)
    # ═══════════════════════════════════════════
    {"id":"PGO-078","name":"Mewtwo V (Alt Art)","set":"PGO","rarity":"ALT","tier":"S","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.55,"cross":0.80,"soc":0.62,"rep":0.28,"stab":0.63},
    {"id":"PGO-071","name":"Pikachu V (Alt Art)","set":"PGO","rarity":"ALT","tier":"S","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.05,"arb":0.52,"vel":0.52,"whale":0.58,"cross":0.88,"soc":0.68,"rep":0.25,"stab":0.65},
    {"id":"PGO-079","name":"Dragonite V (Alt Art)","set":"PGO","rarity":"ALT","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.06,"arb":0.44,"vel":0.44,"whale":0.45,"cross":0.60,"soc":0.48,"rep":0.33,"stab":0.60},

    # ═══════════════════════════════════════════
    # LOST ORIGIN (2022)
    # ═══════════════════════════════════════════
    {"id":"LOR-196","name":"Giratina VSTAR (Alt Art)","set":"LOR","rarity":"ALT","tier":"A","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.05,"arb":0.52,"vel":0.50,"whale":0.55,"cross":0.65,"soc":0.55,"rep":0.25,"stab":0.65},
    {"id":"LOR-197","name":"Aerodactyl VSTAR (Alt Art)","set":"LOR","rarity":"ALT","tier":"B","price":u(25),"p1":u(24.5),"p7":u(22),"p30":u(17),"sat":0.08,"arb":0.32,"vel":0.31,"whale":0.28,"cross":0.50,"soc":0.38,"rep":0.42,"stab":0.56},

    # ═══════════════════════════════════════════
    # SILVER TEMPEST (2022)
    # ═══════════════════════════════════════════
    {"id":"SIT-217","name":"Lugia V (Alt Art)","set":"SIT","rarity":"ALT","tier":"A","price":u(183),"p1":u(181),"p7":u(165),"p30":u(127),"sat":0.06,"arb":0.55,"vel":0.50,"whale":0.60,"cross":0.65,"soc":0.60,"rep":0.15,"stab":0.65},
    {"id":"SIT-193","name":"Lugia VSTAR (Alt Art)","set":"SIT","rarity":"ALT","tier":"A","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.55,"vel":0.48,"whale":0.58,"cross":0.65,"soc":0.58,"rep":0.18,"stab":0.68},
    {"id":"SIT-191","name":"Alolan Vulpix VSTAR (Alt Art)","set":"SIT","rarity":"ALT","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.06,"arb":0.44,"vel":0.43,"whale":0.44,"cross":0.58,"soc":0.46,"rep":0.33,"stab":0.60},

    # ═══════════════════════════════════════════
    # CROWN ZENITH (2023)
    # ═══════════════════════════════════════════
    {"id":"CRZ-GG001","name":"Charizard (Galarian Gallery)","set":"CRZ","rarity":"GG","tier":"S","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.56,"vel":0.55,"whale":0.62,"cross":0.90,"soc":0.70,"rep":0.22,"stab":0.68},
    {"id":"CRZ-GG070","name":"Pikachu VMAX (Galarian Gallery)","set":"CRZ","rarity":"GG","tier":"S","price":u(120),"p1":u(118),"p7":u(107),"p30":u(82),"sat":0.04,"arb":0.60,"vel":0.58,"whale":0.65,"cross":0.92,"soc":0.72,"rep":0.20,"stab":0.70},
    {"id":"CRZ-GG065","name":"Umbreon VMAX (Galarian Gallery)","set":"CRZ","rarity":"GG","tier":"S","price":u(150),"p1":u(148),"p7":u(134),"p30":u(103),"sat":0.04,"arb":0.65,"vel":0.60,"whale":0.70,"cross":0.60,"soc":0.68,"rep":0.15,"stab":0.72},
    {"id":"CRZ-GG063","name":"Rayquaza VMAX (Galarian Gallery)","set":"CRZ","rarity":"GG","tier":"S","price":u(130),"p1":u(128),"p7":u(116),"p30":u(89),"sat":0.04,"arb":0.62,"vel":0.58,"whale":0.68,"cross":0.72,"soc":0.65,"rep":0.15,"stab":0.70},

    # ═══════════════════════════════════════════
    # SCARLET & VIOLET BASE (2023)
    # ═══════════════════════════════════════════
    {"id":"SVI-193","name":"Gardevoir ex (SIR)","set":"SVI","rarity":"SIR","tier":"A","price":u(72),"p1":u(70),"p7":u(64),"p30":u(49),"sat":0.06,"arb":0.52,"vel":0.56,"whale":0.50,"cross":0.65,"soc":0.60,"rep":0.22,"stab":0.65},
    {"id":"SVI-198","name":"Miraidon ex (SIR)","set":"SVI","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(38),"sat":0.07,"arb":0.44,"vel":0.50,"whale":0.44,"cross":0.65,"soc":0.55,"rep":0.28,"stab":0.60},
    {"id":"SVI-199","name":"Koraidon ex (SIR)","set":"SVI","rarity":"SIR","tier":"A","price":u(50),"p1":u(49),"p7":u(44),"p30":u(34),"sat":0.07,"arb":0.42,"vel":0.48,"whale":0.42,"cross":0.63,"soc":0.53,"rep":0.28,"stab":0.58},

    # ═══════════════════════════════════════════
    # PALDEA EVOLVED (2023)
    # ═══════════════════════════════════════════
    {"id":"PAL-254","name":"Iono (SIR)","set":"PAL","rarity":"SIR","tier":"A","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.56,"vel":0.60,"whale":0.60,"cross":0.68,"soc":0.70,"rep":0.20,"stab":0.68},
    {"id":"PAL-255","name":"Iono (IR)","set":"PAL","rarity":"IR","tier":"A","price":u(35),"p1":u(34),"p7":u(31),"p30":u(24),"sat":0.07,"arb":0.40,"vel":0.42,"whale":0.38,"cross":0.65,"soc":0.62,"rep":0.30,"stab":0.60},
    {"id":"PAL-256","name":"Miraidon ex (SIR)","set":"PAL","rarity":"SIR","tier":"A","price":u(58),"p1":u(57),"p7":u(52),"p30":u(40),"sat":0.06,"arb":0.46,"vel":0.52,"whale":0.46,"cross":0.65,"soc":0.56,"rep":0.27,"stab":0.61},

    # ═══════════════════════════════════════════
    # OBSIDIAN FLAMES (2023)
    # ═══════════════════════════════════════════
    {"id":"OBF-201","name":"Charizard ex (SIR)","set":"OBF","rarity":"SIR","tier":"S","price":u(422),"p1":u(420),"p7":u(385),"p30":u(295),"sat":0.04,"arb":0.72,"vel":0.85,"whale":0.80,"cross":0.90,"soc":0.78,"rep":0.20,"stab":0.78},
    {"id":"OBF-230","name":"Charizard ex (IR)","set":"OBF","rarity":"IR","tier":"S","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.55,"whale":0.55,"cross":0.88,"soc":0.68,"rep":0.25,"stab":0.65},
    {"id":"OBF-227","name":"Tyranitar ex (SIR)","set":"OBF","rarity":"SIR","tier":"B","price":u(28),"p1":u(27.5),"p7":u(25),"p30":u(19),"sat":0.08,"arb":0.35,"vel":0.38,"whale":0.30,"cross":0.52,"soc":0.42,"rep":0.35,"stab":0.57},

    # ═══════════════════════════════════════════
    # POKEMON 151 (2023)
    # ═══════════════════════════════════════════
    {"id":"MEW-205","name":"Mew ex (SIR)","set":"MEW","rarity":"SIR","tier":"S","price":u(145),"p1":u(143),"p7":u(130),"p30":u(100),"sat":0.05,"arb":0.65,"vel":0.60,"whale":0.65,"cross":0.82,"soc":0.75,"rep":0.10,"stab":0.72},
    {"id":"MEW-202","name":"Charizard ex (SIR)","set":"MEW","rarity":"SIR","tier":"S","price":u(210),"p1":u(208),"p7":u(190),"p30":u(146),"sat":0.04,"arb":0.70,"vel":0.65,"whale":0.75,"cross":0.88,"soc":0.78,"rep":0.08,"stab":0.78},
    {"id":"MEW-207","name":"Zapdos ex (SIR)","set":"MEW","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(38),"sat":0.06,"arb":0.47,"vel":0.48,"whale":0.46,"cross":0.65,"soc":0.55,"rep":0.22,"stab":0.61},
    {"id":"MEW-204","name":"Blastoise ex (SIR)","set":"MEW","rarity":"SIR","tier":"A","price":u(48),"p1":u(47),"p7":u(43),"p30":u(33),"sat":0.07,"arb":0.45,"vel":0.45,"whale":0.44,"cross":0.68,"soc":0.55,"rep":0.24,"stab":0.60},
    {"id":"MEW-203","name":"Venusaur ex (SIR)","set":"MEW","rarity":"SIR","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.07,"arb":0.44,"vel":0.44,"whale":0.43,"cross":0.68,"soc":0.54,"rep":0.24,"stab":0.60},
    {"id":"MEW-208","name":"Alakazam ex (SIR)","set":"MEW","rarity":"SIR","tier":"A","price":u(38),"p1":u(37),"p7":u(33),"p30":u(26),"sat":0.07,"arb":0.41,"vel":0.41,"whale":0.39,"cross":0.62,"soc":0.50,"rep":0.28,"stab":0.58},
    {"id":"MEW-210","name":"Giovanni's Charisma (SIR)","set":"MEW","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(38),"sat":0.06,"arb":0.47,"vel":0.50,"whale":0.48,"cross":0.65,"soc":0.58,"rep":0.22,"stab":0.62},
    {"id":"MEW-183","name":"Charizard ex (IR)","set":"MEW","rarity":"IR","tier":"S","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.06,"arb":0.47,"vel":0.50,"whale":0.52,"cross":0.87,"soc":0.67,"rep":0.12,"stab":0.64},

    # ═══════════════════════════════════════════
    # PARADOX RIFT (2023)
    # ═══════════════════════════════════════════
    {"id":"PAR-245","name":"Roaring Moon ex (Alt Art)","set":"PAR","rarity":"ALT","tier":"A","price":u(92),"p1":u(90),"p7":u(81),"p30":u(62),"sat":0.06,"arb":0.58,"vel":0.55,"whale":0.55,"cross":0.65,"soc":0.62,"rep":0.15,"stab":0.65},
    {"id":"PAR-246","name":"Iron Valiant ex (Alt Art)","set":"PAR","rarity":"ALT","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.06,"arb":0.47,"vel":0.46,"whale":0.47,"cross":0.60,"soc":0.52,"rep":0.20,"stab":0.61},
    {"id":"PAR-262","name":"Roaring Moon ex (SIR)","set":"PAR","rarity":"SIR","tier":"A","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.50,"whale":0.50,"cross":0.65,"soc":0.58,"rep":0.17,"stab":0.63},

    # ═══════════════════════════════════════════
    # PALDEAN FATES (2024)
    # ═══════════════════════════════════════════
    {"id":"PAF-086","name":"Pikachu ex (SIR)","set":"PAF","rarity":"SIR","tier":"S","price":u(98),"p1":u(96),"p7":u(87),"p30":u(67),"sat":0.08,"arb":0.45,"vel":0.95,"whale":0.50,"cross":0.92,"soc":0.85,"rep":0.40,"stab":0.55},
    {"id":"PAF-090","name":"Charizard ex (SIR)","set":"PAF","rarity":"SIR","tier":"S","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.07,"arb":0.52,"vel":0.60,"whale":0.58,"cross":0.88,"soc":0.70,"rep":0.35,"stab":0.62},
    {"id":"PAF-085","name":"Gardevoir ex (SHV)","set":"PAF","rarity":"SHV","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.07,"arb":0.44,"vel":0.45,"whale":0.44,"cross":0.65,"soc":0.58,"rep":0.30,"stab":0.60},

    # ═══════════════════════════════════════════
    # TEMPORAL FORCES (2024)
    # ═══════════════════════════════════════════
    {"id":"TEF-201","name":"Walking Wake ex (SIR)","set":"TEF","rarity":"SIR","tier":"A","price":u(42),"p1":u(41),"p7":u(37),"p30":u(28),"sat":0.07,"arb":0.42,"vel":0.44,"whale":0.40,"cross":0.60,"soc":0.50,"rep":0.28,"stab":0.58},
    {"id":"TEF-202","name":"Iron Leaves ex (SIR)","set":"TEF","rarity":"SIR","tier":"A","price":u(38),"p1":u(37),"p7":u(33),"p30":u(26),"sat":0.07,"arb":0.40,"vel":0.40,"whale":0.38,"cross":0.58,"soc":0.48,"rep":0.28,"stab":0.57},
    {"id":"TEF-206","name":"Colress's Experiment (SIR)","set":"TEF","rarity":"SIR","tier":"A","price":u(48),"p1":u(47),"p7":u(43),"p30":u(33),"sat":0.07,"arb":0.44,"vel":0.46,"whale":0.42,"cross":0.60,"soc":0.55,"rep":0.26,"stab":0.59},

    # ═══════════════════════════════════════════
    # TWILIGHT MASQUERADE (2024)
    # ═══════════════════════════════════════════
    {"id":"TWM-167","name":"Ogerpon ex (SIR)","set":"TWM","rarity":"SIR","tier":"A","price":u(88),"p1":u(86),"p7":u(78),"p30":u(60),"sat":0.07,"arb":0.50,"vel":0.60,"whale":0.50,"cross":0.70,"soc":0.65,"rep":0.20,"stab":0.62},
    {"id":"TWM-169","name":"Teal Mask Ogerpon ex (SIR)","set":"TWM","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.07,"arb":0.47,"vel":0.48,"whale":0.46,"cross":0.62,"soc":0.55,"rep":0.24,"stab":0.60},
    {"id":"TWM-175","name":"Kieran (SIR)","set":"TWM","rarity":"SIR","tier":"A","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.52,"whale":0.50,"cross":0.65,"soc":0.62,"rep":0.22,"stab":0.62},

    # ═══════════════════════════════════════════
    # SHROUDED FABLE (2024)
    # ═══════════════════════════════════════════
    {"id":"SFA-072","name":"Pecharunt ex (SIR)","set":"SFA","rarity":"SIR","tier":"B","price":u(32),"p1":u(31),"p7":u(28),"p30":u(22),"sat":0.08,"arb":0.38,"vel":0.38,"whale":0.34,"cross":0.55,"soc":0.44,"rep":0.32,"stab":0.57},
    {"id":"SFA-069","name":"Munkidori ex (SIR)","set":"SFA","rarity":"SIR","tier":"B","price":u(28),"p1":u(27.5),"p7":u(25),"p30":u(19),"sat":0.08,"arb":0.35,"vel":0.35,"whale":0.30,"cross":0.52,"soc":0.40,"rep":0.34,"stab":0.55},

    # ═══════════════════════════════════════════
    # STELLAR CROWN (2024)
    # ═══════════════════════════════════════════
    {"id":"SCR-185","name":"Gardevoir ex (SIR)","set":"SCR","rarity":"SIR","tier":"A","price":u(72),"p1":u(70),"p7":u(64),"p30":u(49),"sat":0.06,"arb":0.52,"vel":0.56,"whale":0.50,"cross":0.65,"soc":0.60,"rep":0.22,"stab":0.65},
    {"id":"SCR-188","name":"Terapagos ex (SIR)","set":"SCR","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(37),"sat":0.07,"arb":0.47,"vel":0.48,"whale":0.46,"cross":0.62,"soc":0.55,"rep":0.24,"stab":0.60},
    {"id":"SCR-186","name":"Dragapult ex (SIR)","set":"SCR","rarity":"SIR","tier":"A","price":u(48),"p1":u(47),"p7":u(43),"p30":u(33),"sat":0.07,"arb":0.44,"vel":0.45,"whale":0.43,"cross":0.60,"soc":0.52,"rep":0.26,"stab":0.59},

    # ═══════════════════════════════════════════
    # SURGING SPARKS (2024)
    # ═══════════════════════════════════════════
    {"id":"SSP-260","name":"Pikachu ex SIR (Surging)","set":"SSP","rarity":"SIR","tier":"S","price":u(115),"p1":u(112),"p7":u(101),"p30":u(78),"sat":0.07,"arb":0.48,"vel":0.80,"whale":0.60,"cross":0.90,"soc":0.82,"rep":0.35,"stab":0.58},
    {"id":"SSP-240","name":"Raichu ex (Alt Art)","set":"SSP","rarity":"ALT","tier":"A","price":u(68),"p1":u(66),"p7":u(59),"p30":u(46),"sat":0.06,"arb":0.45,"vel":0.55,"whale":0.45,"cross":0.70,"soc":0.60,"rep":0.25,"stab":0.60},
    {"id":"SSP-258","name":"Raikou V (Alt Art)","set":"SSP","rarity":"ALT","tier":"A","price":u(45),"p1":u(44),"p7":u(40),"p30":u(31),"sat":0.07,"arb":0.44,"vel":0.46,"whale":0.43,"cross":0.62,"soc":0.52,"rep":0.28,"stab":0.59},
    {"id":"SSP-261","name":"Miraidon ex (SIR)","set":"SSP","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(38),"sat":0.07,"arb":0.47,"vel":0.50,"whale":0.46,"cross":0.65,"soc":0.55,"rep":0.26,"stab":0.60},

    # ═══════════════════════════════════════════
    # PRISMATIC EVOLUTIONS (2025)
    # ═══════════════════════════════════════════
    {"id":"PRE-161","name":"Umbreon ex (SIR)","set":"PRE","rarity":"SIR","tier":"S","price":u(820),"p1":u(810),"p7":u(735),"p30":u(565),"sat":0.02,"arb":0.92,"vel":0.70,"whale":0.95,"cross":0.62,"soc":0.90,"rep":0.05,"stab":0.88},
    {"id":"PRE-162","name":"Espeon ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(285),"p1":u(280),"p7":u(252),"p30":u(194),"sat":0.03,"arb":0.82,"vel":0.60,"whale":0.80,"cross":0.55,"soc":0.78,"rep":0.08,"stab":0.82},
    {"id":"PRE-163","name":"Glaceon ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(175),"p1":u(172),"p7":u(155),"p30":u(119),"sat":0.04,"arb":0.75,"vel":0.55,"whale":0.70,"cross":0.50,"soc":0.72,"rep":0.10,"stab":0.78},
    {"id":"PRE-164","name":"Sylveon ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(155),"p1":u(152),"p7":u(138),"p30":u(106),"sat":0.04,"arb":0.72,"vel":0.58,"whale":0.68,"cross":0.58,"soc":0.70,"rep":0.10,"stab":0.76},
    {"id":"PRE-165","name":"Flareon ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.65,"vel":0.52,"whale":0.58,"cross":0.52,"soc":0.65,"rep":0.12,"stab":0.72},
    {"id":"PRE-166","name":"Vaporeon ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(85),"p1":u(83),"p7":u(75),"p30":u(58),"sat":0.05,"arb":0.62,"vel":0.50,"whale":0.55,"cross":0.50,"soc":0.62,"rep":0.12,"stab":0.70},
    {"id":"PRE-167","name":"Jolteon ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(80),"p1":u(78),"p7":u(70),"p30":u(54),"sat":0.05,"arb":0.60,"vel":0.50,"whale":0.55,"cross":0.52,"soc":0.62,"rep":0.12,"stab":0.70},
    {"id":"PRE-168","name":"Leafeon ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(72),"p1":u(70),"p7":u(63),"p30":u(49),"sat":0.06,"arb":0.57,"vel":0.48,"whale":0.52,"cross":0.50,"soc":0.60,"rep":0.13,"stab":0.68},
    {"id":"PRE-169","name":"Eevee ex (SIR)","set":"PRE","rarity":"SIR","tier":"A","price":u(110),"p1":u(108),"p7":u(97),"p30":u(75),"sat":0.04,"arb":0.67,"vel":0.55,"whale":0.62,"cross":0.70,"soc":0.70,"rep":0.10,"stab":0.74},
    {"id":"PRE-131","name":"Umbreon ex (IR)","set":"PRE","rarity":"IR","tier":"S","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.56,"vel":0.55,"whale":0.60,"cross":0.60,"soc":0.72,"rep":0.08,"stab":0.70},
    {"id":"PRE-132","name":"Espeon ex (IR)","set":"PRE","rarity":"IR","tier":"A","price":u(42),"p1":u(41),"p7":u(37),"p30":u(28),"sat":0.07,"arb":0.43,"vel":0.43,"whale":0.42,"cross":0.52,"soc":0.58,"rep":0.12,"stab":0.62},
    {"id":"PRE-140","name":"Eevee ex (IR)","set":"PRE","rarity":"IR","tier":"A","price":u(48),"p1":u(47),"p7":u(43),"p30":u(33),"sat":0.06,"arb":0.45,"vel":0.45,"whale":0.44,"cross":0.68,"soc":0.62,"rep":0.12,"stab":0.63},

    # ═══════════════════════════════════════════
    # JOURNEY TOGETHER (2025)
    # ═══════════════════════════════════════════
    {"id":"JTG-185","name":"Charizard ex (SIR)","set":"JTG","rarity":"SIR","tier":"S","price":u(135),"p1":u(132),"p7":u(119),"p30":u(91),"sat":0.06,"arb":0.55,"vel":0.70,"whale":0.65,"cross":0.88,"soc":0.75,"rep":0.25,"stab":0.62},
    {"id":"JTG-183","name":"Red (SIR)","set":"JTG","rarity":"SIR","tier":"A","price":u(95),"p1":u(93),"p7":u(84),"p30":u(65),"sat":0.05,"arb":0.56,"vel":0.60,"whale":0.58,"cross":0.75,"soc":0.70,"rep":0.20,"stab":0.67},
    {"id":"JTG-184","name":"Pikachu ex (SIR)","set":"JTG","rarity":"SIR","tier":"S","price":u(75),"p1":u(74),"p7":u(67),"p30":u(51),"sat":0.07,"arb":0.52,"vel":0.65,"whale":0.55,"cross":0.90,"soc":0.78,"rep":0.28,"stab":0.62},
    {"id":"JTG-177","name":"Charizard ex (IR)","set":"JTG","rarity":"IR","tier":"S","price":u(35),"p1":u(34),"p7":u(31),"p30":u(24),"sat":0.07,"arb":0.40,"vel":0.42,"whale":0.40,"cross":0.86,"soc":0.65,"rep":0.28,"stab":0.58},

    # ═══════════════════════════════════════════
    # DESTINED RIVALS (2025)
    # ═══════════════════════════════════════════
    {"id":"DRI-198","name":"Mewtwo ex (SIR)","set":"DRI","rarity":"SIR","tier":"S","price":u(95),"p1":u(93),"p7":u(86),"p30":u(66),"sat":0.07,"arb":0.48,"vel":0.68,"whale":0.58,"cross":0.82,"soc":0.72,"rep":0.30,"stab":0.58},
    {"id":"DRI-199","name":"Gengar ex (Alt Art)","set":"DRI","rarity":"ALT","tier":"A","price":u(62),"p1":u(61),"p7":u(56),"p30":u(43),"sat":0.06,"arb":0.42,"vel":0.52,"whale":0.45,"cross":0.62,"soc":0.58,"rep":0.22,"stab":0.60},
    {"id":"DRI-200","name":"N (SIR)","set":"DRI","rarity":"SIR","tier":"A","price":u(85),"p1":u(83),"p7":u(75),"p30":u(58),"sat":0.06,"arb":0.54,"vel":0.60,"whale":0.55,"cross":0.68,"soc":0.68,"rep":0.22,"stab":0.63},
    {"id":"DRI-190","name":"Mewtwo ex (IR)","set":"DRI","rarity":"IR","tier":"S","price":u(28),"p1":u(27.5),"p7":u(25),"p30":u(19),"sat":0.08,"arb":0.35,"vel":0.40,"whale":0.34,"cross":0.80,"soc":0.60,"rep":0.33,"stab":0.55},

    # ═══════════════════════════════════════════
    # MEGA EVOLUTION (2025)
    # ═══════════════════════════════════════════
    {"id":"MEG-198","name":"Mega Charizard Y ex (SIR)","set":"MEG","rarity":"SIR","tier":"S","price":u(180),"p1":u(175),"p7":u(158),"p30":u(121),"sat":0.05,"arb":0.68,"vel":0.75,"whale":0.78,"cross":0.92,"soc":0.85,"rep":0.15,"stab":0.68},
    {"id":"MEG-199","name":"Mega Charizard X ex (SIR)","set":"MEG","rarity":"SIR","tier":"S","price":u(165),"p1":u(162),"p7":u(146),"p30":u(112),"sat":0.05,"arb":0.66,"vel":0.72,"whale":0.75,"cross":0.90,"soc":0.82,"rep":0.15,"stab":0.67},
    {"id":"MEG-200","name":"Mega Gengar ex (SIR)","set":"MEG","rarity":"SIR","tier":"A","price":u(88),"p1":u(86),"p7":u(77),"p30":u(59),"sat":0.06,"arb":0.52,"vel":0.60,"whale":0.55,"cross":0.72,"soc":0.68,"rep":0.18,"stab":0.62},
    {"id":"MEG-201","name":"Mega Blastoise ex (SIR)","set":"MEG","rarity":"SIR","tier":"A","price":u(72),"p1":u(70),"p7":u(63),"p30":u(49),"sat":0.07,"arb":0.48,"vel":0.55,"whale":0.50,"cross":0.70,"soc":0.62,"rep":0.20,"stab":0.60},
    {"id":"MEG-202","name":"Mega Venusaur ex (SIR)","set":"MEG","rarity":"SIR","tier":"A","price":u(65),"p1":u(64),"p7":u(58),"p30":u(44),"sat":0.07,"arb":0.46,"vel":0.52,"whale":0.48,"cross":0.68,"soc":0.60,"rep":0.20,"stab":0.59},
    {"id":"MEG-188","name":"Mega Charizard Y ex (IR)","set":"MEG","rarity":"IR","tier":"S","price":u(42),"p1":u(41),"p7":u(37),"p30":u(28),"sat":0.07,"arb":0.43,"vel":0.48,"whale":0.45,"cross":0.90,"soc":0.72,"rep":0.18,"stab":0.58},

    # ═══════════════════════════════════════════
    # PHANTASMAL FLAMES (2025)
    # ═══════════════════════════════════════════
    {"id":"PHF-185","name":"Dragapult ex (SIR)","set":"PHF","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(49),"p30":u(38),"sat":0.07,"arb":0.40,"vel":0.50,"whale":0.42,"cross":0.60,"soc":0.55,"rep":0.28,"stab":0.55},
    {"id":"PHF-186","name":"Mimikyu ex (Alt Art)","set":"PHF","rarity":"ALT","tier":"B","price":u(42),"p1":u(41),"p7":u(37),"p30":u(28),"sat":0.08,"arb":0.35,"vel":0.45,"whale":0.38,"cross":0.58,"soc":0.50,"rep":0.30,"stab":0.52},
    {"id":"PHF-176","name":"Dragapult ex (IR)","set":"PHF","rarity":"IR","tier":"A","price":u(18),"p1":u(17.5),"p7":u(16),"p30":u(12),"sat":0.09,"arb":0.27,"vel":0.32,"whale":0.25,"cross":0.58,"soc":0.44,"rep":0.32,"stab":0.50},

    # ═══════════════════════════════════════════
    # ASCENDED HEROES (2026)
    # ═══════════════════════════════════════════
    {"id":"ASH-200","name":"Mega Dragonite ex (SIR)","set":"ASH","rarity":"SIR","tier":"A","price":u(78),"p1":u(74),"p7":u(65),"p30":u(50),"sat":0.05,"arb":0.60,"vel":0.72,"whale":0.62,"cross":0.75,"soc":0.70,"rep":0.15,"stab":0.60},
    {"id":"ASH-201","name":"Mega Charizard Y ex (Alt Art)","set":"ASH","rarity":"ALT","tier":"S","price":u(220),"p1":u(210),"p7":u(185),"p30":u(142),"sat":0.04,"arb":0.72,"vel":0.80,"whale":0.78,"cross":0.94,"soc":0.85,"rep":0.12,"stab":0.65},
    {"id":"ASH-202","name":"Mega Mewtwo Y ex (SIR)","set":"ASH","rarity":"SIR","tier":"S","price":u(155),"p1":u(148),"p7":u(130),"p30":u(100),"sat":0.04,"arb":0.68,"vel":0.75,"whale":0.72,"cross":0.87,"soc":0.80,"rep":0.12,"stab":0.62},
    {"id":"ASH-203","name":"N's Zekrom (SIR)","set":"ASH","rarity":"SIR","tier":"A","price":u(68),"p1":u(65),"p7":u(57),"p30":u(44),"sat":0.06,"arb":0.50,"vel":0.60,"whale":0.52,"cross":0.65,"soc":0.68,"rep":0.20,"stab":0.58},
    {"id":"ASH-204","name":"Mega Venusaur ex (SIR)","set":"ASH","rarity":"SIR","tier":"A","price":u(65),"p1":u(63),"p7":u(55),"p30":u(42),"sat":0.06,"arb":0.48,"vel":0.58,"whale":0.50,"cross":0.68,"soc":0.62,"rep":0.18,"stab":0.58},
    {"id":"ASH-190","name":"Mega Charizard Y ex (IR)","set":"ASH","rarity":"IR","tier":"S","price":u(45),"p1":u(43),"p7":u(38),"p30":u(29),"sat":0.07,"arb":0.44,"vel":0.52,"whale":0.46,"cross":0.92,"soc":0.74,"rep":0.15,"stab":0.58},
    {"id":"ASH-191","name":"Mega Mewtwo Y ex (IR)","set":"ASH","rarity":"IR","tier":"S","price":u(32),"p1":u(31),"p7":u(27),"p30":u(21),"sat":0.08,"arb":0.40,"vel":0.48,"whale":0.40,"cross":0.85,"soc":0.68,"rep":0.16,"stab":0.55},

    # ═══════════════════════════════════════════
    # PERFECT ORDER (2026)
    # ═══════════════════════════════════════════
    {"id":"PFO-185","name":"Mega Meganium ex (SIR)","set":"PFO","rarity":"SIR","tier":"B","price":u(45),"p1":u(44),"p7":u(39),"p30":u(30),"sat":0.08,"arb":0.38,"vel":0.48,"whale":0.38,"cross":0.60,"soc":0.52,"rep":0.25,"stab":0.52},
    {"id":"PFO-186","name":"Mega Typhlosion ex (SIR)","set":"PFO","rarity":"SIR","tier":"B","price":u(42),"p1":u(41),"p7":u(36),"p30":u(28),"sat":0.08,"arb":0.36,"vel":0.46,"whale":0.36,"cross":0.58,"soc":0.50,"rep":0.26,"stab":0.51},
    {"id":"PFO-175","name":"Mega Meganium ex (IR)","set":"PFO","rarity":"IR","tier":"B","price":u(15),"p1":u(14.5),"p7":u(13),"p30":u(10),"sat":0.09,"arb":0.25,"vel":0.32,"whale":0.22,"cross":0.58,"soc":0.42,"rep":0.28,"stab":0.48},

    # ═══════════════════════════════════════════
    # CHAOS RISING (2026)
    # ═══════════════════════════════════════════
    {"id":"CRS-190","name":"Mega Rayquaza ex (SIR)","set":"CRS","rarity":"SIR","tier":"S","price":u(185),"p1":u(178),"p7":u(156),"p30":u(120),"sat":0.04,"arb":0.70,"vel":0.82,"whale":0.78,"cross":0.90,"soc":0.82,"rep":0.12,"stab":0.65},
    {"id":"CRS-191","name":"Mega Salamence ex (Alt Art)","set":"CRS","rarity":"ALT","tier":"A","price":u(72),"p1":u(69),"p7":u(61),"p30":u(47),"sat":0.06,"arb":0.52,"vel":0.62,"whale":0.55,"cross":0.68,"soc":0.62,"rep":0.18,"stab":0.60},
    {"id":"CRS-180","name":"Mega Rayquaza ex (IR)","set":"CRS","rarity":"IR","tier":"S","price":u(38),"p1":u(36),"p7":u(32),"p30":u(24),"sat":0.07,"arb":0.43,"vel":0.52,"whale":0.45,"cross":0.88,"soc":0.70,"rep":0.15,"stab":0.56},
]
