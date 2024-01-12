from django.shortcuts import render, redirect
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from django.views.decorators.csrf import csrf_exempt

def upload_file(request):
    if request.method == 'POST':
        # If a form is submitted
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form is valid
            uploaded_file = form.save()  # Save the uploaded file
            file_name = uploaded_file.file.name  # Get the name of the uploaded file
            extracted_text = check_file(file_name)  # Use a function to extract text from the file

            if extracted_text:
                # If text is extracted, show it on a page
                return render(request, 'file_upload.html', {'extracted_text': extracted_text})
            else:
                # If no text is found, show a message
                return HttpResponse("The uploaded file does not contain any text.")
    else:
        # If it's not a form submission, show an empty form
        form = FileUploadForm()

    # Render the HTML template with the form
    return render(request, 'file_upload.html', {'form': form})


def handle_uploaded_file(f):  
  file_name = f.name
  with open('myapp/static/media/'+file_name, 'wb+') as destination:  
      for chunk in f.chunks():  
          destination.write(chunk)
  return file_name

def extract_text_from_image(image):
  text = pytesseract.image_to_string(image, lang ='eng')
  return text



def extract_text_from_pdf(pdf):
  pages = convert_from_path(pdf,last_page=5)
  text =''
  for page in pages:
    text += str(extract_text_from_image(page))
  
  return text

def check_file(file_name):
  format = file_name.split('.',-1)[-1]
  file_path = os.path.join('myapp/static/media',file_name)
  extracted_text = None
  if format == 'jpg' or format == 'png' or format == 'jpeg':
    image = Image.open(file_path)
    extracted_text = extract_text_from_image(image)
  elif format == 'pdf':
    extracted_text = extract_text_from_pdf(file_path)
  return extracted_text

def upload_file(request):
    if request.method == 'POST':
        # If a form is submitted
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form is valid
            uploaded_file = form.save()  # Save the uploaded file
            file_name = uploaded_file.file.name  # Get the name of the uploaded file
            extracted_text = check_file(file_name)  # Use a function to extract text from the file

            if extracted_text:
                # If text is extracted, show it on a page
                return render(request, 'file_upload.html', {'extracted_text': extracted_text})
            else:
                # If no text is found, show a message
                return HttpResponse("The uploaded file does not contain any text.")
  
@csrf_exempt
def upload_file(request):
  text = None
  if request.method == 'POST':
    file_name = handle_uploaded_file(request.FILES['upload_file'])
    text=  check_file(file_name)
    if not text:
      extracted_text= "No text available to extract"
    else:
      extracted_text = "The extracted text is: " + text
    return render (request,'file_upload.html',{'text': extracted_text} )
  return render (request,'file_upload.html' )


