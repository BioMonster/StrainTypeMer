import magic
import gzip
import os

class FileInspector:
    
    
    def is_gzipped(self,path):
        if 'gzip' in magic.from_file(path, mime=True):
            return True
        return False
    
    
    def is_plain_text(self, path):
        return magic.from_file(path, mime=True) == 'text/plain'
    
    
    def is_fasta(self, path):
        return self.read_first_character_in_file(path) == '>'
    
    
    def is_fastq(self, path):
        return self.read_first_character_in_file(path) == '@'
    
    
    def do_all_file_paths_exist(self, paths, raiseErrorOnFalse = False):
        for path in paths:
            if not os.path.isfile(path):
                if raiseErrorOnFalse:
                    raise IOError('{0} is not a valid file path'.format(path))
                else:
                    return False
        return True

        
    def are_paths_fasta_or_fastq(self, paths, raiseErrorOnFalse = False):
        for path in paths:
            if not (self.is_fasta(path) or self.is_fastq(path)):
                if raiseErrorOnFalse:
                    raise TypeError('File {0} is not fastq or fastq'.format(path))
                else:
                    return False
        return True
       
            
    def are_all_paths_fastq(self, paths):
        for path in paths:
            if not self.is_fastq(path):
                return False
        return True
    
    
########## Private Below ##########

        
    def read_first_character_in_file(self, path):
        if self.is_gzipped(path):
            with gzip.open(path,'r') as file:
                return file.readline().decode()[0]
        elif self.is_plain_text(path):
            with open(path, 'r') as file:
                return file.readline()[0]
        raise TypeError('File {0} is not plain/text or gzipped plain/text'.format(path))