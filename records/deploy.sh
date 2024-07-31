#!/bin/bash
rm -rf package
mkdir package
cd package
mkdir services
mkdir models
cd ..
pip install --target ./package -r requirements.txt --platform manylinux2014_x86_64 --only-binary=:all:
cp lambda_function.py package/
cp services/service.py package/services/
cp models/operation.py package/models/
cp models/record.py package/models/
cd package
zip -r ../lambda_function.zip .
cd ..