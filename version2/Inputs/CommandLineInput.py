import argparse
from argparse import ArgumentParser
from Pipes.Type00_02.SequenceFilesToStrainsWithCountsPipe.pipe import SequenceFilesToStrainsWithCountsPipe

class CommandLineInput:
    
    def runInput(self):
        args = self.parseArgv()
        request = self.convertArgsToRequest(args)
        self.runCommand(request)
        

########## Private Below ##########

        
    def parseArgv(self):

        parser = ArgumentParser(prog = 'main',
                                description = 'count, compare, plot, updateMLST for strains',
                                formatter_class = argparse.RawDescriptionHelpFormatter)
        
        subparsers = parser.add_subparsers(title = 'sub-commands',
                                           dest = 'subparser_name',
                                           help = 'sub-command help')
        
        
        ########## Count-Compare Parent Command Parser Below ##########
        
        
        count_compare_parent_arg_parser = ArgumentParser(description = 'count-compare', add_help = False)
        
        count_compare_parent_arg_parser.add_argument('-t',
                                                     '--cpus',
                                                     type = int,
                                                     default = 1,
                                                     help = 'The number of cpus to use [Default: 1]')
        
#         count_compare_parent_arg_parser.add_argument('--no_kmer_filtering',
#                                                      action = 'store_true',
#                                                      default = False,
#                                                      help = 'Do not filter kmers based on coverage; '
#                                                             'useful when comparing reference sequences')
        
        count_compare_parent_arg_parser.add_argument('--count_cutoff',
                                                     type = int,
                                                     default = 0,
                                                     help = 'Filter kmers based on count')
        
        count_compare_parent_arg_parser.add_argument('-q',
                                                     '--qual_score',
                                                     type = int,
                                                     default = None,
                                                     help = 'The phred score to filter bases')
        
        count_compare_parent_arg_parser.add_argument('--coverage_cutoff',
                                                     type = float,
                                                     default = 0.2,
                                                     help = 'percent of genome coverage to set kmer filters '
                                                            '[DEFAULT 0.20 if coverage is 30 [(30 * 0.2) = 6] kmers '
                                                            ' with a count < 5 will be ignored for corresponding strain')
        
        count_compare_parent_arg_parser.add_argument('file_metadata',
                                                     nargs = '*',
                                                     help = 'fastq files for each strain (fq1 OR fq1;label OR fq1,fq2; '
                                                            'label will be matching string of the two files OR fq1,fq2; '
                                                            'label included "[NF]" at the end to prevent kmer filter '
                                                            '(useful when adding a reference genome)')
        
        count_compare_parent_arg_parser.add_argument('-verbose',
                                                     '--verbose_stdout',
                                                     action = 'store_true',
                                                     default = False,
                                                     help = 'Will print extra information to stdout')
        
        count_compare_parent_arg_parser.add_argument('-gz',
                                                     '--gzipped',
                                                     action = 'store_true',
                                                     default = False,
                                                     help = 'flag to indicate fastq/a files are '
                                                            'gzipped [DEFAULT FALSE]')
        
        count_compare_parent_arg_parser.add_argument('-jtd',
                                                     '--jf_temp_dir',
                                                     type = str,
                                                     default = 'temp/',
                                                     help = 'The directory where jf files can be stored')

        
        ########## Compare Command Parser Below ##########
        
        
        compare_arg_parser = subparsers.add_parser('compare',
                                                    parents = [count_compare_parent_arg_parser],
                                                    help = 'compare strains')
         
        compare_arg_parser.add_argument('-k',
                                        '--kmer_reference',
                                        type = str,
                                        default = None,
                                        help = 'Use kmer reference set for comparison (e.g plasmid core genome, '
                                               'pan genome kmers; [ONLY COMPARE KMERS IN THIS FILE]')
         
        compare_arg_parser.add_argument('-r',
                                        '--inverse_kmer_reference',
                                        type = str,
                                        default = None,
                                        help = 'Use kmer reference set for comparison (e.g plasmid core genome, '
                                               'pan genome kmers; [ONLY COMPARE KMERS NOT IN THIS FILE]')
         
        compare_arg_parser.add_argument('-kr',
                                        '--inverse_and_kmer_reference',
                                        type = str,
                                        default = None,
                                        help = argparse.SUPPRESS)
         
        compare_arg_parser.add_argument('--do_not_output_histograms',
                                        action = 'store_false',
                                        default = True,
                                        help = 'This will prevent the output of the PDF files containing the histograms')
         
        compare_arg_parser.add_argument('--do_not_output_matrix',
                                        action = 'store_false',
                                        default = True,
                                        help = 'This will prevent the output of the PDF files containing the matrix')
         
        compare_arg_parser.add_argument('--no_pdfs',
                                        action = 'store_true',
                                        default = False,
                                        help = 'Output will only go to stdout')
         
        compare_arg_parser.add_argument('-o',
                                        '--output_prefix',
                                        default = '',
                                        help = 'appends a prefix to the output files')
         
        compare_arg_parser.add_argument('-pwf',
                                        '--pairwise_kmer_filter',
                                        action = 'store_true',
                                        default = False,
                                        help = 'Evaluate non-shared kmers in closely related strains')
         
        compare_arg_parser.add_argument('-ard',
                                        '--include_ard_comparison',
                                        action = 'store_true',
                                        default = False,
                                        help = 'include comparison with ard genes')
         
        compare_arg_parser.add_argument('--rapid_mode',
                                        action = 'store_true',
                                        default = False,
                                        help = 'analyze a subset of kmers')
         
        compare_arg_parser.add_argument('-kf',
                                        '--keep_files',
                                        action = 'store_false',
                                        default = True,
                                        help = argparse.SUPPRESS)
         
        compare_arg_parser.add_argument('-jf',
                                        '--jf_input',
                                        action = 'store_true',
                                        default = False,
                                        help = argparse.SUPPRESS)
         
        
        ########## Count Command Parser Below ##########
        
        
        count_arg_parser = subparsers.add_parser('count',
                                                 parents = [count_compare_parent_arg_parser],
                                                 help = 'count kmers in strains')
         
        count_arg_parser.add_argument('-l',
                                      '--label',
                                        default = None,
                                        help = 'the label to attach to the file')
         
        count_arg_parser.add_argument('-o',
                                      '--out',
                                        help = 'the output file')
        
        
        ########## Plot Command Parser Below ##########
        
        
        plot_arg_parser = subparsers.add_parser('plot',
                                                 help = 'plot results from standard out')
        
        plot_arg_parser.add_argument('-i',
                                     '--input',
                                     type = argparse.FileType('r'),
                                     required = True,
                                     help = 'the input file')
        
        plot_arg_parser.add_argument('-o',
                                     '--output_prefix',
                                     type = argparse.FileType('w'),
                                     required = True,
                                     help = 'the output file')
        
        
        ########## Update MLST Command Parser Below ##########
        
        plot_arg_parser = subparsers.add_parser('update_mlst',
                                                 help = 'update mlst resources')
        
        
        ########## Parse Below ##########
        
        
        args = parser.parse_args()
        
        return args
        
        
        ########## Convert to Dictionary Format ##########
        
    def convertArgsToRequest(self, args):
    
        request = {}
        
        if args.subparser_name == 'count':
            request = {
                'name': 'count',
                'count_args': {
                        'file_metadata_list': args.file_metadata,
                        'cpus': args.cpus,
#                         'no_kmer_filtering': args.no_kmer_filtering,  
                        'count_cutoff': args.count_cutoff,
                        'quality_filter': args.qual_score,
                        'jf_temp_dir': args.jf_temp_dir,
                        'kmer_length': 31,
                        'gzipped': args.gzipped,
                        'label': args.label,
                        'o': args.out,
                        'coverage_cutoff': args.coverage_cutoff,
                        'verbose_stdout': args.verbose_stdout,
                        'hash_size': '500M'
                    }
                }
        elif args.subparser_name == 'compare':
            request = {
                'name': 'compare',
                'count_args': {
                        'file_metadata_list': args.file_metadata,
                        'cpus': args.cpus,
#                         'no_kmer_filtering': args.no_kmer_filtering,  
                        'count_cutoff': args.count_cutoff,
                        'quality_filter': None if args.qual_score is None else args.qual_score,
                        'is_jellyfish_input': args.jf_input,
                        'jf_temp_dir': args.jf_temp_dir,
                        'kmer_length': 31,
                        'gzipped': args.gzipped,
                        'verbose_stdout': args.verbose_stdout,
                        'hash_size': '500M'
                    },
                'compare_args': {   
                        'cpus': args.cpus,      
                        'coverage_cutoff': args.coverage_cutoff,
                        'do_not_output_matrix': args.do_not_output_matrix,
                        'do_not_output_histograms': args.do_not_output_histograms,
                        'output_prefix': args.output_prefix,
                        'kmer_reference': args.kmer_reference,
                        'inverse_kmer_reference': args.inverse_kmer_reference,
                        'pairwise_kmer_filter': args.pairwise_kmer_filter,
                        'rapid_mode': args.rapid_mode,
                        'include_ard_comparison': args.include_ard_comparison,
                        'keep_files': args.keep_files,
                        'no_pdfs': args.no_pdfs,
                        'verbose_stdout': args.verbose_stdout,
                        'inverse_and_kmer_reference': args.inverse_and_kmer_reference
                    }
                }
        elif args.subparser_name == 'plot':
            request = {
                'name': 'plot',
                'plot_args': {
                    'input': args.input,
                    'output_prefix': args.output_prefix
                    }
                }   
        elif args.subparser_name == 'update_mlst':
            request = {
                    'name': 'update_mlst',
                    'update_mlst_args': {}
                }
        
        return request;
    
    def runCommand(self, request):
        command_name = request['name']
        if command_name == 'count':
            pass
        if command_name == 'compare':
            SequenceFilesToStrainsWithCountsPipe().runPipe(request)
            #Then run a pipe that comes after the one above
        if command_name == 'plot':
            pass
        if command_name == 'update_mlst':
            pass