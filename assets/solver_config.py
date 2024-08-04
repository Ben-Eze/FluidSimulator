spec = {
    "name": "TestSolver",

    "grid": {                                           # TODO
        "width": 1.5,
        "height": 1,
        "base_size": 0.01
    },

    "BCs": {                                            # TODO
        "horizontal": "wall",
        "vertical": "wall",
        # TODO: specify values
        # TODO: Dirichlet AND Neumann BC support
    },

    "ICs": {},

    "fluid": {
        "name": "air",
        "density": 1e3,                                     # TODO
        "viscosity": 1e-2,                                  # TODO
        # and other values
    },

    "display": {                                      # TODO
        "max_width": 1000,
        "max_height": 700,
        "visualisation": "velocity",
        "show_smoke": True,
        "show_particles": True,
        "record": True
    },

    "log": {                                          
        "verbose": True,                        
        "log_file": True                         
    }
}