import os
import re
import copy
from Pipes.Type00_02.SequenceFilesToStrainsWithCountsPipe.FileUtilities.FileInspector import FileInspector

class Strain:
    
    
    label = None
    sequence_file_paths = []
    jellyfish_directory = None
    jellyfish_file_path = None
    count_cutoff = 0
    
    
    def __init__(self, file_metadata, jf_temp_dir, count_cutoff):
         
        file_metadata = copy.deepcopy(file_metadata)
          
        count_cutoff = count_cutoff if self.should_filter_kmers(file_metadata) else 0
        self.count_cutoff = count_cutoff
            
        file_paths_and_label = file_metadata.replace('[NF]', '')
        
        self.set_label(file_paths_and_label)

        file_paths = file_paths_and_label.replace(':' + self.label, '').split(',')
        
        self.set_sequence_file_paths(file_paths)
        self.jellyfish_directory = jf_temp_dir
        self.set_jellyfish_directory(jf_temp_dir)
            
         
    ########## Private Below ##########
   
               
    def should_filter_kmers(self, file_metadata):
        if '[NF]' in file_metadata:
            return False
        return True
            
        
    def set_jellyfish_directory(self, directory):
        self.jellyfish_directory = os.path.dirname(directory)
        if not os.path.isdir(directory):
            raise IOError('{0} is not a valid directory'.format(directory))
    

    def set_sequence_file_paths(self, file_paths):
        self.sequence_file_paths = file_paths
        FileInspector().do_all_file_paths_exist(self.sequence_file_paths, True)
        FileInspector().are_paths_fasta_or_fastq(self.sequence_file_paths, True)
    

    def set_label(self, file_paths_and_label):
        if self.label_is_not_empty(file_paths_and_label):
            self.label = file_paths_and_label.split(':')[1]
        else:
            self.label = self.make_label(file_paths_and_label)
                
 
    def make_label(self, file_paths_and_label):
        file_paths = file_paths_and_label.split(':')[0].split(',')
        file_basenames = []
        for path in file_paths:
            file_basenames.append(os.path.basename(path))
        label = os.path.commonprefix(file_basenames)
        if len(label) == 0:
            raise NameError('File names must have a common prefix of at least ' 
                                'one for a label to be autogenerated')
        return label
  
  
    def label_is_not_empty(self, file_paths_and_label):
        pattern = re.compile('.*:.+')
        return True if pattern.match(file_paths_and_label) else False