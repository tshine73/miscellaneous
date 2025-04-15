# tshine73's utils

browse my [blog post](https://tshine73.blog/programmer/%e5%a6%82%e4%bd%95%e5%bb%ba%e7%ab%8b-python-%e5%8c%85%e7%84%b6%e5%be%8c%e4%b8%8a%e5%82%b3%e5%88%b0-server-%e8%ae%93%e4%bd%a0%e9%81%94%e6%88%90-dry-%e5%8e%9f%e5%89%87/) for further description

### prepare python package 

1. install twine

```bash
pip install twine==6.1.0
```

2. package

```bash
python setup.py sdist
```

### upload package to repo

#### public repo
```bash
twine upload dist/*
```

#### private repo
```bash
twine upload dist/* --repository-url http://localhost:8080
```
