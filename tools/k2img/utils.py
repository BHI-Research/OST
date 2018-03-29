def print_object_in_file(obj, file):
    format_obj = vars(obj)
    for i in format_obj:
        if (format_obj[i] != 0):
            file.write("\t-" + i + "\t=\t" +  str(format_obj[i]) + '\n')


def output_label(parameters):
    file = open('output.txt','a')
    time = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    file.write('\n' +"*"*140 + '\n')
    if(parameters.label):
        file.write(parameters.label + "\t\tEvaluation date: " + time + '\n')
    else:
        file.write("Evaluation date: " + time + '\n')
    print_object_in_file(parameters,file)
    file.write("*"*140 + '\n')
    file.write("\t\t\tusers path\t\t\t\t\tdata path\t\t\t\tCUSa\t\tCUSe\t\tprecision\trecall\t\tF-meter\t\tCohen's Kappaaa\n")

    file.close()

