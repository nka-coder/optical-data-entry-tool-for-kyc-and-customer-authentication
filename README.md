# An optical data entry tool for KYC and customer authentication 

## Domain :
Finance and Insurance.

## Problem statement 
Verification of identity is a tedious and recurrenttask that employees of financial services companies have to perform on daily basis. Before providing a service to a customer, any financial service agent has to perform KYC procedure if it is a new customer or proceed to authentication if it is an already registered customer. For that sake, they have to manually enter on a software the information that are on the identity document provided by the client. The  tedious  and  boring  nature  of  this  task  always  results  in  poor  performance  of  those agents, thus leading to poor quality of data into customer databases of these companies. In  this  project,  I  created  an  App  that  leverages  Tesseract,  an  OCR  library,  to automatize extraction of information on identity documents. OCR (Optical Character Recognition) is a computer  vision  technique  used  in  data  science  to  convert  imagetextsinto  machine-encoded texts.

## Solution statement 
The  goal  is  to  create  an  identity  document  information  extractor  running  on  Android smartphones. The app must be able to detect if a document has a MRZ (Machine-readable-zone)and if  it  is  the  case, extract  identity  information  from  it. The tasks  involved are  the following:</br>
	- Create a dataset of images of different types of identity document.</br>
 	- Write an OCR model (code) that can extract identity information from an MRZ image with high accuracy.</br>
 	- Make an Android App that leverage the model above to extract identity information from an identity document.</br>
We expect  our code to  have  a  better  accuracy than [Passporteye](https://pypi.org/project/PassportEye/) text  extraction  function called **read_mrz()**.

## Dataset 
The dataset that I used can be found in this Github repo. This dataset is composed of two video of a Cameroonian passport that a recorded myself with an android smartphone and some video of identity documents that I downloaded from the [MIDV-500](ftp://smartengines.com/midv-500/dataset/) dataset.

## Benchmark model 
We benchmark our solution with **Passporteye read_mrz() function**.
According to its documentation, Passporteye precision  on identity information  extraction from MRZs is around 80%. However, while testing Passporteye on our dataset, I obtained a less good result, a precision of about 60%.

## Evaluation metrics 
Per-Character  Recognition  rate  (PCR) is a metric  which  is  commonly used  to  evaluate performance of OCR systems.</br>

***PCR = Number of correct characters / Adjusted dataset size***

I  used  this  metric  when  evaluating  the  model  because the  greater  the number  of correct characters the better the experience of the user; and the metric has to take into account any additional unexpected characters that might deteriorate the quality of the extracted text.</br>
	- A correct character is a character that is correctly extracted from the MRZ image and that occupy its right position.</br>
	- The  Adjusted  dataset  size is  the  length  (number  of  characters)  of  the  longest  text between the original MRZ text and the machine extracted text. The Adjustmentsof the size of the dataset size is justified by the fact that we must consider an additional empty  character  (“”)  for  each  unexpected  additional  character  generated  by  the machine to take into account their impact on the PCR measurement.

## Software requirements
To   implement   the   proposed   solution,   there   are   some   software   requirements. The requirements  listed  below  are those  that  I found  on documentations  of libraries and  tools that I used.</br>
	- Pyhton 3 or higher (Iused Python 3.8.5)</br>
	- OpenCV 3 or Higher (Iused OpenCV 3)</br>
	- Pytesseract (Iused Pytesseract 4.1.1)</br>
	- Passporteye (I used Passporteye 2.1.0)</br>
	- Uvicorn(I used Uvicorn 0.13.4)

## Deliverables
To make this work practical, I developed an android app that leverages the proposed OCR model and the check-digits verification to extract identity information from identity document. The app is not already perfect, but it is a good start for the development of a professional tool.

**Experiment source codes**</br>
The source code (**experiment.py**) of the experiment can be found on this Github repo.</br>
	1. Clone or download the Github repo of the source code into the server computer</br>
	2. Start your Anaconda orPython Terminal</br>
	3. Use cd command to navigate to the folder containing the file **experiment.py**</br>
	4. Set the  path  to the  image  folderand  the  validation  data  onthe  code  of  the **experiment.py** file at line 164 and 166 </br>
	5. Execute on the Terminal the command: **python experiment.py** </br>

**API source code**</br>
The source code (**api.py**) of the app can be found on this Github repo.</br>
To test the API, follow the step below:</br>
	1. Clone or download the Github repo of the source code into the server computer</br>
	2. Start your Anaconda or Python Terminal</br>
	3. Use cd commandto navigate to the folder containing the file **api.py**</br>
	4. Execute on the Terminal the command: **uvicorn api:app --host xxx.xxx.xxx.xxx** , where xxx.xxx.xxx.xxx represents the IP address of the computer hosting the API.</br>
	5. Open on you navigator the url: http://xxx.xxx.xxx.xxx:8000/docs</br>
	6. The Swagger interface below will appears and let you test the API.</br>

**App source code and executable file**</br>
The work  is  still  in  progress  to  finalize  the  Android  app  development. You  can  follow  the development of the Android app on this Github repo (the sourcecode of the app is in the folder named **idinfoextractor**).</br>
To test the Android app at its current status.</br>
	1. Clone or download the Github repo of the source code into the server computer</br>
	2. Open the project on Android Studio</br>
	3. On the file named **UploadUtility.kt** at  line  20,change  the **serverURL** variable  byyour  API  URL  (http ://xxx.xxx.xxx.xxx:8000/idreader, where xxx.xxx.xxx.xxx represents the IP address of the computer hosting the API)</br>
	4. On the file named **UploadUtility.kt** at line 21, change the **serverUploadDirectoryPath** variable by your server URL (http: //xxx.xxx.xxx.xxx:8000, where xxx.xxx.xxx.xxx represents the IP address of the computer hosting the API)</br>
	5. Build the app</br>
	6. Enjoy! 