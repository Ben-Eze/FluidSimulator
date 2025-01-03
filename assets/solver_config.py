spec = {
    "name": "TestSolver",

    "domain": {                                           
        "width": 150,
        "height": 40,
        "base_size": 0.2,
    },

    "time": {
        "dt": 0.1,
        "t_max": 1
    },

    "BCs": {                                            # TODO
        "horizontal": "wall",
        "vertical": "wall",
        # TODO: specify values
        # TODO: Dirichlet AND Neumann BC support
    },

    "ICs": {},                                          # TODO

    "scheme": {
        "name": "ExplicitEuler",
        "dx==dy": True,
        "nit": 5
    },

    "fluid": {
        "name": "air",
        "density": 1e1,                                     # TODO
        "viscosity": 1e-1,
        "smoke_viscosity": 1e-3,
        "smoke_fade": 0.99
    },

    "display": {
        "pygame": False,
        "show_live": True,
        "width": 1000,
        "height": 700,
        "visualisation": "",
        "show_smoke": True,
        "show_particles": True,
    },

    "gui": {
        "brush_size": 20,
        "smoke_strength": 2
    },

    "videowriter": {
        "record": False,
        "fps": 24,
        "vid_dir": "out/vid",
        "vid_name": "vid"
    },

    "log": {                                          
        "verbose": True,                        
        "log_file": True                         
    }
}