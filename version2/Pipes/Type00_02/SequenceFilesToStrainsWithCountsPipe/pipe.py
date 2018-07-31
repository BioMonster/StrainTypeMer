from Pipes.Type00_02.SequenceFilesToStrainsWithCountsPipe.Actions.KmerCounter import KmerCounter
from Pipes.Type00_02.SequenceFilesToStrainsWithCountsPipe.Models.Strain import Strain
from Pipes.Type00_02.SequenceFilesToStrainsWithCountsPipe.FileUtilities.FileInspector import FileInspector

class SequenceFilesToStrainsWithCountsPipe():


    def runPipe(self, request):
    
        count_args = request['count_args']
        
        file_metadata_list = count_args['file_metadata_list']
        jf_temp_dir = count_args['jf_temp_dir']
        count_cutoff = count_args['count_cutoff']
        quality_filter = count_args['quality_filter']
        
        strains = self.initStrains(file_metadata_list, jf_temp_dir, count_cutoff)
        self.validateStrainList(strains, quality_filter)
      
        KmerCounter().add_counts_to_strains(count_args, strains)
        
        return strains
 
 
########## Private Below ##########

    
    def initStrains(self, file_metadata_list, jf_temp_dir, count_cutoff):
        strains = []
        for file_metadata in file_metadata_list:
            strain = Strain(file_metadata, jf_temp_dir, count_cutoff)
            strains.append(strain)
        return strains
    
    
    def validateStrainList(self, strains, quality_filter):
        
        self.are_labels_unique(strains)
             
        if quality_filter is not None:
            self.are_all_paths_fastq(strains)
            
    
    def are_all_paths_fastq(self, strains):
        for strain in strains:
            if not FileInspector().are_all_paths_fastq(strain.sequence_file_paths):
                raise TypeError('It was specified that bases should be filtered based on quality during '
                                'comparision but not all files are in fastq format')
     
              
    def are_labels_unique(self, strains):
        labels_list = []
        for strain in strains:
            labels_list.append(strain.label)
        if len(labels_list) > len(set(labels_list)):
            raise NameError('Every sequence set needs unique label')