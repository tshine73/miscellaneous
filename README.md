# blog monitor deployment

```bash
rm deployment_blog_package.zip
mkdir blog_package
pip install -r ../blog/requirements.txt --target ./blog_package --platform manylinux2014_x86_64 --only-binary=:all:
cp -r ../blog/blog_monitor.py ./blog_package
cd blog_package
zip -r ../deployment_blog_package.zip .
cd ..
rm -rf blog_package
```