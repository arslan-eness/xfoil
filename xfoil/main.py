import untitled0 as ga

npop = 1000
n_first_parent =10
gen = 1 
child_size =1000

details = {}


current_pop=ga.first_pop(npop, n_first_parent, child_size)

for i in range(1,gen+1):
    current_pop=ga.ga(current_pop, npop, child_size)
    details[i]="The best member of {}. pop: Cl={} Cd={} Cl/Cd = {}" .format(i,current_pop[1].cl,current_pop[1].cd,current_pop[1].cl_cd)
                 

#PermissionError: [Errno 13] Permission denied: 'new_airfoil.txt'