import json

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

fixes = {
    # 1. Kesselheim
    "kesselheim2013": {
        "title": "An Optimal Online Algorithm for Weighted Bipartite Matching and Extensions to Combinatorial Auctions",
        "venue": "ESA 2013",
        "bibtex": [
            """@inproceedings{kesselheim2013optimal,
  title={An Optimal Online Algorithm for Weighted Bipartite Matching and Extensions to Combinatorial Auctions},
  author={Kesselheim, Thomas and Radke, Klaus and T{\\\"o}nnis, Andreas and V{\\\"o}cking, Berthold},
  booktitle={Algorithms - ESA 2013 - 21st Annual European Symposium, Sophia Antipolis, France, September 2-4, 2013. Proceedings},
  pages={589--600},
  year={2013},
  organization={Springer}
}""",
            """@article{kesselheim2013corr,
  title={An Optimal Online Algorithm for Weighted Bipartite Matching and Extensions to Combinatorial Auctions},
  author={Kesselheim, Thomas and Radke, Klaus and T{\\\"o}nnis, Andreas and V{\\\"o}cking, Berthold},
  journal={CoRR},
  volume={abs/1307.2435},
  year={2013}
}"""
        ]
    },
    
    # 2. Oveis Gharan
    "oveisgharan2013": {
        "bibtex": [
            """@article{oveisgharan2013variants,
  title={On Variants of the Matroid Secretary Problem},
  author={Oveis Gharan, Shayan and Vondr{\\\'a}k, Jan},
  journal={Algorithmica},
  volume={67},
  number={4},
  pages={475--497},
  year={2013},
  publisher={Springer}
}""",
            """@inproceedings{oveisgharan2011variants,
  title={On Variants of the Matroid Secretary Problem},
  author={Oveis Gharan, Shayan and Vondr{\\\'a}k, Jan},
  booktitle={Algorithms - ESA 2011 - 19th Annual European Symposium, Saarbr{\\\"u}cken, Germany, September 5-9, 2011. Proceedings},
  pages={333--344},
  year={2011},
  organization={Springer}
}""",
            """@article{oveisgharan2011corr,
  title={On Variants of the Matroid Secretary Problem},
  author={Oveis Gharan, Shayan and Vondr{\\\'a}k, Jan},
  journal={CoRR},
  volume={abs/1104.2838},
  year={2011}
}"""
        ]
    },
    
    # 3. Huynh & Nelson
    "huynh2016": {
        "bibtex": [
            """@article{huynh2020matroid,
  title={The Matroid Secretary Problem for Minor-Closed Classes and Random Matroids},
  author={Huynh, Tony and Nelson, Peter},
  journal={SIAM J. Discrete Math.},
  volume={34},
  number={3},
  pages={1514--1526},
  year={2020},
  publisher={SIAM}
}""",
            """@article{huynh2016corr,
  title={The Matroid Secretary Problem for Minor-Closed Classes and Random Matroids},
  author={Huynh, Tony and Nelson, Peter},
  journal={CoRR},
  volume={abs/1609.08389},
  year={2016}
}"""
        ]
    },
    
    # 4. Dinitz & Kortsarz
    "dinitz2013": {
        "bibtex": [
            """@article{dinitz2014matroid,
  title={Matroid Secretary for Regular and Decomposable Matroids},
  author={Dinitz, Michael and Kortsarz, Guy},
  journal={SIAM J. Comput.},
  volume={43},
  number={5},
  pages={1807--1830},
  year={2014},
  publisher={SIAM}
}""",
            """@inproceedings{dinitz2013matroid,
  title={Matroid secretary for regular and decomposable matroids},
  author={Dinitz, Michael and Kortsarz, Guy},
  booktitle={Proceedings of the Twenty-Fourth Annual ACM-SIAM Symposium on Discrete Algorithms},
  pages={522--536},
  year={2013},
  organization={SIAM}
}""",
            """@article{dinitz2012corr,
  title={Matroid secretary for regular and decomposable matroids},
  author={Dinitz, Michael and Kortsarz, Guy},
  journal={CoRR},
  volume={abs/1206.5057},
  year={2012}
}"""
        ]
    },
    
    # 5. Jaillet, Soto, Zenklusen
    "jaillet2013": {
        "bibtex": [
            """@article{jaillet2016advances,
  title={Advances on Matroid Secretary Problems: Free Order Model and Laminar Case},
  author={Jaillet, Patrick and Soto, Jos{\\\'e} A. and Zenklusen, Rico},
  journal={Math. Oper. Res.},
  volume={41},
  number={3},
  pages={768--788},
  year={2016},
  publisher={INFORMS}
}""",
            """@inproceedings{jaillet2013advances,
  title={Advances on Matroid Secretary Problems: Free Order Model and Laminar Case},
  author={Jaillet, Patrick and Soto, Jos{\\\'e} A. and Zenklusen, Rico},
  booktitle={Integer Programming and Combinatorial Optimization - 16th International Conference, IPCO 2013, Valpara{\\'i}so, Chile, March 18-20, 2013. Proceedings},
  pages={254--265},
  year={2013},
  organization={Springer}
}""",
            """@article{jaillet2012corr,
  title={Advances on Matroid Secretary Problems: Free Order Model and Laminar Case},
  author={Jaillet, Patrick and Soto, Jos{\\\'e} A. and Zenklusen, Rico},
  journal={CoRR},
  volume={abs/1210.1558},
  year={2012}
}"""
        ]
    },
    
    # 6. Soto, Turkieltaub, Verdugo
    "soto2018": {
        "bibtex": [
            """@article{soto2021strong,
  title={Strong Algorithms for the Ordinal Matroid Secretary Problem},
  author={Soto, Jos{\\\'e} A. and Turkieltaub, Abner and Verdugo, Victor},
  journal={Math. Oper. Res.},
  volume={46},
  number={4},
  pages={1514--1536},
  year={2021},
  publisher={INFORMS}
}""",
            """@inproceedings{soto2018strong,
  title={Strong Algorithms for the Ordinal Matroid Secretary Problem},
  author={Soto, Jos{\\\'e} A. and Turkieltaub, Abner and Verdugo, Victor},
  booktitle={Proceedings of the Twenty-Ninth Annual ACM-SIAM Symposium on Discrete Algorithms},
  pages={1558--1577},
  year={2018},
  organization={SIAM}
}""",
            """@article{soto2017corr,
  title={Strong Algorithms for the Ordinal Matroid Secretary Problem},
  author={Soto, Jos{\\\'e} A. and Turkieltaub, Abner and Verdugo, Victor},
  journal={CoRR},
  volume={abs/1706.01429},
  year={2017}
}"""
        ]
    },
    
    # 7. Feldman, Svensson, Zenklusen
    "feldman2015": {
        "bibtex": [
            """@article{feldman2022simple,
  title={A Simple $O(\log \log rank)$-Competitive Algorithm for the Matroid Secretary Problem},
  author={Feldman, Moran and Svensson, Ola and Zenklusen, Rico},
  journal={SIAM J. Comput.},
  volume={51},
  number={4},
  pages={1010--1045},
  year={2022},
  publisher={SIAM}
}""",
            """@inproceedings{feldman2015simple,
  title={A simple $O(\log \log rank)$-competitive algorithm for the matroid secretary problem},
  author={Feldman, Moran and Svensson, Ola and Zenklusen, Rico},
  booktitle={Proceedings of the Twenty-Sixth Annual ACM-SIAM Symposium on Discrete Algorithms},
  pages={1189--1204},
  year={2015},
  organization={SIAM}
}""",
            """@article{feldman2014corr,
  title={A simple $O(\log \log rank)$-competitive algorithm for the matroid secretary problem},
  author={Feldman, Moran and Svensson, Ola and Zenklusen, Rico},
  journal={CoRR},
  volume={abs/1404.4754},
  year={2014}
}"""
        ]
    },
    
    # 8. Lachish
    "lachish2014": {
        "bibtex": [
            """@inproceedings{lachish2014olog,
  title={O(log log rank) Competitive Ratio for the Matroid Secretary Problem},
  author={Lachish, Oded},
  booktitle={55th Annual IEEE Symposium on Foundations of Computer Science, FOCS 2014, Philadelphia, PA, USA, October 18-21, 2014},
  pages={326--335},
  year={2014},
  organization={IEEE Computer Society}
}""",
            """@article{lachish2014corr,
  title={O(log log rank) Competitive Ratio for the Matroid Secretary Problem},
  author={Lachish, Oded},
  journal={CoRR},
  volume={abs/1402.1311},
  year={2014}
}"""
        ]
    },
    
    # 9. Ma, Tang, Wang
    "ma2013": {
        "bibtex": [
            """@article{ma2016simulated,
  title={The Simulated Greedy Algorithm for Several Submodular Matroid Secretary Problems},
  author={Ma, Will and Tang, Zhihao and Wang, Yajun},
  journal={Theory Comput. Syst.},
  volume={59},
  number={4},
  pages={577--595},
  year={2016},
  publisher={Springer}
}""",
            """@inproceedings{ma2013simulated,
  title={The Simulated Greedy Algorithm for Several Submodular Matroid Secretary Problems},
  author={Ma, Will and Tang, Zhihao and Wang, Yajun},
  booktitle={30th International Symposium on Theoretical Aspects of Computer Science, STACS 2013, February 27 - March 2, 2013, Kiel, Germany},
  pages={386--397},
  year={2013},
  organization={Schloss Dagstuhl - Leibniz-Zentrum f{\\"u}r Informatik}
}""",
            """@article{ma2013corr,
  title={The Simulated Greedy Algorithm for Several Submodular Matroid Secretary Problems},
  author={Ma, Will and Tang, Zhihao and Wang, Yajun},
  journal={CoRR},
  volume={abs/1301.2754},
  year={2013}
}"""
        ]
    }
}

for p in papers:
    pid = p.get('id')
    if pid in fixes:
        for k, v in fixes[pid].items():
            p[k] = v
            
with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
    
print("Metadata patched successfully!")
