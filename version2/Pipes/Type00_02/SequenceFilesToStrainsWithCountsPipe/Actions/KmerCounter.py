import sys
import random
import string
import subprocess
from Pipes.Type00_02.SequenceFilesToStrainsWithCountsPipe.FileUtilities.FileInspector import FileInspector


class KmerCounter:
    
    #Should be deprecated in favor of pipes that will parallelize on a strain basis
    def add_counts_to_strains(self, count_args, strains):
    
        verbose_stdout = count_args['verbose_stdout']
        cpus = count_args['cpus']
        hash_size = count_args['hash_size']
        quality_filter = count_args['quality_filter']
        kmer_length = count_args['kmer_length']
        directory = count_args['jf_temp_dir']
        
        for i, strain in enumerate(strains):
            
            file_paths = strain.sequence_file_paths
            label = strain.label
            jellyfish_temp_file_path_str = self.generate_jellyfish_temp_file_path_str(directory, label)
            
            if verbose_stdout:
                self.count_kmers_verbose_stdout(strain, label, i)
                
            flags = [{'name': 'canonical',
                     'flag_key': '-C',
                     'value': None
                     },
                    {'name': 'count_cutoff',
                     'flag_key': '-L',
                     'value': str(strain.count_cutoff)
                     },
                    {'name': 'cpus',
                     'flag_key': '-t',
                     'value': str(cpus)
                     },
                    {'name': 'hash_size',
                     'flag_key': '-s',
                     'value': str(hash_size)
                     },
                    {'name': 'jellyfish_temp_file_path_str',
                     'flag_key': '-o',
                     'value': jellyfish_temp_file_path_str
                     },
                    {'name': 'kmer_length',
                     'flag_key': '-m',
                     'value': str(kmer_length)
                     },
                    {'name': 'number_of_files',
                     'flag_key': '-F',
                     'value': str(len(file_paths))
                        }]
            
            if quality_filter is not None:
                phred33 = quality_filter + 33
                flags.append({
                 'name': 'quality_filter',
                 'flag_key': '-Q',
                 'value': self.get_quality_filter_chr(phred33)
                 })
                       
            #Use Docker instead here, for now assume jellyfish is on the path
#             program = '../../Desktop/Jellyfish/jellyfish-linux'
            program = 'jellyfish'
                                                               
            jellyfish_count_command_str = self.create_command_str(program, 'count', flags, file_paths)
             
            #change this to use Popen or use shlex.split at least                
            subprocess.check_call(jellyfish_count_command_str, shell = True,  executable='/bin/bash')
             
            strain.jellyfish_file_path = jellyfish_temp_file_path_str
    

########## Private Below ##########

    
    def generate_jellyfish_temp_file_path_str(self, directory, label):
        eight_random_uppercase_letters = ''.join(random.choice(string.ascii_uppercase) for i in range(8))
        return '{0}temp_{1}_{2}.jf'.format(directory, label, eight_random_uppercase_letters)


    def count_kmers_verbose_stdout(self, file_metadata, label, i):
        list_len = len(file_metadata)
        sys.stdout.write('\rcounting kmers in strain {0} of {1}: {2}{3}\n'
                                 .format(i+1, len(list_len),label, ' ' * 30))
        sys.stdout.flush()
        
        
    def get_quality_filter_chr(self, phred33):
        return self.escape_quality_filter_chr(chr(phred33))
        
        
    def escape_quality_filter_chr(self, phred33):
        if ord(phred33) in [34, 92, 96]:
            return "'" + str(phred33) + "'"
        else:
            return '"' + str(phred33) + '"'
          
              
    def create_command_str(self, program_name, command_name, flags, file_paths):  
        command_str = program_name + ' ' + command_name
        command_str = self.append_flags_to_command_str(command_str, flags)
        command_str = self.append_file_paths_to_command_str(command_str, file_paths)
        return command_str  
         
            
    def append_flags_to_command_str(self, command_str, flags):
        for flag in flags:
            command_str += ' ' + flag['flag_key']
            if flag['value'] is not None:
                command_str += ' ' + flag['value']
        return command_str
     
     
    def append_file_paths_to_command_str(self, command_str, file_paths):
            for path in file_paths:
                if FileInspector().is_gzipped(path):
                    command_str += ' <(zcat {0})'.format(path)
                else:
                    command_str += ' <(cat {0})'.format(path)
            return command_str