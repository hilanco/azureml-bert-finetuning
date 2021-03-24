FROM python:3.8-slim

COPY . /app
WORKDIR /app


RUN pip install -U pip
RUN pip install flask pillow 
RUN pip install flask-cors nltk
RUN pip install torch
RUN pip install transformers


# By default, we run manual image resizing to maintain parity with CVS webservice prediction results.
# If parity is not required, you can enable faster image resizing by uncommenting the following lines.
# RUN apt-get update && apt-get install -y --no-install-recommends libglib2.0-bin
# RUN pip install opencv-python-headless

# Expose the port
EXPOSE 80


# Run the flask server for the endpoints
CMD python -u app.py
