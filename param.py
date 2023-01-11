class Param:
    # class variables shared by all instances
    # Make props add up to total_invested (out of 1000, 'per mille')
    total_invested = 1000
    
    def reset_total(self, par_idx=0):
        self.par_idx = par_idx
        
    def incr_total(self):
        self.par_idx += 1
    
    def reset_attempt(self):
        self.attempt = 0

    def next_attempt(self):
        self.param = self.save_param.copy()
        self.attempt += 1

    def __init__(self, gen, width, param, par_adj=[]):
        self.gen = gen
        self.width = width
        self.param = param
        if (not gen['do_singlerun']) and (len(par_adj) == 0):
            self.par_adj = range(0, len(param))
        else:
            self.par_adj = par_adj
        self.par_max = len(self.par_adj)
        self.reset_attempt()

    def __str__(self):
        select_par = 0
        return_str = '['
        while select_par < len(self.param):
            for sub_par in range(0, self.width - 1): 
                return_str = f"{return_str}{self.param[select_par + sub_par]}, "
            select_par += self.width
            if select_par != len(self.param):
                return_str = f"{return_str}{self.param[select_par - 1]},\n\t "
            else:
                return_str = f"{return_str}{self.param[select_par - 1]}]"
        return return_str
        
    def save(self, run):
        self.save_param = self.param.copy()
        run['save_param'] = self.save_param
        
    def do_attempt(self):
        return self.attempt < 2 * self.par_max
    
    def prep_next(self, run, zoom):
        self.save(run)
        select_par = self.par_adj[(self.par_idx // 2) % self.par_max]
        select_dir = ((self.par_idx % 2) * 2 - 1) * zoom
        self.param[select_par] += select_dir
        # Keep parameters sane
        if select_par % self.width in [0, 1, 2, 3]:
            pass
        if select_par % self.width in [4, 5, 6]:
            self.param[select_par] = max(1, self.param[select_par])
        if select_par % self.width == 7:
            self.param[select_par] = max(460, self.param[select_par])
        if select_par % self.width == 8:
            self.param[select_par] = max(7, self.param[select_par])
            
    def buy(self):
        buy = 0
        select_par = 0
        while select_par < len(self.param):
            buy += abs(self.param[select_par] + self.param[select_par + 2] * bal_mean + self.param[select_par + 3] * fed_mean)
            select_par += self.width
        return buy / self.total_invested
