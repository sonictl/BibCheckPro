
Assistance with enhancements, feature requests and bug fixes are all very welcome!

Any Pull Rrequest will be reviewed promptly.

BibLatex-Check
==============

**A web based version of this checker is now available: https://biblatex-linter.herokuapp.com/** [(repo)](https://github.com/Pezmc/BibLatex-Linter)

*A python2/3 script for checking BibLatex .bib files*

BibTeX Check is a small Python script that goes through a list of references and checks if certain required fields are available, for instance, if each publication is assigned a year or if a journal article has a volume and issue number.

Additionally, it allows for consistency checks of names of conference proceedings and could easily be extended to other needs.

The results of the check are printed to an html file, which includes links to Google Scholar, DBLP, etc. for each flawed reference. These links help retrieving missing information and correcting the entries efficiently.

Please note that it is **not a BibLaTeX validator**. And in the current version, it might not yet be able to parse every valid bib file. The software targets the specific needs of Computer Scientist, but may be applicable in other fields as well.

For use in automated environments, BibLaTeX-Check returns errors on the console (can be disabled).
Further, it returns an exit code depending on whether problems have been found.

The html output is tested with Firefox and Chrome, but the current version does not properly work with Internet Explorer.

## Getting Started

Just copy the file into a directory with write permission, then run the script

	./biblatex_check.py <-b input.bib> [-a input.aux] [-o output/output.html]

If you provide the additional aux file (created when compiling a tex document), then the check of the bib file is restricted to only those entries that are really cited in the tex document.

## Options

Specify these when calling the script.

- -b (--bib=file.bib) Set the input Bib File
- -a (--aux=file.aux) Set the input Aux File
- -o (--output=file.html) Write results to the HTML Output File.
- -v (--view) Open in Browser. Use together with -o.
- -N (--no-console) Do not print problems to console. An exit code is always returned.

## Help

See `./biblatex_check.py -h` for basic help.

If your getting an environment error, try using `python ./biblatex_check.py` or `python3 ./biblatex_check.py` depending on your OS.

## Why Pro? Changes on this fork

### 1. field_check.py

在实际的使用中，经常遇到的一个问题是，一种论文（比如article）的bib 条目中，所包含的域并不一致。比如article1包含了"题目","作者","期刊"和"年"；article2却包含了"题目","作者","年"和"页码"。blabla...这会导致我们在开始使用`biblatex_check.py`之前，进行配置的时候，无所适从。

我们需要一段代码（增加的`field_check.py`）来辅助我们得到所谓的list of 'certain required fields'.

In practice, one of the problems we often encounter is that the bib entries of a paper (e.g. article) do not contain the same fields. For example, article1 contains "title", "author", "journal" and "year", while article2 contains "title", "author", "year" and "page". blabla...
This will cause us to be at a loss when configuring `biblatex_check.py` before using it.

**We need a piece of code, i.e. `field_check.py`, to help us get the so-called list of 'certain required fields'.**

Then we can use biblatex_check.py to check if `certain required fields` are available.

#### usage:

`./field_check.py -b tests/input.bib`

### 2. field_filter.py

我们利用`field_check.py`检查所有的bib条目后，发现每个条目下的field并不一致。比如，有的多了address field，有的少了publisher field。
`field_filter.py` 就是帮助我们仅仅按照需要来保留field. 去掉那些不需要的field.
**使用`field_filter.py` 之前，需要进入代码内部进行配置，配置 line40 及以后的代码，以按照需要来保留field.**

After checking all the bib entries with `field_check.py` and `biblatex_check.py`, we found that the fields under each bib item are not consistent. For example, some have `address` field while some have no `publisher` field. 

`field_filter.py` helps to keep those fields only as configured. And remove the fields that are not needed. 

Before using `field_filter.py`, you need to go inside the code and configure line43 and later few lines.

#### usage:

`./field_filter.py -b tests/input_real.bib -o output/bib_fieldFilter_output.bib`

---



## Alternatives

BibLatex check is adapted from [BibTex Check](https://code.google.com/p/bibtex-check/) by Fabian Beck, which can be used to validate BibTex files.

See [BibTex vs BibLaTex vs NatBib](http://tex.stackexchange.com/questions/25701/bibtex-vs-biber-and-biblatex-vs-natbib) for a comparison of different referencing packages.

## Screenshot

![Screenshots of the BibLatex check screen](/../screenshots/screenshots/checkscreen.png?raw=true "BibLatex Check")

## Development

The checker is a single python script that takes .bib files as input and prints to console and/or an html file.

It maintains compatibility with Python 2, so any changes should be run against both Python 2.7 and 3.

Any bug fixes should be paired with a new test case in `tests/input.bib`

### "Running" the tests

```bash
python3 ./biblatex_check.py -b tests/input.bib
python2 ./biblatex_check.py -b tests/input.bib
```

Then _manually_ confirm the number of errors matches the details top of `tests/input.bib`


## License

MIT license
