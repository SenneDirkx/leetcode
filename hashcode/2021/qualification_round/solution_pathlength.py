from math import ceil

def parse_input(filename):
    data = None
    with open(filename, 'r') as file:
        data = file.readlines()
    return data

def write_output(filename, data):
    with open(filename, 'w') as file:
        file.writelines(data)

def get_solution(data):
    # parse data
    duration_simulation, nb_intersections, nb_streets, nb_cars, bonus_points = map(lambda string: int(string), data[0].strip(" \n").split(' '))

    # street = [ start_intersection , end_intersection , street_name , travel time ]
    streets = []
    for street_input in data[1:nb_streets + 1]:
        raw_street = street_input.strip(" \n").split(' ')
        for i in range(len(raw_street)):
            if i != 2:
                raw_street[i] = int(raw_street[i])
        streets.append(raw_street)

    # car_path = [ nb_streets , street_name1, street_name2...... ]
    car_paths = []
    for car_path_input in data[nb_streets+1:nb_cars + nb_streets + 1]:
        car_path = car_path_input.strip(" \n").split(' ')
        car_path[0] = int(car_path[0])
        car_paths.append(car_path)

    streets_to_duration = {}
    for street in streets:
        streets_to_duration[street[2]] = street[3]
    
    car_total_durations = []
    for car_path in car_paths:
        count = 0
        for p in range(2,len(car_path)):
            count += streets_to_duration[car_path[p]]
        car_total_durations.append(count)

    intersections_to_streets = {}
    for street in streets:
        end_intersection = street[1]
        street_name = street[2]
        if end_intersection in intersections_to_streets:
            intersections_to_streets[end_intersection].add(street_name)
        else:
            intersections_to_streets[end_intersection] = set()
            intersections_to_streets[end_intersection].add(street_name)
    
    streets_to_cars_total = {}
    streets_to_cars_paths_to_go= {}
    for car_path in car_paths:
        for street_index in range(1,len(car_path)):
            if car_path[street_index] in streets_to_cars_total:
                streets_to_cars_total[car_path[street_index]] +=1
                for p in range(street_index,len(car_path)):
                    if p == 1:
                        continue
                    streets_to_cars_paths_to_go[car_path[street_index]] += streets_to_duration[car_path[p]]
            else: 
                streets_to_cars_total[car_path[street_index]] = 1
                streets_to_cars_paths_to_go[car_path[street_index]] = 0
                for p in range(street_index,len(car_path)):
                    if p == 1:
                        continue
                    streets_to_cars_paths_to_go[car_path[street_index]] += streets_to_duration[car_path[p]]
    
    schedules = []

    for intersection in intersections_to_streets:
        schedule = []


        if len(intersections_to_streets[intersection]) == 1:
            schedule.append(str(intersection)+'\n')
            schedule.append(str(len(intersections_to_streets[intersection]))+'\n')
            for street in intersections_to_streets[intersection]:
                schedule.append(street + ' ' + '1' + '\n')
            schedules.append(schedule)
            #######
        else:
            
            streets_to_cars_tmp = []
            streets_to_pathlength_avg = []
            # for street in intersections_to_streets[intersection]:
            #     if street in streets_to_cars_total:
            #         streets_to_cars_tmp.append([street, streets_to_cars_total[street]])
            #     else:
            #         streets_to_cars_tmp.append([street, 0])
            #streets_to_cars_tmp.sort(key=lambda x: x[1]m, reverse=True)
            for street in intersections_to_streets[intersection]:
                if street in streets_to_cars_total:
                    streets_to_cars_tmp.append([street, streets_to_cars_total[street]])
                    streets_to_pathlength_avg.append([street, streets_to_cars_paths_to_go[street]/streets_to_cars_total[street]])
            i = 0
            street_count = 0
            #i geeft terug hoeveel straten er zijn met een auto op T0
            while i < len(streets_to_cars_tmp):
                if streets_to_cars_tmp[i][1] != 0:
                    street_count += 1
                i+=1
            if street_count == 0:
                street_count = 1
                
            # best_streets = []
            # total_cars = 0
            # for [street_name, car_amount] in streets_to_cars_tmp:
            #     total_cars += car_amount
            
            # for [street_name, car_amount] in streets_to_cars_tmp:
            #     seconds = max(1, ceil(car_amount/i) )
            #     if street_name in streets_to_cars_total:
            #         seconds = min(seconds, streets_to_cars_total[street_name])
            #         best_streets.append([street_name, seconds ])
            best_streets = []
            max_path = 0
            min_cars = 0
            max_cars = 0
            for [street_name, avg_path] in streets_to_pathlength_avg:
                if max_path == 0 or avg_path > max_path:
                    max_path =avg_path
            for [street_name, car_amount] in streets_to_cars_tmp:
                if min_cars == 0 or car_amount < min_cars:
                    min_cars = car_amount
                if max_cars == 0 or car_amount > max_cars:
                    max_cars = car_amount
            
            for i in range(len(streets_to_pathlength_avg)):
                voodoo = duration_simulation / 10
                street_name = streets_to_pathlength_avg[i][0]
                avg_path = streets_to_pathlength_avg[i][1]
                car_amount = streets_to_cars_tmp[i][1]
                #print(voodoo)
                # voodoo = i
                #print(total_paths)
                tmp_max_path = max_path
                tmp_min_cars = min_cars
                tmp_max_cars = max_cars
                if min_cars == 0:
                    tmp_min_cars = 1
                if max_cars == 0:
                    tmp_max_cars = 1
                if max_path == 0:
                    tmp_max_path = duration_simulation*2
                if avg_path == 0:
                    avg_path = duration_simulation*2
                
                normalized1 = ((1/avg_path)/(1/tmp_max_path))  * 0.1
                normalized2 = car_amount/tmp_min_cars  * 0.9
                if tmp_max_cars/tmp_min_cars <= 1.5:
                    normalized = 1
                else:

                    normalized = min(duration_simulation,min(street_count, normalized1+normalized2))

                if avg_path != 0:
                    best_streets.append([street_name, int(round(normalized,0))])

            
            
            tmp_counter = 0
            while tmp_counter < len(best_streets):
                if best_streets[tmp_counter][1] == 0:
                    del best_streets[tmp_counter]
                else:
                    tmp_counter += 1
                    
                        
                        
#Nog kijken of  aantal seconden dat een licht op groen is niet groter is dan totaal aantal autos dat er ooit in die straat komt
#dus totale runtime/som(van alle lichten in 1 sequentie) * tijd licht op groen < totaal aantal autos door deze straat
                
            if len(best_streets) > 0:
                schedule.append(str(intersection)+'\n')
                schedule.append(str(len(best_streets))+'\n')
                for best_street in best_streets:
                    
                    schedule.append(best_street[0] + ' ' + str(best_street[1]) + '\n')
                
                schedules.append(schedule)




    # restrict search space to subspaces

    # find solution for subspace


    # add solutions together
    result = [str(len(schedules)) + '\n']
    for sched in schedules:
        for line in sched:
            result.append(line)

    # return solution

    return result

def main():
    filenames = ['a', 'b', 'c', 'd', 'e', 'f']
    #filenames = ['a']
    input_ext = '.txt'
    output_ext = '.out'
    for filename in filenames:
        input_data = parse_input(filename + input_ext)
        solution = get_solution(input_data)
        write_output(filename + output_ext, solution)
        print(f"Filename {filename} done!")

main()


#dict van (keys) intersect nummer met als values set met straat namen

#per intersections aantal straten bijhouden 
#per straat aantal autos dat er door moet
#als er bij intersection maar 1 straat -) altijd groen
#straat zonder auto's altijd rood

#idee 1: prioriteer straat met meeste auto's die minste andere straten blokt
#prioriteer auto's die minder straten moeten

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#tony pseudo voor straks
#                       intersect x 
#            licht 1                   licht 2
# t=0       waiting_list1           waiting_list2
# t=1       waiting_list1           waiting_list2
# t=2       waiting_list1           waiting_list2
# ...
# ...
# t=max       waiting_list1           waiting_list2

# optimale sequentie bepalen? 
# 1: bepaal voor elk tijdstip een 'waarde' van elk licht
# 2: bepaal een 'loopke' dat een best mogelijke score bepaald

# hoe bepalen we 1 en 2 ? 

# 1
# Bekijk de wachtrij van elk licht (auto1, auto2, ..., auto n)
# elke auto heeft een score afhankelijk van hoe ver deze is van zijn eindoel, onder 'ideale' omstandigheden (hoe dichter hoe meer punten)
# extra: een auto die onmogelijk nog zijn einddoel kan halen is nul punten waard. De score van elke auto neemt af naarmate deze verder is in de lijs(schalingsfactor x?)
# nota: hoe weten we waar welke auto staat te wachten? --> veronderstel dat elke auto een perfect pad volgt (iemand betere suggesties?)

# 2
# euhm weet ik nog niet maar lijkt me haalbaar 

# gewenste output is dus iets als:
# voor alle intersecties:
# intersectie x = [ [scorelicht1_t0,scorelicht2_t0], [scorelicht1_t1,scorelicht2_t1], ..., [scorelicht1_tmax,scorelicht2_tmax]
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#Stel 1 straat heeft te veel autos om in tijd te kunnen doen en 1 straat te weining dan straat met te weining negeren
