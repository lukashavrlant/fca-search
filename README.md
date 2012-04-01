# FCA Search Engine CLaSeek
## O vyhledávači CLaSeek
CLaSeek (Concept Lattice Seeker) je vyhledávač napsaný v Pythonu 3. Na vstupu bere seznam odkazů na dokumenty dostupné přes web, tyto dokumenty (HTML, PDF, ODT) stáhne, zaindexuje a umožňuje nad nimi vyhledávat. 

Dále při každém dotazu provádí vyhledávař dodatečnou analýzu prostřednictvím [formální konceptuální analýzy](http://en.wikipedia.org/wiki/Formal_concept_analysis) a snaží se uživateli, kromě výsledků samotných, nabídnout i návrhy na úpravu dotazu. Nabízí celkem tři různé druhy úprav:

- odstranění klíčového slova z dotazu,
- změna některých klíčových slov v dotazu,
- přidání klíčového slova k dotazu. 

## Jak zprovoznit CLaSeek
Popis instalace a použití CLaSeeku je napsán na [wiki stránce](https://github.com/havrlant/fca-search/wiki). Dále je potřeba [nainstalovat webové rozhraní](https://github.com/havrlant/fca-search-web) nad tímto vyhledávačem.