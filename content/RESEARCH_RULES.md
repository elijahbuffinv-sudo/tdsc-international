# Research rules for this batch (read before starting)

1. **No approval prompts.** Only WebFetch URLs that appeared in YOUR OWN WebSearch results (or links inside a page you already fetched). Never fetch an address you typed from memory — that interrupts the user with an approval prompt. If a page you need never appears in results, rely on what the search snippets say and flag it.
2. **Search budget.** At most 2 WebSearch calls per jurisdiction or city. Make them count: e.g. "<country> data protection law regulator private investigator licence" and "<country> company registry beneficial ownership anti-corruption law". Search snippets themselves are usable evidence; cite the result URL.
3. **Population.** Use a World Bank or national statistics result that appears in your searches; otherwise cite whatever authoritative result you found and flag it.
4. **Sources.** At least 5 real URLs per file, each one either fetched or shown in your search results. Never invent a URL.
5. Do not use the scratchpad for shared scripts — another agent may overwrite it. Validate with `python3 -m json.tool <file> > /dev/null` and count meta_description length with python inline.
6. Work file by file; write each JSON as soon as it is done.
