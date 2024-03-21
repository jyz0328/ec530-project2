march 20th update:<br>
  #python3 ./nowwithlogin.py(backend)<br>
  then open another terminal, print:#python3 ./nowclient.py(frontend)<br><br>
  what i done<br>
  design api and rest api<br>
  relieaze a docuent analyzer with login upload and analyze<br><br>
  what i must finish later<br>
  database set (have not understand)<br>
  separate the backend, currently it is a whole backend, not a seperate backend<br><br>
  what i may finish later if have time<br>
  text analyzer is too simple, try to also import openai<br>
  it seems only analyze txt, only make it successful in analyze pdf at least. if have time can consider csv<br>





MyProject/<br>
│<br>
├── app/<br>
│   ├── __init__.py<br>
│   ├── routes.py<br>
│   └── utils/<br>
│       └── nlp.py<br>
│<br>
├── uploads/sample documents for run this app, but you can diy these documents<br>
│<br>
├── templates/<br>
│   └── upload.html<br>
│   └─── analyze.html<br>
└── run.py <br>

may add later:
log in function
database (must)
api&rest api realization (must)
