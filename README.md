# frenchtext
> NLP library to process french text.


In this early pre-version, the library provides :
- datasets to train business-oriented french text models
- a characters normalization pipeline tailored for french text

## Install

`pip install frenchtext`

## Dependencies

- [pandas](https://pandas.pydata.org/)
- [pyarrow](https://arrow.apache.org/docs/python/)
- [requests](https://requests.readthedocs.io/en/latest/)
- [fastprogress](https://github.com/fastai/fastprogress)

## Licence

APACHE licence 2.0 : https://www.apache.org/licenses/LICENSE-2.0

## How to use

The detailed documentation for each module is available through the menu on the left side of this page.

You will find below an overview of the library.

## French datasets

### Data sources

The text content of the main french websites in the domain of finance and business (+ wikipedia) was extracted in september 2019 using [nlptextdoc](https://github.com/laurentprudhon/nlptextdoc).

This extraction was done as "politely" as possible:
- extract only freely and publicly available content
- respect the robots.txt directives of each website (pages forbidden for indexing, maximum extraction rate)
- detect when websites use tools to prevent indexing (like Datadome) and abort the crawl

**IMPORTANT: The original authors of the websites own the copyright on all text blocks in this dataset.**

To be able to link each text block to its original author, we track the origin URL of each text block throughout the whole process.

**YOU CAN'T REUSE THE TEXT BLOCKS FOR ANY PURPOSE EXCEPT TRAINING A NATURAL LANGUAGE PROCESSING MODEL.**

See the new European copyright rules : [European Parliament approves new copyright rules for the internet](https://www.europarl.europa.eu/news/en/headlines/priorities/copyright/20190321IPR32110/european-parliament-approves-new-copyright-rules-for-the-internet)

"*The directive aims to make it easier for copyrighted material to be used freely through text and data mining, thereby removing a significant competitive disadvantage that European researchers currently face.*"

=> 131 websites and 2 564 755 HTML pages

### Data preparation

The text blocks were then:
- deduplicated to keep only distinct text blocks for each website (forgetting part of the original document structure), 
- tagged (but not filtered) by language (using https://fasttext.cc/docs/en/language-identification.html),
- grouped in categories according to the main theme of the original website,
- split in [Pandas](https://pandas.pydata.org/) dataframes of size < 2 GB.

=> 10 categories: 'Assurance', 'Banque', 'Bourse', 'Comparateur', 'Crédit', 'Forum', 'Institution', 'Presse', 'SiteInfo', 'Wikipedia'

In each dataframe, the text blocks were additionnaly **SHUFFLED IN A RANDOM ORDER** to make it very difficult to reconstruct the original articles (safety measure to help protect the copyrights of the authors).

The results of this second step can be downloaded in the *config.datasets* directory, as dataframes serialized in the [feather format](https://arrow.apache.org/docs/python/ipc.html?highlight=feather#feather-format), in files named according to the 'DatasetFile' column of the datasets table.

=> 19 dataset files: 'assurance', 'banque', 'bourse', 'comparateur', 'crédit', 'forum', 'institution', 'presse-1', 'presse-2', 'presse-3', 'presse-4', 'presse-5', 'presse-6', 'siteinfo', 'wikipedia-1', 'wikipedia-2', 'wikipedia-3', 'wikipedia-4', 'wikipedia-5'

### Dataset size

The number of words in each text block was computed using the default french tokenizer from [spaCy](https://spacy.io/) v2.1.

This business-oriented dataset contains **2 billion french words**.

Here is a summary of the number of words contributed by each category **in millions**:

- Assurance : 12
- Banque : 20
- Bourse : 26
- Comparateur :	20
- Crédit : 1
- Forum : 152
- Institution : 4
- Presse : 963
- SiteInfo : 78
- Wikipedia : 727

### Dataset files

```python
from frenchtext.core import *
from frenchtext.datasets import *
```

List available dataset files :

```python
datasetfiles = list_dataset_files()
datasetfiles
```




    ['assurance',
     'banque',
     'bourse',
     'comparateur',
     'crédit',
     'forum',
     'institution',
     'presse-1',
     'presse-2',
     'presse-3',
     'presse-4',
     'presse-5',
     'presse-6',
     'siteinfo',
     'wikipedia-1',
     'wikipedia-2',
     'wikipedia-3',
     'wikipedia-4',
     'wikipedia-5']



Source websites and number of words in each dataset file :

```python
datasetsdf = list_datasets()
datasetsdf[["DatasetFile","Url","Pages","Words"]].iloc[80:100]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DatasetFile</th>
      <th>Url</th>
      <th>Pages</th>
      <th>Words</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>80</th>
      <td>comparateur</td>
      <td>https://www.panorabanques.com/</td>
      <td>4341</td>
      <td>2584038</td>
    </tr>
    <tr>
      <th>81</th>
      <td>crédit</td>
      <td>https://www.cetelem.fr/</td>
      <td>274</td>
      <td>157191</td>
    </tr>
    <tr>
      <th>82</th>
      <td>crédit</td>
      <td>https://www.cofidis.fr/</td>
      <td>347</td>
      <td>243904</td>
    </tr>
    <tr>
      <th>83</th>
      <td>crédit</td>
      <td>https://www.cofinoga.fr/</td>
      <td>413</td>
      <td>86796</td>
    </tr>
    <tr>
      <th>84</th>
      <td>crédit</td>
      <td>https://www.sofinco.fr/</td>
      <td>916</td>
      <td>597221</td>
    </tr>
    <tr>
      <th>85</th>
      <td>crédit</td>
      <td>https://www.younited-credit.com/</td>
      <td>1341</td>
      <td>665115</td>
    </tr>
    <tr>
      <th>86</th>
      <td>forum</td>
      <td>https://droit-finances.commentcamarche.com/</td>
      <td>96450</td>
      <td>56120562</td>
    </tr>
    <tr>
      <th>87</th>
      <td>forum</td>
      <td>http://forum.doctissimo.fr/famille/argent-budg...</td>
      <td>26981</td>
      <td>61020453</td>
    </tr>
    <tr>
      <th>88</th>
      <td>forum</td>
      <td>http://forum.doctissimo.fr/viepratique/finance...</td>
      <td>5745</td>
      <td>4962230</td>
    </tr>
    <tr>
      <th>89</th>
      <td>forum</td>
      <td>http://forum.doctissimo.fr/viepratique/Impots/...</td>
      <td>2338</td>
      <td>1422143</td>
    </tr>
    <tr>
      <th>90</th>
      <td>forum</td>
      <td>https://forum.lesarnaques.com/assurance-automo...</td>
      <td>3530</td>
      <td>3085101</td>
    </tr>
    <tr>
      <th>91</th>
      <td>forum</td>
      <td>https://forum.lesarnaques.com/banque/</td>
      <td>6206</td>
      <td>5766116</td>
    </tr>
    <tr>
      <th>92</th>
      <td>forum</td>
      <td>https://www.60millions-mag.com/forum/</td>
      <td>3692</td>
      <td>2222882</td>
    </tr>
    <tr>
      <th>93</th>
      <td>forum</td>
      <td>https://www.boursorama.com/patrimoine/forum/</td>
      <td>13020</td>
      <td>10497065</td>
    </tr>
    <tr>
      <th>94</th>
      <td>forum</td>
      <td>https://www.cbanque.com/forums/</td>
      <td>12098</td>
      <td>7702002</td>
    </tr>
    <tr>
      <th>95</th>
      <td>institution</td>
      <td>https://acpr.banque-france.fr/</td>
      <td>470</td>
      <td>51397</td>
    </tr>
    <tr>
      <th>96</th>
      <td>institution</td>
      <td>https://www.banque-france.fr/</td>
      <td>728</td>
      <td>75101</td>
    </tr>
    <tr>
      <th>97</th>
      <td>institution</td>
      <td>https://www.ffa-assurance.fr/</td>
      <td>301</td>
      <td>146499</td>
    </tr>
    <tr>
      <th>98</th>
      <td>institution</td>
      <td>https://www.economie.gouv.fr/</td>
      <td>2720</td>
      <td>159663</td>
    </tr>
    <tr>
      <th>99</th>
      <td>institution</td>
      <td>https://www.impots.gouv.fr/portail/</td>
      <td>1631</td>
      <td>653735</td>
    </tr>
  </tbody>
</table>
</div>



### Download dataset files

```python
download_dataset_file("assurance")
```

    Downloading dataset file : assurance (17 MB)


```python
download_all_datasets()
```

    Downloading dataset file : assurance (17 MB)
    Downloading dataset file : banque (28 MB)
    Downloading dataset file : bourse (38 MB)
    Downloading dataset file : comparateur (28 MB)
    Downloading dataset file : crédit (2 MB)
    Downloading dataset file : forum (220 MB)
    Downloading dataset file : institution (5 MB)
    Downloading dataset file : presse-1 (218 MB)
    Downloading dataset file : presse-2 (196 MB)
    Downloading dataset file : presse-3 (190 MB)
    Downloading dataset file : presse-4 (234 MB)
    Downloading dataset file : presse-5 (269 MB)
    Downloading dataset file : presse-6 (334 MB)
    Downloading dataset file : siteinfo (116 MB)
    Downloading dataset file : wikipedia-1 (131 MB)
    Downloading dataset file : wikipedia-2 (182 MB)
    Downloading dataset file : wikipedia-3 (263 MB)
    Downloading dataset file : wikipedia-4 (269 MB)
    Downloading dataset file : wikipedia-5 (267 MB)


You can change the local directory where the dataset files are downloaded :

```python
config.datasets
```




    PosixPath('/home/laurent/.frenchtext/datasets')



```python
config["datasets_path"] = "/tmp/datasets"
config.datasets.mkdir(parents=True, exist_ok=True)
```

```python
config.datasets
```




    PosixPath('/tmp/datasets')



### Read dataset files

```python
datasetdf = read_dataset_file("assurance")
datasetdf
```

    Loaded dataframe for dataset assurance : 563613 text blocks





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Website</th>
      <th>DocId</th>
      <th>DocEltType</th>
      <th>DocEltCmd</th>
      <th>NestingLevel</th>
      <th>Text</th>
      <th>Lang</th>
      <th>Words</th>
      <th>Unique</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>11</td>
      <td>22332</td>
      <td>ListItem</td>
      <td>Text</td>
      <td>2</td>
      <td>5 tournages catastrophe pour un assureur</td>
      <td>fr</td>
      <td>6</td>
      <td>True</td>
    </tr>
    <tr>
      <th>1</th>
      <td>74</td>
      <td>710</td>
      <td>Section</td>
      <td>Start</td>
      <td>1</td>
      <td>Tout connaitre sur la nouvelle formation post-...</td>
      <td>fr</td>
      <td>7</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2</th>
      <td>11</td>
      <td>12082</td>
      <td>TextBlock</td>
      <td>Text</td>
      <td>1</td>
      <td>Votre Agent Mandataire AXA - Civry Marie Claud...</td>
      <td>?</td>
      <td>18</td>
      <td>True</td>
    </tr>
    <tr>
      <th>3</th>
      <td>87</td>
      <td>461</td>
      <td>TextBlock</td>
      <td>Text</td>
      <td>4</td>
      <td>60 ans et 4 mois</td>
      <td>fr</td>
      <td>5</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7</td>
      <td>200</td>
      <td>TextBlock</td>
      <td>Text</td>
      <td>1</td>
      <td>Mon devis sur mesure</td>
      <td>fr</td>
      <td>4</td>
      <td>True</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>563608</th>
      <td>138</td>
      <td>255</td>
      <td>Section</td>
      <td>Start</td>
      <td>2</td>
      <td>Les autres pouvoirs de police</td>
      <td>fr</td>
      <td>5</td>
      <td>True</td>
    </tr>
    <tr>
      <th>563609</th>
      <td>11</td>
      <td>19483</td>
      <td>TextBlock</td>
      <td>Text</td>
      <td>1</td>
      <td>Yves Nicolau assurance Laon</td>
      <td>?</td>
      <td>4</td>
      <td>True</td>
    </tr>
    <tr>
      <th>563610</th>
      <td>106</td>
      <td>1644</td>
      <td>ListItem</td>
      <td>Text</td>
      <td>3</td>
      <td>Evènements sportifs</td>
      <td>fr</td>
      <td>2</td>
      <td>True</td>
    </tr>
    <tr>
      <th>563611</th>
      <td>58</td>
      <td>4155</td>
      <td>Section</td>
      <td>Start</td>
      <td>1</td>
      <td>Agence Groupama Chalon</td>
      <td>?</td>
      <td>3</td>
      <td>True</td>
    </tr>
    <tr>
      <th>563612</th>
      <td>10</td>
      <td>150</td>
      <td>TextBlock</td>
      <td>Text</td>
      <td>2</td>
      <td>Nos agences d'assurance Aviva à OYONNAX sont h...</td>
      <td>fr</td>
      <td>26</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
<p>563613 rows × 9 columns</p>
</div>



### Access text blocks in dataset files

Filter and iterate over the rows of a dataset file :

```python
rowsiterator = get_rows_from_datasetdf(datasetdf, minwords=None, maxwords=5, lang="?")
show_first_rows(rowsiterator,10)
```

    12 - COORDONNEES
    41 - 01 30 41 67 33
    49 - Dmitriy G.
    57 - Les atouts du Multisupport CONFIANCE
    74 - 01XXL meribel hiver
    76 - Garantie en cas de vol
    87 - Par AXA, le 01/08/2016
    96 - mgr@enderby.eu
    127 - 18 place De Strasbourg
    131 - Saint Gaudens


Filter and iterate over the text blocks of a full dataset (across multiple files) :

```python
textiterator = get_textblocks_from_dataset("Assurance", minwords=None, maxwords=10, lang="fr")
show_first_textblocks(textiterator,skip=2000,count=10)
```

    Loaded dataframe for dataset assurance : 563613 text blocks
    2001 - Rééquipement à neuf à vie
    2002 - Définition Conducteur secondaire- Lexique
    2003 - Comment éviter les fraudes
    2004 - Comment demander un remboursement santé - GENERALI
    2005 - Simulateur pour connaître les obligations de votre accord de branche
    2006 - Complémentaire Epargne retraite des indépendants et TNS - Malakoff Médéric
    2007 - Experts-Comptables, découvrez la mission épargne salariale
    2008 - Vous n’êtes pas encore client :
    2009 - Actualités (Page 6) | ameli.fr | Pharmacien
    2010 - Dépression : quelle prise en charge ? - Matmut


Access a specific row :

```python
get_text_from_rowindex(datasetdf,100)
```




    'Les inondations de plaine : débordement de cours d’eau avec une durée d’immersion longue (prévisibles plusieurs jours ou heures à l’avance).'



Find text blocks with a specific char or substring :

```python
find_textblocks_with_chars(datasetdf,"rétroviseur",count=20,ctxsize=15)
```




    350594     ore dans notre rétroviseur gauche lorsque 
    149029     de glace ? Les rétroviseurs ainsi que les 
    51349      ace. Quant aux rétroviseurs, ils le sont d
    310354     vant, arrière, rétroviseurs et vitres laté
    489866    \naussi dans le rétroviseur pour ne pas se 
    364550     ôté ou sous le rétroviseur intérieur de vo
    560539     tionnement des rétroviseurs.              
    560700     é (pare-brise, rétroviseurs…),            
    223621     riorations des rétroviseurs et des phares.
    543903     es miroirs des rétroviseurs lorsqu’ils peu
    502075      logo dans son rétroviseur et par un signa
    53237      vous cassez le rétroviseur d’une voiture. 
    310456      éraflures, un rétroviseur abîmé, ou un au
    375158     ant, moteur de rétroviseurs…              
    539914     nt et arrière, rétroviseurs intérieurs et 
    171367     t utilisez vos rétroviseurs               
    485058      ainsi que les rétroviseurs ne sont pas ga
    277390     ant, moteur de rétroviseurs...            
    20222      sont offerts : rétroviseurs électriques, c
    317634     res, y compris rétroviseurs et feux       
    Name: Text, dtype: object



```python
find_textblocks_with_chars(datasetdf,64257,count=10,wrap=True)
```




    175413    x besoins de diversi[ﬁ]cation des placements
    337398    e 30 villes ont béné[ﬁ]cié de ces animations
    265114    nt règlementaire et [ﬁ]nancier, nous accompa
    74267          La Fondation a [ﬁ]nancé depuis 2009, l’
    424584    tion de l’équilibre [ﬁ]nancier des régimes d
    219195    d, Jérôme Powell con[ﬁ]rmera que, dans l’att
    489511    s besoins de diversi[ﬁ]cation de la clientèl
    517563    si en présence d’un [ﬁ]nancement par crédit,
    479694    nt règlementaire et [ﬁ]nancier, La Mondiale 
    252202    n de disponibilités [ﬁ]nancières mais aussi,
    Name: Text, dtype: object



### Track the source URL for each text block 

Optionally download and read urls file to track the origin of each text block :

```python
urlsdf = read_urls_file()
urlsdf.head()
```

    Loaded datasets urls : 2668787 urls





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Website</th>
      <th>DocId</th>
      <th>DocUrl</th>
      <th>Words</th>
      <th>fr</th>
      <th>en</th>
      <th>de</th>
      <th>es</th>
      <th>?</th>
      <th>%fr</th>
      <th>%en</th>
      <th>%de</th>
      <th>%es</th>
      <th>%?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4</td>
      <td>1</td>
      <td>https://www.afer.fr/</td>
      <td>573.0</td>
      <td>524.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>46.0</td>
      <td>0.914485</td>
      <td>0.005236</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.080279</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>2</td>
      <td>https://www.afer.fr/afer/adhesion/</td>
      <td>74.0</td>
      <td>74.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4</td>
      <td>3</td>
      <td>https://www.afer.fr/afer/adhesion/adherent-ass...</td>
      <td>475.0</td>
      <td>457.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>13.0</td>
      <td>0.962105</td>
      <td>0.010526</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.027368</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>4</td>
      <td>https://www.afer.fr/afer/adhesion/adherer-assu...</td>
      <td>519.0</td>
      <td>519.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>5</td>
      <td>https://www.afer.fr/afer/adhesion/parrainage-a...</td>
      <td>355.0</td>
      <td>345.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>10.0</td>
      <td>0.971831</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.028169</td>
    </tr>
  </tbody>
</table>
</div>



```python
get_text_from_rowindex(datasetdf,100)
```




    'Les inondations de plaine : débordement de cours d’eau avec une durée d’immersion longue (prévisibles plusieurs jours ou heures à l’avance).'



```python
get_url_from_rowindex(datasetdf, 100)
```




    'https://www.maif.fr/conseils-prevention/risques-majeurs/inondation.html'



## Characters normalization pipeline

### Motivation

French datasets often contain several thousands distinct Unicode characters.

Characters stats in Wikipedia dataset :
- 35.6 billion chars
- 13 502 distinct Unicode chars

Characters stats in Business dataset :
- 27.5 billion chars
- 3 763 distinct Unicode chars

We need to reduce the number of distinct characters fed to our natural language processing applications, for three reasons :
- chars considered by the user as visually equivalent will often produce a different application behavior : this is a huge problem for the user experience
- with so many chars, the designer of the NLP application will not be able to reason about all possible combinations : this could harm the explainability of the system
- this huge number of distinct characters brings a significant amount complexity the NLP models will have to deal with

Characters stats in Wikipedia dataset :
- Only 1316 chars more frequent than 1 in 100 million
- 99.9987 % of Wikipedia chars would be preserved if we only kept the frequent chars

Characters stats in Business dataset :
- Only 531 chars more frequent than 1 in 100 million
- 99.9996 % of Business chars would be preserved if we only kept the frequent chars

We can be smarter than that and replace rare chars with equivalent (or mostly equivalent) more frequent chars to preserve a maximum of information.

### Target characters set

After a detailed study of all the frequent chars, the goal is to design a noramization pipeline which can retain as much information as possible while greatly reducing the number of dinstinct chars.

We saw before that it is possible to preserve 99.9996% of the original chars while keeping only 500 distinct chars. By being clever and replacing equivalent chars, we can divide this number by 2 and still retain the same amount of information.

It may then be useful to limit the number of distinct characters after normalization to **255 distinct characters** : 
- if needed, french text chars can then be encoded with a single byte
- the list of supported chars can be memorized by NLP application developers and users

```python
from frenchtext.core import *
from frenchtext.chars import *
```

255 supported characters after normalization : 

```python
import pandas as pd
dfcharsnorm = pd.read_csv(chardatadir / "charset-fr.csv", sep=";")
dfcharsnorm
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>FrCode</th>
      <th>Category</th>
      <th>SubCategory</th>
      <th>Code</th>
      <th>Char</th>
      <th>CharName</th>
      <th>CountBusiness</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>separator</td>
      <td>control</td>
      <td>0</td>
      <td>NaN</td>
      <td>Reserved - End of string</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>separator</td>
      <td>space</td>
      <td>32</td>
      <td></td>
      <td>Space</td>
      <td>88494564</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>separator</td>
      <td>space</td>
      <td>10</td>
      <td>\n</td>
      <td>Char 10</td>
      <td>9588147</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>separator</td>
      <td>space</td>
      <td>9</td>
      <td>\t</td>
      <td>Char 9</td>
      <td>1522053</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>separator</td>
      <td>punctuation</td>
      <td>44</td>
      <td>,</td>
      <td>Comma</td>
      <td>286106887</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>251</th>
      <td>251</td>
      <td>emoticon</td>
      <td>object</td>
      <td>9792</td>
      <td>♀</td>
      <td>Female Sign</td>
      <td>515</td>
    </tr>
    <tr>
      <th>252</th>
      <td>252</td>
      <td>emoticon</td>
      <td>object</td>
      <td>127881</td>
      <td>🎉</td>
      <td>Party Popper</td>
      <td>356</td>
    </tr>
    <tr>
      <th>253</th>
      <td>253</td>
      <td>emoticon</td>
      <td>object</td>
      <td>9997</td>
      <td>✍</td>
      <td>Writing Hand</td>
      <td>157</td>
    </tr>
    <tr>
      <th>254</th>
      <td>254</td>
      <td>emoticon</td>
      <td>object</td>
      <td>9993</td>
      <td>✉</td>
      <td>Envelope</td>
      <td>55</td>
    </tr>
    <tr>
      <th>255</th>
      <td>255</td>
      <td>emoticon</td>
      <td>object</td>
      <td>10013</td>
      <td>✝</td>
      <td>Latin Cross</td>
      <td>22</td>
    </tr>
  </tbody>
</table>
<p>256 rows × 7 columns</p>
</div>



The table below shows the number of chars in each category (after normalization) **per 100 million characters** :

```python
dfblocks = dfcharsnorm.groupby(by=["Category","SubCategory"]).agg({"Char":["count","sum"],"CountBusiness":"sum"})
dfblocks["CountBusiness"] = (dfblocks["CountBusiness"] / 27577304956 * 100000000).astype(int)
dfblocks
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th colspan="2" halign="left">Char</th>
      <th>CountBusiness</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>count</th>
      <th>sum</th>
      <th>sum</th>
    </tr>
    <tr>
      <th>Category</th>
      <th>SubCategory</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">emoticon</th>
      <th>hand</th>
      <td>12</td>
      <td>💪👉👍👏🙏🙌👇👊👎👌✌✊</td>
      <td>42</td>
    </tr>
    <tr>
      <th>head</th>
      <td>28</td>
      <td>🙂😉😀😂😁😊🙁😅😍😃😡🤣😄🤔😎😭👹😱😜😋🤩🙄😆😛🤪😢😇🤦</td>
      <td>233</td>
    </tr>
    <tr>
      <th>object</th>
      <td>16</td>
      <td>⚠🔴🔥🏆⚽💡🚨💥⚡♫♂♀🎉✍✉✝</td>
      <td>60</td>
    </tr>
    <tr>
      <th rowspan="6" valign="top">letter</th>
      <th>digit</th>
      <td>10</td>
      <td>0123549876</td>
      <td>3271115</td>
    </tr>
    <tr>
      <th>encoding</th>
      <td>3</td>
      <td>Ã�￼</td>
      <td>249</td>
    </tr>
    <tr>
      <th>greek</th>
      <td>2</td>
      <td>λπ</td>
      <td>2</td>
    </tr>
    <tr>
      <th>latin-fr</th>
      <td>84</td>
      <td>abcdefghijklmnopqrstuvwxyzàâäçèéêëîïôöùûüÿABCD...</td>
      <td>91437146</td>
    </tr>
    <tr>
      <th>latin-other</th>
      <td>25</td>
      <td>áãåćčėğıíìńñóòõøšşßúÁÅŠÚŽ</td>
      <td>712</td>
    </tr>
    <tr>
      <th>other</th>
      <td>5</td>
      <td>_&amp;@\#</td>
      <td>40814</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">separator</th>
      <th>control</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>punctuation</th>
      <td>23</td>
      <td>,'.-:/")(?!»«|…;[]}{•¿¡</td>
      <td>4684722</td>
    </tr>
    <tr>
      <th>space</th>
      <td>3</td>
      <td>\n\t</td>
      <td>361183</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">symbol</th>
      <th>currency</th>
      <td>6</td>
      <td>€$¤£¥¢</td>
      <td>21099</td>
    </tr>
    <tr>
      <th>math</th>
      <td>14</td>
      <td>=&gt;+&lt;^~×≤÷≥±≠∞√</td>
      <td>50056</td>
    </tr>
    <tr>
      <th>shape</th>
      <td>15</td>
      <td>*✓⇒♥¦→★¯↓❌❐†↑←↔</td>
      <td>7954</td>
    </tr>
    <tr>
      <th>sign</th>
      <td>3</td>
      <td>©®™</td>
      <td>1754</td>
    </tr>
    <tr>
      <th>unit</th>
      <td>6</td>
      <td>%°§µØ‰</td>
      <td>102213</td>
    </tr>
  </tbody>
</table>
</div>



### Normalization pipeline overview

The normalization pipeline applies the following **14 steps**, which are explained and illustrated in the sections below.

- Fix encoding errors
  - fix windows1252 text read as iso8859-1
  - fix utf8 text read as windows1252
  - fix windows1252 text read as utf8
  - merge Unicode combining chars
  - ignore control chars
- Remove display attributes
  - replace latin letter symbols
  - replace latin letter ligatures
  - replace latin number symbols
- Normalize visually equivalent chars
  - replace equivalent chars 
  - replace cyrillic and greek chars looking like latin letters
- Encode infrequent chars while losing a little bit of information 
  - replace infrequent latin letters with diacritics
  - replace infrequent chars from other scripts
  - replace infrequent symbols 
  - ignore remaining chars with no glyph 

The statistics below count the number of chars normalized **for 1 million chars** in 4 distinct parts of the french datasets : business websites, forums, news, wikipedia.

The first line of the table below shows that :
- in 1 million chars extracted from forum pages (raw users input), 41.8 chars will be encoding errors (windows1252 read as iso8859-1)
- in 1 million chars extracted from wikipedia (curated content), only 0.006 chars will be encoding errors

These numbers show that **characters normalization is much more important in real world applications** than in academic papers based on clean wikipedia text. 

```python
normstats = pd.read_csv(chardatadir / "stats" / "normalization.total.stats.csv")
normstats[["Transform","FreqBusiness","FreqForum","FreqPresse","FreqWikipedia"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Transform</th>
      <th>FreqBusiness</th>
      <th>FreqForum</th>
      <th>FreqPresse</th>
      <th>FreqWikipedia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Fix encoding errors : windows1252 read as iso8...</td>
      <td>0.510560</td>
      <td>41.818746</td>
      <td>0.813485</td>
      <td>0.006025</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Fix encoding errors : utf8 read as windows1252</td>
      <td>0.126815</td>
      <td>0.058024</td>
      <td>0.072456</td>
      <td>0.001037</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fix encoding errors :  windows1252 read as utf8</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.019315</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Merge Unicode combining chars</td>
      <td>2.811983</td>
      <td>0.432638</td>
      <td>0.568146</td>
      <td>0.000140</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ignore control chars</td>
      <td>6.450737</td>
      <td>349.052995</td>
      <td>6.454367</td>
      <td>4.118586</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Replace latin letter symbols</td>
      <td>0.019360</td>
      <td>0.039701</td>
      <td>0.297372</td>
      <td>0.150550</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Replace latin letter ligatures</td>
      <td>6.603815</td>
      <td>6.541480</td>
      <td>10.097290</td>
      <td>17.204422</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Replace latin number symbols</td>
      <td>2.528338</td>
      <td>4.162482</td>
      <td>2.560933</td>
      <td>0.429792</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Normalize equivalent chars</td>
      <td>814.327384</td>
      <td>1248.410777</td>
      <td>684.333730</td>
      <td>242.391239</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Replace cyrillic and greek chars looking like ...</td>
      <td>0.062432</td>
      <td>0.760424</td>
      <td>0.491996</td>
      <td>7.479907</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Replace infrequent chars : latin letters with ...</td>
      <td>0.063782</td>
      <td>0.078384</td>
      <td>0.099106</td>
      <td>9.124948</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Replace infrequent chars : other scripts</td>
      <td>0.085694</td>
      <td>0.468776</td>
      <td>1.192548</td>
      <td>16.612142</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Replace infrequent chars : symbols</td>
      <td>0.139271</td>
      <td>0.159821</td>
      <td>0.399064</td>
      <td>0.073566</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Replace infrequent chars : chars to ignore</td>
      <td>0.018910</td>
      <td>0.044282</td>
      <td>0.021320</td>
      <td>0.016423</td>
    </tr>
  </tbody>
</table>
</div>



Most frequent chars replaced from equivalent characters :

```python
replacestats = pd.read_csv(chardatadir / "stats" / "normalization.layer8.stats.csv")
replacestats[["Char","CharName","FreqBusiness","FreqForum","FreqPresse","FreqWikipedia"]].head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Char</th>
      <th>CharName</th>
      <th>FreqBusiness</th>
      <th>FreqForum</th>
      <th>FreqPresse</th>
      <th>FreqWikipedia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>'</td>
      <td>Apostrophe</td>
      <td>486.034805</td>
      <td>160.264219</td>
      <td>376.104982</td>
      <td>134.658673</td>
    </tr>
    <tr>
      <th>1</th>
      <td></td>
      <td>Space</td>
      <td>310.411117</td>
      <td>1082.845985</td>
      <td>288.635983</td>
      <td>87.877649</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-</td>
      <td>Hyphen-Minus</td>
      <td>14.431203</td>
      <td>2.903761</td>
      <td>12.828203</td>
      <td>16.223154</td>
    </tr>
    <tr>
      <th>3</th>
      <td>«</td>
      <td>Left-Pointing Double Angle Quotation Mark</td>
      <td>1.429478</td>
      <td>0.680513</td>
      <td>3.002426</td>
      <td>0.559632</td>
    </tr>
    <tr>
      <th>4</th>
      <td>»</td>
      <td>Right-Pointing Double Angle Quotation Mark</td>
      <td>1.323524</td>
      <td>0.533926</td>
      <td>2.461880</td>
      <td>0.544134</td>
    </tr>
    <tr>
      <th>5</th>
      <td>|</td>
      <td>Vertical Line</td>
      <td>0.003452</td>
      <td>0.001018</td>
      <td>0.005488</td>
      <td>0.875894</td>
    </tr>
    <tr>
      <th>6</th>
      <td>•</td>
      <td>Bullet</td>
      <td>0.204104</td>
      <td>0.243295</td>
      <td>0.189664</td>
      <td>0.543237</td>
    </tr>
    <tr>
      <th>7</th>
      <td>.</td>
      <td>Full Stop</td>
      <td>0.059280</td>
      <td>0.078893</td>
      <td>0.856230</td>
      <td>0.069278</td>
    </tr>
    <tr>
      <th>8</th>
      <td>"</td>
      <td>Quotation Mark</td>
      <td>0.085093</td>
      <td>0.023413</td>
      <td>0.011504</td>
      <td>0.292385</td>
    </tr>
    <tr>
      <th>9</th>
      <td>:</td>
      <td>Colon</td>
      <td>0.000150</td>
      <td>0.000509</td>
      <td>0.000053</td>
      <td>0.169047</td>
    </tr>
    <tr>
      <th>10</th>
      <td>°</td>
      <td>Degree Sign</td>
      <td>0.148726</td>
      <td>0.181199</td>
      <td>0.014618</td>
      <td>0.078302</td>
    </tr>
    <tr>
      <th>11</th>
      <td>é</td>
      <td>Latin Small Letter E With Acute</td>
      <td>0.001651</td>
      <td>0.006108</td>
      <td>0.003166</td>
      <td>0.101114</td>
    </tr>
    <tr>
      <th>12</th>
      <td>←</td>
      <td>Leftwards Arrow</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000158</td>
      <td>0.047194</td>
    </tr>
    <tr>
      <th>13</th>
      <td>=</td>
      <td>Equals Sign</td>
      <td>0.004802</td>
      <td>0.029012</td>
      <td>0.000686</td>
      <td>0.041589</td>
    </tr>
    <tr>
      <th>14</th>
      <td>→</td>
      <td>Rightwards Arrow</td>
      <td>0.026113</td>
      <td>0.002545</td>
      <td>0.034302</td>
      <td>0.015862</td>
    </tr>
    <tr>
      <th>15</th>
      <td>d</td>
      <td>Latin Small Letter D</td>
      <td>0.000000</td>
      <td>0.024940</td>
      <td>0.000000</td>
      <td>0.036405</td>
    </tr>
    <tr>
      <th>16</th>
      <td>&lt;</td>
      <td>Less-Than Sign</td>
      <td>0.004202</td>
      <td>0.142007</td>
      <td>0.001267</td>
      <td>0.024073</td>
    </tr>
    <tr>
      <th>17</th>
      <td>,</td>
      <td>Comma</td>
      <td>0.006453</td>
      <td>0.101288</td>
      <td>0.004538</td>
      <td>0.022756</td>
    </tr>
    <tr>
      <th>18</th>
      <td>↓</td>
      <td>Downwards Arrow</td>
      <td>0.007504</td>
      <td>0.001527</td>
      <td>0.011188</td>
      <td>0.021888</td>
    </tr>
    <tr>
      <th>19</th>
      <td>★</td>
      <td>Black Star</td>
      <td>0.001351</td>
      <td>0.013743</td>
      <td>0.022006</td>
      <td>0.011686</td>
    </tr>
  </tbody>
</table>
</div>



For example, list of all Unicode chars wich will be projected to a regular 'apostrophe' :

```python
replacechars = pd.read_csv(chardatadir / "normalizedchars.csv", sep=';')
replacechars[replacechars["NormChar"]=="'"][["Code","Char","CharName"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Code</th>
      <th>Char</th>
      <th>CharName</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>23</th>
      <td>96</td>
      <td>`</td>
      <td>Grave Accent</td>
    </tr>
    <tr>
      <th>24</th>
      <td>180</td>
      <td>´</td>
      <td>Acute Accent</td>
    </tr>
    <tr>
      <th>25</th>
      <td>697</td>
      <td>ʹ</td>
      <td>Modifier Letter Prime</td>
    </tr>
    <tr>
      <th>26</th>
      <td>699</td>
      <td>ʻ</td>
      <td>Modifier Letter Turned Comma</td>
    </tr>
    <tr>
      <th>27</th>
      <td>700</td>
      <td>ʼ</td>
      <td>Modifier Letter Apostrophe</td>
    </tr>
    <tr>
      <th>28</th>
      <td>702</td>
      <td>ʾ</td>
      <td>Modifier Letter Right Half Ring</td>
    </tr>
    <tr>
      <th>29</th>
      <td>703</td>
      <td>ʿ</td>
      <td>Modifier Letter Left Half Ring</td>
    </tr>
    <tr>
      <th>30</th>
      <td>712</td>
      <td>ˈ</td>
      <td>Modifier Letter Vertical Line</td>
    </tr>
    <tr>
      <th>31</th>
      <td>714</td>
      <td>ˊ</td>
      <td>Modifier Letter Acute Accent</td>
    </tr>
    <tr>
      <th>32</th>
      <td>715</td>
      <td>ˋ</td>
      <td>Modifier Letter Grave Accent</td>
    </tr>
    <tr>
      <th>33</th>
      <td>729</td>
      <td>˙</td>
      <td>Dot Above</td>
    </tr>
    <tr>
      <th>34</th>
      <td>8216</td>
      <td>‘</td>
      <td>Left Single Quotation Mark</td>
    </tr>
    <tr>
      <th>35</th>
      <td>8217</td>
      <td>’</td>
      <td>Right Single Quotation Mark</td>
    </tr>
    <tr>
      <th>36</th>
      <td>8219</td>
      <td>‛</td>
      <td>Single High-Reversed-9 Quotation Mark</td>
    </tr>
    <tr>
      <th>37</th>
      <td>8223</td>
      <td>‟</td>
      <td>Double High-Reversed-9 Quotation Mark</td>
    </tr>
    <tr>
      <th>38</th>
      <td>8242</td>
      <td>′</td>
      <td>Prime</td>
    </tr>
  </tbody>
</table>
</div>



Frequency of characters from other scripts (chinese, arabic, cyrillic ...) :

```python
scriptsstats = pd.read_csv(chardatadir / "stats" / "normalization.layer11.stats.csv")
scriptsstats[["CharFamily","FreqBusiness","FreqForum","FreqPresse","FreqWikipedia"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CharFamily</th>
      <th>FreqBusiness</th>
      <th>FreqForum</th>
      <th>FreqPresse</th>
      <th>FreqWikipedia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ChineseJapaneseKorean</td>
      <td>0.012456</td>
      <td>0.177127</td>
      <td>0.194677</td>
      <td>4.059173</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Arabic</td>
      <td>0.012306</td>
      <td>0.026467</td>
      <td>0.460280</td>
      <td>3.140120</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cyrillic</td>
      <td>0.024462</td>
      <td>0.166438</td>
      <td>0.237159</td>
      <td>3.118961</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Greek</td>
      <td>0.016058</td>
      <td>0.022904</td>
      <td>0.031347</td>
      <td>2.423996</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Hebrew</td>
      <td>0.000150</td>
      <td>0.000000</td>
      <td>0.184914</td>
      <td>1.132155</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Other</td>
      <td>0.000750</td>
      <td>0.029012</td>
      <td>0.004063</td>
      <td>0.800871</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Indian</td>
      <td>0.000750</td>
      <td>0.037665</td>
      <td>0.033458</td>
      <td>0.737955</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Phonetic</td>
      <td>0.002401</td>
      <td>0.001527</td>
      <td>0.001636</td>
      <td>0.298579</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Latin</td>
      <td>0.013507</td>
      <td>0.006108</td>
      <td>0.007283</td>
      <td>0.269377</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Math</td>
      <td>0.001801</td>
      <td>0.000509</td>
      <td>0.000528</td>
      <td>0.240707</td>
    </tr>
    <tr>
      <th>10</th>
      <td>LaoThai</td>
      <td>0.000000</td>
      <td>0.001018</td>
      <td>0.033194</td>
      <td>0.217867</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Armenian</td>
      <td>0.001051</td>
      <td>0.000000</td>
      <td>0.004011</td>
      <td>0.172382</td>
    </tr>
  </tbody>
</table>
</div>



### Normalization pipeline API

Initialize a text normalizer :

```python
%time norm = TextNormalizer()
norm
```

    CPU times: user 1.83 s, sys: 15.6 ms, total: 1.84 s
    Wall time: 2 s





    1 - Fix encoding errors : windows1252 read as iso8859-1
    2 - Fix encoding errors : utf8 read as windows1252
    3 - Fix encoding errors :  windows1252 read as utf8
    4 - Merge Unicode combining chars
    5 - Ignore control chars
    6 - Replace latin letter symbols
    7 - Replace latin letter ligatures
    8 - Replace latin number symbols
    9 - Normalize equivalent chars
    10 - Replace cyrillic and greek chars looking like latin letters
    11 - Replace infrequent chars : latin letters with diacritics
    12 - Replace infrequent chars : other scripts
    13 - Replace infrequent chars : symbols
    14 - Replace infrequent chars : chars to ignore



Normalize text :

```python
teststring = chr(127995)+"① l`"+chr(156)+"uv"+chr(127)+"re est¨ "+chr(147)+"belle"+chr(148)+"¸ Ã  Â½ â‚¬ énième â€° "+chr(133)+" ⁽🇪ﬃc🇦ce⁾ ！"
teststring
```




    '🏻① l`\x9cuv\x7fre est¨ \x93belle\x94¸ Ã  Â½ â‚¬ énième â€° \x85 ⁽🇪ﬃc🇦ce⁾ ！'



```python
result = norm(teststring)
result
```




    (1) l'oeuvre est «belle», Ã  1/2 € énième ‰ … (EfficAce) !



Describe the changes applied by the normalization pipeline :

```python
print(result.describeChanges())
```

    Fix encoding errors : windows1252 read as iso8859-1
     < 🏻① l` [] uvre est¨  [] belle [] ¸ Ã  Â½ â‚¬ énième â€°  []  ⁽🇪ﬃc🇦ce⁾ ！
     < 🏻① l` [œ] uvre est¨  [“] belle [”] ¸ Ã  Â½ â‚¬ énième â€°  […]  ⁽🇪ﬃc🇦ce⁾ ！
    Fix encoding errors : utf8 read as windows1252
     < 🏻① l`œuvre est¨ “belle”¸ Ã   [Â½]   [â‚¬]  énième  [â€°]  … ⁽🇪ﬃc🇦ce⁾ ！
     < 🏻① l`œuvre est¨ “belle”¸ Ã   [½_]   [€__]  énième  [‰__]  … ⁽🇪ﬃc🇦ce⁾ ！
    Merge Unicode combining chars
     < 🏻① l`œuvre est¨ “belle”¸ Ã  ½ €  [é] ni [è] me ‰ … ⁽🇪ﬃc🇦ce⁾ ！
     < 🏻① l`œuvre est¨ “belle”¸ Ã  ½ €  [é_] ni [è_] me ‰ … ⁽🇪ﬃc🇦ce⁾ ！
    Ignore control chars
     <  [🏻] ① l`œuv [] re est [¨]  “belle”¸ Ã  ½ € énième ‰ … ⁽🇪ﬃc🇦ce⁾ ！
     <  [_] ① l`œuv [_] re est [_]  “belle”¸ Ã  ½ € énième ‰ … ⁽🇪ﬃc🇦ce⁾ ！
    Replace latin letter symbols
     < ① l`œuvre est “belle”¸ Ã  ½ € énième ‰ … ⁽ [🇪] ﬃc [🇦] ce⁾ ！
     < ① l`œuvre est “belle”¸ Ã  ½ € énième ‰ … ⁽ [E] ﬃc [A] ce⁾ ！
    Replace latin letter ligatures
     < ① l` [œ ] uvre est “belle”¸ Ã  ½ € énième ‰ … ⁽E [ﬃ  ] cAce⁾ ！
     < ① l` [oe] uvre est “belle”¸ Ã  ½ € énième ‰ … ⁽E [ffi] cAce⁾ ！
    Replace latin number symbols
     <  [①  ]  l`oeuvre est “belle”¸ Ã   [½  ]  € énième ‰ … ⁽EfficAce⁾ ！
     <  [(1)]  l`oeuvre est “belle”¸ Ã   [1/2]  € énième ‰ … ⁽EfficAce⁾ ！
    Normalize equivalent chars
     < (1) l [`] oeuvre est  [“] belle [”]  [¸]  Ã  1/2 € énième ‰ …  [⁽] EfficAce [⁾]   [！] 
     < (1) l ['] oeuvre est  [«] belle [»]  [,]  Ã  1/2 € énième ‰ …  [(] EfficAce [)]   [!] 
    


Compute spans for equivalent substrings before and after normalization :

```python
result.output[0:12]
```




    "(1) l'oeuvre"



```python
result.input[result.mapOutputIndexToInput(0):result.mapOutputIndexToInput(12)]
```




    '🏻① l`\x9cuv\x7fre'



```python
result.output[3:10]
```




    " l'oeuv"



```python
result.input[result.mapOutputIndexToInput(3):result.mapOutputIndexToInput(10)]
```




    ' l`\x9cuv\x7f'



Performance test : **2500 sentences per second** => fast enough but will be optimized in a later version.

```python
%timeit -n100 norm(teststring)
```

    397 µs ± 89.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


### Appendix : Unicode utility functions

Unicode characters properties :

```python
charname("🙂")
```




    'Slightly Smiling Face'



```python
charcategory("🙂")
```




    'Symbol'



```python
charsubcategory("🙂")
```




    'Other'



```python
charblock("🙂")
```




    'Emoticons'



```python
blockfamily('Emoticons')
```




    'Symbols'


