#!/bin/bash
rm -rf package
mkdir package
pip install --target ./package -r requirements.txt --platform manylinux2014_x86_64 --only-binary=:all:
cp lambda_function.py package/
cd package
zip -r ../lambda_function.zip .
cd ..