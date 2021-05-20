import re

class Target:
    def __init__(self, selector):
        self.selector = selector
        self.args = {
            "coords":[None, None, None], 
            "delta":[None, None, None], 
            "radius": [None, None],
            "tags": [],
            "sort": "nearest"
        }

        self.process_selector()

    def process_selector(self):
        if self.selector[0] != "@":
            self.args["name"] = self.selector[0]
        else:
            ## Todo: Rewrite this whole section

            variable = self.selector[:2]
            raw_args = self.selector[3:-1]

            scores = re.match("{.*}", raw_args)
            if scores:
                raw_args = re.sub("{.*}", "", raw_args)
            
            for arg in raw_args.split(","):
                k, v = arg.split("=")

                if k == "x":
                    self.args["coords"][0] = v
                elif k == "y":
                    self.args["coords"][1] = v
                elif k == "z":
                    self.args["coords"][2] = v
                elif k == "dx":
                    self.args["delta"][0] = v
                elif k == "dy":
                    self.args["delta"][1] = v
                elif k == "dz":
                    self.args["delta"][0] = v
                elif k == "rm":
                    self.args["radius"][0] = v
                elif k == "r":
                    self.args["radius"][1] = v
                elif k == "name":
                    self.args["name"] = v
                elif k == "type":
                    self.args["type"] = v
                elif k == "c":
                    self.args["count"] = v
                elif k == "scores":
                    self.args["scores"] = scores
                elif k == "tag":
                    self.args["tags"].append(v)


                self.process_variable(self.selector[:2])
    
    def process_variable(self, var):
        if var == "@a":
            self.args["type"] = "player"
                
        elif var == "@p":
            self.args["c"] = 1
            self.args["type"] = "player"
        
        elif var == "@e":
            pass

        elif var == "@r":
            self.args["sort"] = "random"
        
        elif var == "@s":
            self.args["self"] = True