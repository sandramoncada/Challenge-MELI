FROM public.ecr.aws/lambda/python:3.8
LABEL mainteiner="Sandra Milena Restrepo Moncada <sandramoncada@hotmail.com>" \
      Description="lambda image" Vendor="Sandra Milena Restrepo Moncada" Version="1"
ENV TZ=America/Bogota
RUN pip3 install pymongo pymongo[srv] requests PyJWT PyJWT[crypto]
COPY main.py ${LAMBDA_TASK_ROOT}
CMD ["main.handler"]
