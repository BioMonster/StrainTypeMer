import os

_ROOT = os.path.abspath(os.path.dirname(__file__))

mlst_urls = {
    'Acinetobacter baumannii Oxf': [
        'http://pubmlst.org/data/profiles/abaumannii.txt',
        'http://pubmlst.org/data/alleles/abaumannii/Oxf_gltA.tfa',
        'http://pubmlst.org/data/alleles/abaumannii/Oxf_gyrB.tfa',
        'http://pubmlst.org/data/alleles/abaumannii/Oxf_gdhB.tfa',
        'http://pubmlst.org/data/alleles/abaumannii/Oxf_recA.tfa',
        'http://pubmlst.org/data/alleles/abaumannii/Oxf_cpn60.tfa',
        'http://pubmlst.org/data/alleles/abaumannii/Oxf_gpi.tfa',
        'http://pubmlst.org/data/alleles/abaumannii/Oxf_rpoD.tfa',
    ],
    'Acinetobacter baumannii Pas': [
        'http://pubmlst.org/data/profiles/abaumannii_2.txt',
        'http://pubmlst.org/data/alleles/abaumannii_2/Pas_cpn60.tfa',
        'http://pubmlst.org/data/alleles/abaumannii_2/Pas_fusA.tfa',
        'http://pubmlst.org/data/alleles/abaumannii_2/Pas_gltA.tfa',
        'http://pubmlst.org/data/alleles/abaumannii_2/Pas_pyrG.tfa',
        'http://pubmlst.org/data/alleles/abaumannii_2/Pas_recA.tfa',
        'http://pubmlst.org/data/alleles/abaumannii_2/Pas_rplB.tfa',
        'http://pubmlst.org/data/alleles/abaumannii_2/Pas_rpoB.tfa',
    ],
    'Enterococcus faecalis': [
        'http://pubmlst.org/data/profiles/efaecalis.txt',
        'http://pubmlst.org/data/alleles/efaecalis/gdh.tfa',
        'http://pubmlst.org/data/alleles/efaecalis/gyd.tfa',
        'http://pubmlst.org/data/alleles/efaecalis/pstS.tfa',
        'http://pubmlst.org/data/alleles/efaecalis/gki.tfa',
        'http://pubmlst.org/data/alleles/efaecalis/aroE.tfa',
        'http://pubmlst.org/data/alleles/efaecalis/xpt.tfa',
        'http://pubmlst.org/data/alleles/efaecalis/yqiL.tfa',
    ],
    'Enterococcus faecium': [
        'http://pubmlst.org/data/profiles/efaecium.txt',
        'http://pubmlst.org/data/alleles/efaecium/atpA.tfa',
        'http://pubmlst.org/data/alleles/efaecium/ddl.tfa',
        'http://pubmlst.org/data/alleles/efaecium/gdh.tfa',
        'http://pubmlst.org/data/alleles/efaecium/purK.tfa',
        'http://pubmlst.org/data/alleles/efaecium/gyd.tfa',
        'http://pubmlst.org/data/alleles/efaecium/pstS.tfa',
        'http://pubmlst.org/data/alleles/efaecium/adk.tfa',
    ],
    'Staphylococcus aureus': [
        'http://pubmlst.org/data/profiles/saureus.txt',
        'http://pubmlst.org/data/alleles/saureus/arcC.tfa',
        'http://pubmlst.org/data/alleles/saureus/aroE.tfa',
        'http://pubmlst.org/data/alleles/saureus/glpF.tfa',
        'http://pubmlst.org/data/alleles/saureus/gmk.tfa',
        'http://pubmlst.org/data/alleles/saureus/pta_.tfa',
        'http://pubmlst.org/data/alleles/saureus/tpi.tfa',
        'http://pubmlst.org/data/alleles/saureus/yqiL.tfa',
    ],
    'Salmonella enterica': [
        'http://pubmlst.org/data/profiles/senterica.txt',
        'http://pubmlst.org/data/alleles/senterica/aroC.tfa',
        'http://pubmlst.org/data/alleles/senterica/dnaN.tfa',
        'http://pubmlst.org/data/alleles/senterica/hemD.tfa',
        'http://pubmlst.org/data/alleles/senterica/hisD.tfa',
        'http://pubmlst.org/data/alleles/senterica/purE.tfa',
        'http://pubmlst.org/data/alleles/senterica/sucA.tfa',
        'http://pubmlst.org/data/alleles/senterica/thrA.tfa',
    ],
    'Escherichia coli' : [
        'http://pubmlst.org/data/profiles/ecoli.txt',
        'http://pubmlst.org/data/alleles/ecoli/adk.tfa',
        'http://pubmlst.org/data/alleles/ecoli/fumC.tfa',
        'http://pubmlst.org/data/alleles/ecoli/gyrB.tfa',
        'http://pubmlst.org/data/alleles/ecoli/icd.tfa',
        'http://pubmlst.org/data/alleles/ecoli/mdh.tfa',
        'http://pubmlst.org/data/alleles/ecoli/purA.tfa',
        'http://pubmlst.org/data/alleles/ecoli/recA.tfa'
    ]


}
