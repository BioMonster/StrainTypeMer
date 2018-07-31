import argparse
from argparse import ArgumentParser
from Pipes.Type00_02.SequenceFilesToStrainsWithCountsPipe.pipe import SequenceFilesToStrainsWithCountsPipe

class CommandLineInput:
    
    def runInput(self):
        args = self.parseArgv()
        request = self.convertArgsToRequest(args)
        self.runPipe(request)
        

########## Private Below ##########

        
    def parseArgv(self):

        parser = ArgumentParser(prog = 'StrainTyper',
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
        
         
        ########## Parse Below ##########
        
        
        args = parser.parse_args()
        
        return args
        
        
        ########## Convert to Dictionary Format ##########
        
    def convertArgsToRequest(self, args):
    
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
   
        return request;
    
    def runPipe(self, request):
        SequenceFilesToStrainsWithCountsPipe.runPipe(request)