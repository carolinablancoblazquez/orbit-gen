from .orbit_ic import OrbitIC

<<<<<<< HEAD
PRESETS: dict[str, dict[str, OrbitIC]] = {
    "L2_Southern_Halo": {
        "EM" : OrbitIC(
            name="EM_L2_Southern_Halo",
            x0=1.0110350588,
            z0=-0.1731500000,
            vy0=-0.0780141199,
            half_period=1.3632096570 / 2,
        ),
        "SE" : OrbitIC(
            name="SE_L2_Southern_Halo",
            x0=1.0057032659079346,
            z0=-1.2409260038177099e-2,
            vy0=-1.2623398608372105e-2,
            half_period=2.1172370586539060 / 2,
        ),
    },

    "DRO": {
        "EM" : OrbitIC(
            name="EM_DRO",
            x0=0.583856747,
            z0=0.0,
            vy0=0.96455414,
            half_period=5.70245716 / 2,
        ),
        "SE" : OrbitIC(
            name="SE_DRO",
            x0=1.0005627381528093e+0,
            z0=-9.9084312832447642e-27,
            vy0=-7.4041644955106137e-2,
            half_period=4.8020469554671263e-2 / 2,
        ),
    },

    "L1_Northern_Halo": {
        "EM" : OrbitIC(
            name="EM_L1_Northern_Halo",
            x0=0.856382122325864,
            z0=0.181519309916197,
            vy0=0.257898218422393,
            half_period=1.22727308466325,
        ),
        "SE" : OrbitIC(
            name="SE_L1_Northern_Halo",
            x0=9.9342988420305367e-1,
            z0=1.2285790238546899e-2,
            vy0=1.3842107210222549e-2,
            half_period=2.2812718320995415e+0 / 2,
        ),
    },

    "Butterfly": {
        "EM" : OrbitIC(
            name="EM_Butterfly",
            x0=1.06896234204296,
            z0=0.159599443574046,
            vy0=-0.00769167653854165,
            half_period=1.66142030228280,
        ),
        "SE" : OrbitIC(
            name="SE_Butterfly",
            x0=9.9478400099057562e-1,
            z0=9.3307317319370944e-3,
            vy0=-2.7018843432500038e-3,
            half_period=3.6918732624381563 / 2,
        ),
    },

    "L2_Northern_Halo": {
        "EM" : OrbitIC(
            name="EM_L2_Northern_Halo",
            x0=1.0924697204324003e+0,
            z0=2.0118187175809177e-1,
            vy0=-2.0999964360980777e-1,
            half_period=2.5256026213792353e+0 / 2,
        ),
        "SE" : OrbitIC(
            name="SE_L2_Northern_Halo",
            x0=1.0082893998277027,
            z0=0.011434182696839030,
            vy0=-0.015179690420484332,
            half_period=2.7047531095113841 / 2,
        ),
    },

    "L2_Lyapunov": {
        "EM" : OrbitIC(
            name="EM_L2_Lyapunov",
            x0=1.1213042091132026e+0,
            z0=1.0696906809883904e-29,
            vy0=1.7168023931614440e-1,
            half_period=3.4134266416026278e+0 / 2,
        ),
        "SE" : OrbitIC(
            name="SE_L2_Lyapunov",
            x0=1.0030516289641727,
            z0=1.7613075082610678e-17,
            vy0=4.2071729820709863e-2,
            half_period=4.1379689311747248 / 2,
        ),
    },

    "Dragonfly": {
        "EM" : OrbitIC(
            name="EM_Dragonfly",
            x0=1.1436327184719191e+0,
            z0=1.0109395279050720e-1,
            vy0=-3.4052545075190177e-1,
            half_period=6.8974361097955299e+0 / 2,
        ),
        "SE" : OrbitIC(
            name="SE_Dragonfly",
            x0=1.0087123143716323,
            z0=1.0173103235716078e-2,
            vy0=-1.6680589951751042e-2,
            half_period=5.6228423897645730 / 2,
        ),
    },
    
    "3_1_Lunar_Resonant" : {
        "EM" : OrbitIC(
            name="EM_3_1_Lunar_Resonant",
            x0=2.4285786740195644e-3,
            z0=-7.6513528595122203e-57,
            vy0=1.1534396288254891e+1,
            half_period=6.2649639398149954e+0 / 2,
        ),
    },
=======
PRESETS: dict[str, OrbitIC] = {
    "EM_L2_Northern_Halo": OrbitIC(
        name="EM_L2_Northern_Halo",
        x0=1.0110350588,
        z0=-0.1731500000,
        vy0=-0.0780141199,
        half_period=1.3632096570 / 2,
    ),
    "EM_DRO_1": OrbitIC(
        name="EM_DRO_1",
        x0=0.583856747,
        z0=0.0,
        vy0=0.96455414,
        half_period=5.70245716 / 2,
    ),
    "EM_DRO_2": OrbitIC(
        name="EM_DRO_2",
        x0=0.429519110229904,
        z0=0.0,
        vy0=1.440796689672539,
        half_period=3.051133070334277,
    ),
    "EM_L1": OrbitIC(
        name="EM_L1",
        x0=0.856382122325864,
        z0=0.181519309916197,
        vy0=0.257898218422393,
        half_period=1.22727308466325,
    ),
    "EM_Butterfly": OrbitIC(
        name="EM_Butterfly",
        x0=1.06896234204296,
        z0=0.159599443574046,
        vy0=-0.00769167653854165,
        half_period=1.66142030228280,
    ),
    "EM_Unnamed_1": OrbitIC(
        name="EM_Unnamed_1",
        x0=0.95571113,
        z0=0.16892834,
        vy0=0.29101955,
        half_period=6.8828406 / 2,
    ),
    "SE_L2_Northern_Halo": OrbitIC(
        name="SE_L2_Northern_Halo",
        x0=1.0082893998277027,
        z0=0.011434182696839030,
        vy0=-0.015179690420484332,
        half_period=2.7047531095113841 / 2,
    ),
    "SE_L1_Vertical": OrbitIC(
        name="SE_L1_Vertical",
        x0=1.0022515716338869,
        z0=-1.9346947758385478e-13,
        vy0=-1.3010231214778553e-1,
        half_period=6.2826376084648130 / 2,
    ),
    "SE_L2_Lyapunov": OrbitIC(
        name="SE_L2_Lyapunov",
        x0=1.0030516289641727,
        z0=1.7613075082610678e-17,
        vy0=4.2071729820709863e-2,
        half_period=4.1379689311747248 / 2,
    ),
    "SE_L2_Small_Lyapunov": OrbitIC(
        name="SE_L2_Small_Lyapunov",
        x0=1.0173058431158761,
        z0=-8.9129284257995943e-27,
        vy0=-3.5071329991448227e-2,
        half_period=5.5314456810353905 / 2,
    ),
    "SE_L2_Large_Lyapunov": OrbitIC(
        name="SE_L2_Large_Lyapunov",
        x0=1.0437961011210057,
        z0=0,
        vy0=-8.2206717351832326e-2,
        half_period=8.3852287199494260 / 2,
    ),
    "SE_L2_Southern_Halo": OrbitIC(
        name="SE_L2_Southern_Halo",
        x0=1.0057032659079346,
        z0=-1.2409260038177099e-2,
        vy0=-1.2623398608372105e-2,
        half_period=2.1172370586539060 / 2,
    ),
    "SE_Butterfly": OrbitIC(
        name="SE_Butterfly",
        x0=9.9478400099057562e-1,
        z0=9.3307317319370944e-3,
        vy0=-2.7018843432500038e-3,
        half_period=3.6918732624381563 / 2,
    ),
    "SE_Dragonfly": OrbitIC(
        name="SE_Dragonfly",
        x0=1.0087123143716323,
        z0=1.0173103235716078e-2,
        vy0=-1.6680589951751042e-2,
        half_period=5.6228423897645730 / 2,
    ),
>>>>>>> main
}
