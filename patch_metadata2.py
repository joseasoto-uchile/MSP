import json
import re

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

for p in papers:
    pid = p.get('id')
    
    # Ensure bibtex is a list
    if 'bibtex' in p and isinstance(p['bibtex'], str):
        p['bibtex'] = [p['bibtex']]
        
    # Kesselheim fix (specifically requested)
    if pid == "kesselheim2013":
        p['versions'] = ["arXiv preprint version", "ESA 2013 version"]
        
    # Oveis Gharan fix
    elif pid == "oveisgharan2013":
        p['versions'] = ["arXiv preprint version", "ESA 2011 version", "Algorithmica 2013 version"]
        
    # Huynh & Nelson
    elif pid == "huynh2016":
        p['versions'] = ["arXiv preprint version", "SIAM J. Discrete Math. 2020 version"]
        
    # Dinitz & Kortsarz
    elif pid == "dinitz2013":
        p['versions'] = ["arXiv preprint version", "SODA 2013 version", "SIAM J. Comput. 2014 version"]
        
    # Jaillet, Soto, Zenklusen
    elif pid == "jaillet2013":
        p['versions'] = ["arXiv preprint version", "IPCO 2013 version", "Math. Oper. Res. 2016 version"]
        
    # Soto, Turkieltaub, Verdugo
    elif pid == "soto2018":
        p['versions'] = ["arXiv preprint version", "SODA 2018 version", "Math. Oper. Res. 2021 version"]
        
    # Feldman, Svensson, Zenklusen
    elif pid == "feldman2015":
        p['versions'] = ["arXiv preprint version", "SODA 2015 version", "SIAM J. Comput. 2022 version"]
        
    # Lachish
    elif pid == "lachish2014":
        p['versions'] = ["arXiv preprint version", "FOCS 2014 version"]
        
    # Ma, Tang, Wang
    elif pid == "ma2013":
        p['versions'] = ["arXiv preprint version", "STACS 2013 version", "Theory Comput. Syst. 2016 version"]
        
    # Babaioff et al.
    elif pid == "babaioff2007":
        p['versions'] = ["arXiv preprint version", "SODA 2007 version"]
        if len(p['bibtex']) == 1:
            p['bibtex'].append("""@article{babaioff2007corr,
  title={Matroids, Secretary Problems, and Online Mechanisms},
  author={Babaioff, Moshe and Immorlica, Nicole and Kleinberg, Robert},
  journal={CoRR},
  volume={abs/0711.4884},
  year={2007}
}""")

    # Chakraborty & Lachish
    elif pid == "chakraborty2012":
        p['versions'] = ["arXiv preprint version", "SODA 2012 version"]
        if len(p['bibtex']) == 1:
            p['bibtex'].append("""@article{chakraborty2012corr,
  title={Improved Competitive Ratio for the Matroid Secretary Problem},
  author={Chakraborty, Sourav and Lachish, Oded},
  journal={CoRR},
  volume={abs/1202.1643},
  year={2012}
}""")

    # Dimitrov & Plaxton
    elif pid == "dimitrov2012":
        p['versions'] = ["arXiv preprint version", "ICALP 2012 version"]
        if len(p['bibtex']) == 1:
            p['bibtex'].append("""@article{dimitrov2012corr,
  title={Competitive Weighted Matching in Transversal Matroids},
  author={Dimitrov, Nenad and Plaxton, C. Greg},
  journal={CoRR},
  volume={abs/1204.6062},
  year={2012}
}""")

    # Im & Wang
    elif pid == "im2011":
        p['versions'] = ["arXiv preprint version", "SODA 2011 version"]
        if len(p['bibtex']) == 1:
            p['bibtex'].append("""@article{im2011corr,
  title={Secretary Problems: Laminar Matroid and Intersection of Matroids},
  author={Im, Sungjin and Wang, Yajun},
  journal={CoRR},
  volume={abs/1105.3526},
  year={2011}
}""")

    # Check if there are other papers lacking the arXiv explicitly in 'versions'
    # but having multiple bibtex entries
    elif isinstance(p.get('bibtex', []), list) and len(p.get('bibtex', [])) > 1:
        pass # Already handled manually above
        
with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
    
print("Metadata patched successfully!")
