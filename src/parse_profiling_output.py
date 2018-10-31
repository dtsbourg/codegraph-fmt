import pstats

output_file = './output.txt'
p = pstats.Stats(output_file)
p.strip_dirs().sort_stats(-1).print_stats()
